# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from app.core.models.base import BaseModel, BaseCatalog


class Product(BaseModel):
    """Represents a product bought or sold."""

    company = models.ForeignKey(
        # Represents the company making this invoice
        'core.Company'
    )
    name = models.CharField(
        _('Name'),
        max_length=255
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        db_index=True
    )
    base_price = models.DecimalField(
        _('Base price'),
        max_digits=15,
        decimal_places=2,
        default=0
    )
    unit = models.ForeignKey(
        # Product unit
        'core.Unit'
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-id',]
        app_label = 'core'


class Unit(BaseCatalog):
    """Product Unit."""

    company = models.ForeignKey(
        'core.Company'
    )

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['-id',]
        app_label = 'core'