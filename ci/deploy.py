# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from fabric.api import local, run, hosts, env, sudo, settings, abort
from fabric.colors import green, red, yellow


def deploy(tag):
    revision = deploy_ecs_prod_celery_worker(tag)
    print(yellow('[AWS] Deployed Webapp with revision %s' % revision))

    deploy_gke_webapp(tag)
    print(green('[GKE] Deployed WebApp with tag %s' % tag))


def deploy_gke_webapp(tag):
  """
  Update saved gunicorn-deployment Deployment object in Google Kubernetes
  Engine.
  """

  local("""kubectl set image deployment webapp \
      webapp=us.gcr.io/payee-183417/payee:{}""".format(tag),
      capture=True)
  local('kubectl rollout status deployment webapp', capture=True)


def deploy_ecs(tag):
    """
    Deploys a previously saved Task definition on Amazon Elastic Container
    Service.
    """

    family = 'Payee-Webapp'
    task_definition_dict = [
        {
          "portMappings": [],
          "essential": True,
          "name": "Webapp",
          "environment": [
            {
              "name": "BACKEND_URL",
              "value": "https://payee.mx/"
            },
            {
              "name": "DEBUG",
              "value": "0"
            },
            {
              "name": "DJANGO_SETTINGS_MODULE",
              "value": "payee.settings.deploy"
            },
            {
              "name": "MAIN_DB_HOST",
              "value": "127.0.0.1"
            },
            {
              "name": "MAIN_DB_NAME",
              "value": "payee"
            },
            {
              "name": "MAIN_DB_PASS",
              "value": "Use something really strong in here"
            },
            {
              "name": "MAIN_DB_PORT",
              "value": "5432"
            },
            {
              "name": "MAIN_DB_USER",
              "value": "webapp"
            },
            {
              "name": "RAVEN_SENTRY_URL",
              "value": "https://ac42418a5e104973a02bc98ae9ae178d:a94cbdd60b4849b681f6c8d4ee003c39@sentry.io/189967"
            },
          ],
          "image": "821962124919.dkr.ecr.us-east-1.amazonaws.com/payee:{}".format(tag),
          "cpu": 0,
          "memoryReservation": 256,
          "command": [
            "newrelic-admin",
            "run-program",
            "celery",
            "-A",
            "rocket",
            "worker",
            "-l",
            "info"
          ],
        } 
    ]
    with settings(warn_only=True):
        task_definition = local("""
          aws ecs register-task-definition
          --container-definitions "{}" --family {}""".format(
            json.dumps(json.dumps(task_definition_dict))[1:-1], # Escaping " char
            family), capture=True)
    revision = json.loads(task_definition)['taskDefinition']['revision']
    service = local("""aws ecs update-service \
                        --cluster Payee \
                        --service Payee-Webapp \
                        --task-definition {}:{} \
                        --desired-count 2""".format(
        family, revision), capture=True)
    return revision
