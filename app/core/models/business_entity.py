# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from app.core.models.base import BaseModel


class BaseBusinessEntity(BaseModel):
    """Shared fields for companies and their client/providers."""

    name = models.CharField(
        _('Name'),
        max_length=255
    )
    RFC = models.CharField(
        _('RFC'),
        max_length=255,
        db_index=True
    )
    legal_name = models.CharField(
        _('Legal name'),
        max_length=512
    )

    class Meta:
        abstract = True


class BusinessEntity(BaseBusinessEntity):
    """Can represent either a Customer or a Provider."""

    company = models.ForeignKey(
        'core.Company',
        related_name='parent_company'
    )
    
    class Meta:
        verbose_name = _('Business Entity')
        verbose_name_plural = _('Business Entities')
        ordering = ['-id',]
        app_label = 'core'