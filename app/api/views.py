# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions

from app.core import models
from app.api.serializers import (InvoiceSerializer,
                                 CompanySerializer,
                                 BusinessEntitySerializer,
                                 ProductSerializer)

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = models.Invoice.objects.all()
    serializer_class = InvoiceSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = models.Company.objects.all()
    serializer_class = CompanySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer


class BusinessEntityViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = models.BusinessEntity.objects.all()
    serializer_class = BusinessEntitySerializer