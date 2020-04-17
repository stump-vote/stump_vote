# from django.shortcuts import render
import datetime
import pytz
import json
import os.path as op

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
from rest_framework.views import APIView
from .serializers import SampleSerializer, NewsfeedDemoItemSerializer
from .models import Sample, NewsfeedDemoItem


# Create your views here.


class SampleViewSet(viewsets.ModelViewSet):
    """
    A sample model that is exposed using the REST API.
    """
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()


class SomeDataView(APIView):
    """
    Just some random data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of random data
        """
        data = {
            'status': 'ok',
            'date_denver': datetime.datetime.now(pytz.timezone('America/Denver')),
            'date_utc': datetime.datetime.now(pytz.utc),
            'somelist': ['foo', 'bar', 'baz', 42]
        }
        return Response(data)


class ZackDataView(APIView):
    '''
    For Zack's frontend-demo
    '''

    def get(self, request, format=None):
        json_path = op.join(op.dirname(op.abspath(__file__)), 'sample_data', 'frontend_demo.json')
        with open(json_path, "r") as fp:
            data = json.load(fp)
            return Response(data)


class NewsfeedDemoItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    A sample model that is exposed using the REST API.
    """
    serializer_class = NewsfeedDemoItemSerializer
    queryset = NewsfeedDemoItem.objects.all()


class BoulderCandidatesViewSet(viewsets.ViewSet):
    """
    Boulder city council candidates exposed via REST API.
    """
    from .sample_data.boulder_city_council import data
    candidates = [_['_source'] for _ in data['responses'][0]['hits']['hits']]

    def __init__(self, *args, **kwargs):
        # Convert the timestamps from the Elasticsearch query
        for candidate in self.candidates:
            for date_attr in ('Created Date', 'Modified Date'):
                candidate[date_attr + ' X'] = datetime.datetime.fromtimestamp(candidate[date_attr] / 1000.0)
        super().__init__(*args, **kwargs)

    def list(self, request):
        return Response(self.candidates)

    def retrieve(self, request, pk=None):
        candidate = next((_ for _ in self.candidates if _['_id'] == pk), None)
        if candidate is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(candidate)
