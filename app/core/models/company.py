# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from app.core.models.business_entity import BaseBusinessEntity


class Company(BaseBusinessEntity):
    """Represents a registered company on our platform."""

    tax_private_key = models.CharField(
        # TODO: Don't forget to encrypt your DB if you're going to do this!
        _('Private Key'),
        max_length=512
    )
    payment_plan = models.ForeignKey(
        # Represents the company's paying plan (monthly, yearly, on-demand...)
        'core.PaymentPlan'
    )

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['-id',]
        app_label = 'core'