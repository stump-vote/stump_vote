# from django.shortcuts import render
import datetime
import pytz
import json
import os.path as op

from django.contrib.auth import login
from django.http import Http404

from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from knox.views import LoginView as KnoxLoginView

# from rest_framework import generics
from rest_framework.views import APIView
from .serializers import SampleSerializer, NewsfeedDemoItemSerializer, UserSerializer, GeoLocationSerializer
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


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class GeoLocationAPIView(RetrieveUpdateAPIView):
    '''
    API for address lookup to lat/lon
    '''

    permission_classes = (AllowAny, )
    serializer_class = GeoLocationSerializer

    MY_LOCATION_SESSION_KEY = 'my_location'

    def _get_object_from_session(self):
        session = self.request.session
        if self.MY_LOCATION_SESSION_KEY in session:
            my_location = session[self.MY_LOCATION_SESSION_KEY]
            return my_location
        else:
            return None

    def _set_object_from_session(self, my_location):
        self.request.session[self.MY_LOCATION_SESSION_KEY] = my_location
        return

    def get_object(self):
        my_location = self._get_object_from_session()
        return my_location

    def retrieve(self, request, *args, **kwargs):
        # GET address, latitude, and longitude, if set in the session

        instance = self.get_object()
        if instance is None:
            raise Http404
        serializer = GeoLocationSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # PUT address, latitude and longitude are read-only fields and not changed by the user
        serializer = GeoLocationSerializer(data=request.data)
        if serializer.is_valid():
            new_instance = serializer.save()
            self._set_object_from_session(new_instance)
            return Response(new_instance)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # PATCH address, update if it changed by the caller
        instance = self.get_object()
        serializer = GeoLocationSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            new_instance = serializer.save()
            self._set_object_from_session(new_instance)
            return Response(new_instance)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
