from django.test import TestCase
from django.urls import reverse
from django.test import TransactionTestCase
from rest_framework import status
from json import loads
from .models import Sample

# Create your tests here.


class SampleApiTestCase(TransactionTestCase):

    def setUp(self):
        super().setUp()

    def test_sample_view_success(self):
        s1 = Sample.objects.create(title='Title 1', description='Description 1')
        _ = Sample.objects.create(title='Title 2', description='Description 2')

        # list view
        url = reverse('sample-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_json = loads(response.content)
        self.assertEquals(response_json, [{'id': 1, 'title': 'Title 1', 'description': 'Description 1'}, {'id': 2, 'title': 'Title 2', 'description': 'Description 2'}])

        # detail view
        url = reverse('sample-detail', kwargs={'pk': s1.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_json = loads(response.content)
        self.assertEquals(response_json, {'id': s1.pk, 'title': s1.title, 'description': s1.description})

        # Add item
        url = reverse('sample-list')
        data = {
            'title': 'Title 3',
            'description': 'Description 3',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        s3 = Sample.objects.last()
        self.assertEquals(s3.title, data['title'])
        self.assertEquals(s3.description, data['description'])
