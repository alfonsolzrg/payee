# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import raven
import os

from fabric.api import local, run, hosts, env, sudo, settings, abort, lcd
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm

from ci.deploy import deploy


GIT_SHA = raven.fetch_git_sha(os.path.dirname(os.pardir))

def prepare_deploy(tag=None):
    ecr_login = local('aws ecr get-login --no-include-email --region us-east-1',
                      capture=True)
    local(ecr_login)
    if not tag:
        tags = local('git tag', capture=True)
        if tags:
            parts = tags.splitlines().pop().split('.')
            sub_version = int(parts.pop()) + 1
            tag = '{}.{}.{}'.format(parts[0], parts[1], sub_version)
        else:
            tag = 'v1.0.0'

    print(green('Tagging release as {}'.format(tag)))
    with settings(warn_only=True):
        result = local('git tag {}'.format(tag), capture=True)
    if result.failed and not confirm("Git tag failed. Continue?"):
        abort("Aborting at user request.")
    local('git push origin --tags')
    local('python manage.py runserver localhost:8000 &')
    with lcd('frontend'):
        local('npm run build')
    local('python manage.py collectstatic --settings=global_settings.deploy --no-input')
    local('pkill python manage.py runserver')
    local('docker build -t payee . -f Dockerfile')
    local('docker tag payee 821962124919.dkr.ecr.us-east-1.amazonaws.com/payee:{}'.format(tag))
    local('docker push 821962124919.dkr.ecr.us-east-1.amazonaws.com/payee:{}'.format(tag))

    local('docker tag payee us.gcr.io/payee-183417/payee:{}'.format(tag))
    local('gcloud docker -- push us.gcr.io/payee-183417/payee:{}'.format(tag))
    return tag


@hosts('ubuntu@delta.rocket.la')
def deploy_delta(tag=None):
    print(yellow('Starting deploy...'))
    tag = prepare_deploy(tag)
    local('python manage.py migrate --settings=global_settings.prod')
    
    # Compressing and uploading files
    local("""gsutil -m \
        -h "Cache-Control:public, max-age=315360000" \
        cp -r -z js,css,html,png,jpg,jpeg -a public-read \
        assets/{} \
        gs://payee-cdn/{}""".format(GIT_SHA, GIT_SHA))
    deploy(tag)
    print(green('Successful deploy of tag {}'.format(tag)))