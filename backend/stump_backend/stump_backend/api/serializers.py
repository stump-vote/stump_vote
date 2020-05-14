import pytz
import random
import re

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from stump_auth.models import StumpUser

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

class StumpUserModelSerializer(serializers.ModelSerializer):
    zip_code = serializers.RegexField(r'^\d{5}(?:-\d{4})?$', **dict(error_messages={'invalid': _('Enter a zip code in the format XXXXX or XXXXX-XXXX.')}))
    common_fields = ['id', 'email', 'last_name', 'first_name', 'address', 'city', 'state', 'zip_code', 'latitude', 'longitude']


class UserSerializer(StumpUserModelSerializer):
    # zip_code = serializers.RegexField(r'^\d{5}(?:-\d{4})?$', **dict(error_messages={'invalid': _('Enter a zip code in the format XXXXX or XXXXX-XXXX.')}))

    class Meta:
        model = StumpUser
        fields = StumpUserModelSerializer.common_fields + ['is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'latitude', 'longitude']

    def update(self, instance, validated_data):
        '''
        Updates selected fields on the user model
        '''
        print('update')
        assert isinstance(instance, StumpUser), "Update requires instance of StumpUser"
        print(instance)
        print(validated_data)
        updated = False
        for field in validated_data.keys():
            # Only explictly whitelisted fields are allowed to be updated
            assert field in ['first_name', 'last_name', 'address', 'city', 'state', 'zip_code'], "Update field sanity check, do not update: '{}'".format(field)
            if hasattr(instance, field):
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
                updated = True
        if updated:
            instance.save()
        return instance


class RegisterSerializer(StumpUserModelSerializer):

    class Meta:
        model = StumpUser
        # Note: only pass in email, which will become the username too
        fields = StumpUserModelSerializer.common_fields + ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = StumpUser.objects.create_user(
            validated_data['email'],  # username field
            validated_data['email'],  # email field
            validated_data['password'],
            **dict(first_name=validated_data.get('first_name', ''),
                   last_name=validated_data.get('last_name', ''),
                   address=validated_data.get('address'),
                   city=validated_data.get('city'),
                   state=validated_data.get('state'),
                   zip_code=validated_data.get('zip_code'),
                   )
        )
        return user


class GeoLocationSerializer(serializers.Serializer):
    address = serializers.CharField()
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    def _geolocate_address(self, address):
        '''
        Mock up lat / lon somewhere in North America
        '''
        latitude = random.randrange(26000, 48900)
        longitude = random.randrange(-124000, -72000)
        return latitude / 1000.0, longitude / 1000.0

    def validate_address(self, value):
        '''
        Address validation includes looking up the lat / lon
        '''
        address = value.strip()
        if address == '':
            # DJF checks for this already, but...
            raise serializers.ValidationError(_('Address cannot be empty'))
        return address

    def create(self, validated_data):
        '''
        Create new instance based on validated data. Note that if address validates, we have
        a valid lat / lon too
        '''
        address = validated_data.get('address')
        latitude, longitude = self._geolocate_address(address)
        return dict(address=address, latitude=latitude, longitude=longitude)

    def update(self, instance, validated_data):
        '''
        Updates the instance with validated data, but there is nothing to do since create does this for us
        '''
        new_address = validated_data.get('address')
        if not new_address == instance['address']:
            # Address changed
            return self.create(validated_data)
        else:
            # Address did not change
            return instance
