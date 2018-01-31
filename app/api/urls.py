# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from app.api import views


router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'business_entity', views.BusinessEntityViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'invoice', views.InvoiceViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]