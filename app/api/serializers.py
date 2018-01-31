# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from app.core import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class BusinessEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessEntity
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):

    products = ProductSerializer(
        many=True,
        source='products.all'
    )
    customer = BusinessEntitySerializer()

    class Meta:
        model = models.Invoice
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ('tax_private_key',)
