from django.test import TestCase
from django.urls import reverse
from json import loads
from .models import Sample

# Create your tests here.


class SampleApiTestCase(TestCase):

    def setUp(self):
        super().setUp()

    def test_sample_view_success(self):
        s1 = Sample.objects.create(title='Title 1', description='Description 1')
        _ = Sample.objects.create(title='Title 2', description='Description 2')

        # list
        url = reverse('sample-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response_json = loads(response.content)
        self.assertEquals(response_json, [{'id': 1, 'title': 'Title 1', 'description': 'Description 1'}, {'id': 2, 'title': 'Title 2', 'description': 'Description 2'}])

        # detail
        url = reverse('sample-detail', kwargs={'pk': s1.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response_json = loads(response.content)
        self.assertEquals(response_json, {'id': 1, 'title': 'Title 1', 'description': 'Description 1'})
