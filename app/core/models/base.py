# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class BaseModel(models.Model):
    """Base model containing common fields for all other models."""

    created_on = models.DateTimeField(
        _('Created at'),
        default=timezone.now
    )
    last_updated_on  = models.DateTimeField(
        _('Last updated on'),
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ['created_on',]
        app_label = 'core'


class BaseCatalog(BaseModel):
    """Base model for catalogs."""

    id = models.CharField(
        _('Id'),
        max_length=50,
        primary_key=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    description = models.CharField(
        _('Description'),
        max_length=255,
        blank=True
    )
    is_active = models.BooleanField(
        _('Active?'),
        default=True
    )

    class Meta:
        abstract = True
        ordering = ['name',]
        app_label = 'core'


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name