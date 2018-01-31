# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from rest_framework.test import APITestCase

from app.core import models


class APITest(APITestCase):
    """Tests all API Endpoints."""

    def setUp(self):
        self.payment_plan = models.PaymentPlan.objects.create(id='Monthly')
        self.company = models.Company.objects.create(
            name='Test Company',
            legal_name='Test Company Gmbh',
            RFC='TTTT980811',
            tax_private_key=hashlib.md5('Test private key').hexdigest(),
            payment_plan=self.payment_plan
        )
        self.unit = models.Unit.objects.create(id='kg', company=self.company)
        self.product = models.Product.objects.create(
            name='Test product',
            slug='test-product',
            company=self.company,
            base_price=123.99,
            unit=self.unit
        )
        self.customer = models.BusinessEntity.objects.create(
            name='Test customer',
            RFC='CCCC983873',
            legal_name='Test customer Gmbh',
            company=self.company
        )        
        self.invoice = models.Invoice.objects.create(
            company=self.company,
            customer=self.customer,
            title='Test invoice',
            slug='test-invoice',
            description='Invoice for testing. DO NOT PAY.',
        )
        models.InvoicedProduct.objects.create(
            invoice=self.invoice,
            product=self.product,
            quantity=3,
            unit_cost=100,
            discount_percentage=30,
            tax_rate_percentage=10)


    def test_get_companies(self):
        """Tests company list feature."""

        data = {}
        response = self.client.get('/api/company/', data, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['id'], self.company.id)


    def test_get_invoices(self):
        """Tests invoice list feature."""

        data = {}
        response = self.client.get('/api/invoice/', data, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['id'], self.invoice.id)


    def test_get_products(self):
        """Tests product list feature."""

        data = {}
        response = self.client.get('/api/product/', data, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['id'], self.product.id)

    def test_get_customers(self):
        """Tests customer list feature."""

        data = {}
        response = self.client.get('/api/business_entity/', data, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['id'], self.customer.id)

    # Creation tests
    def test_create_companies(self):
        """Tests company create feature."""

        data = {
            'name': 'Test Company 2',
            'legal_name': 'Test Company 2 Gmbh',
            'RFC': 'JJJASDKW0232',
            'tax_private_key': hashlib.md5('Test other key').hexdigest(),
            'payment_plan': self.payment_plan.id
        }
        response = self.client.post('/api/company/', data, format='json')
        self.assertEquals(response.status_code, 201)

        response = self.client.get('/api/company/', data, format='json')
        self.assertEquals(len(response.data), 2)
        self.assertNotEquals(response.data[0]['id'], self.company.id)
        self.assertEquals(response.data[1]['id'], self.company.id)

    def test_create_products(self):
        """Tests product create feature."""

        data = {
            'name': 'Test product number 2',
            'slug': 'test-product-number-2',
            'company': self.company.id,
            'base_price': 456.87,
            'unit': self.unit.id
        }
        response = self.client.post('/api/product/', data, format='json')
        self.assertEquals(response.status_code, 201)

        response = self.client.get('/api/product/', data, format='json')
        self.assertEquals(len(response.data), 2)
        self.assertNotEquals(response.data[0]['id'], self.product.id)
        self.assertEquals(response.data[1]['id'], self.product.id)
