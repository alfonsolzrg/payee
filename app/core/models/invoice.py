# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

from django.db import models
from django.utils.translation import ugettext as _

from app.core.models.base import BaseModel


class Invoice(BaseModel):
    """Can represent either a Customer or a Provider."""

    company = models.ForeignKey(
        # Represents the company making this invoice
        'core.Company'
    )
    customer = models.ForeignKey(
        # The invoice recepient
        'core.BusinessEntity',
        related_name='customer'
    )
    title = models.CharField(
        _('Title'),
        max_length=512,
        db_index=True
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=512,
        db_index=True
    )
    products = models.ManyToManyField(
        # Products contained in this invoice
        'core.Product',
        through='core.InvoicedProduct'
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-id',]
        app_label = 'core'


class InvoicedProduct(BaseModel):
    """Represents an invoiced product."""

    product = models.ForeignKey(
        'core.Product'
    )
    invoice = models.ForeignKey(
        'core.Invoice'
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=15,
        decimal_places=2
    )
    unit_cost = models.DecimalField(
        _('Unit cost'),
        max_digits=15,
        decimal_places=2
    )
    discount_percentage = models.DecimalField(
        _('Discount percentage'),
        max_digits=15,
        decimal_places=2
    )
    tax_rate_percentage = models.DecimalField(
        _('Tax rate percentage'),
        max_digits=15,
        decimal_places=2
    )

    @property
    def discounted_unit_cost(self):
        return self.unit_cost * (1 - self.discount_percentage / 100)

    @property
    def sub_total(self):
        return self.discounted_unit_cost * self.quantity

    @property
    def total(self):
        return self.sub_total * (1 + self.tax_rate / 100)

    class Meta:
        verbose_name = _('Invoiced product')
        verbose_name_plural = _('Invoiced products')
        ordering = ['-id',]
        app_label = 'core'