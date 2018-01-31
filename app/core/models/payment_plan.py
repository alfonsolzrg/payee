# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from app.core.models.base import BaseCatalog


class PaymentPlan(BaseCatalog):
    """Payment plans catalog (monthly, yearly, on-demand, etc)."""

    class Meta:
        verbose_name = _('Payment plan')
        verbose_name_plural = _('Payment plans')
        ordering = ['-id',]
        app_label = 'core'