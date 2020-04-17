import pytz

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from collections import OrderedDict

from .models import Sample, NewsfeedDemoItem


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ('id', 'title', 'description')


class NewsfeedDemoItemSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    _type = serializers.CharField(source='item_type')  # field same as built-in Python class and will be stripped out below
    image = serializers.URLField(source='main_image')
    bill = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source='pub_date', default_timezone=pytz.timezone('America/Denver'))

    class Meta:
        model = NewsfeedDemoItem
        fields = ('id', '_type', 'topic', 'date', 'feed_key', 'content', 'image', 'bill')

    def get_topic(self, obj):
        if obj.topic is not None:
            return dict(id=obj.topic.id, name=obj.topic.name)

    def get_bill(self, obj):
        if obj.bill is not None:
            return dict(id=obj.bill.id, name=obj.bill.name)

    def to_representation(self, instance):
        '''
        Removes null fields from response, and strip out leading underscores in key name
        '''
        result = super().to_representation(instance)
        return OrderedDict([(key.lstrip('_'), result[key]) for key in result if result[key] is not None])


# User and authenication serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'is_staff', 'is_superuser')
