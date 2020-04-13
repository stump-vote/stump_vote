import pytz

from rest_framework import serializers
from collections import OrderedDict

from .models import Sample, NewsfeedDemoItem


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ('id', 'title', 'description')


class NewsfeedDemoItemSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField(many=False)
    type = serializers.CharField(source='item_type')
    image = serializers.URLField(source='main_image')
    bill = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source='pub_date', default_timezone=pytz.timezone('America/Denver'))

    class Meta:
        model = NewsfeedDemoItem
        fields = ('id', 'type', 'topic', 'date', 'feed_key', 'content', 'image', 'bill')

    def get_bill(self, obj):
        if obj.bill is not None:
            return dict(id=obj.bill.id, name=obj.bill.name)

    def to_representation(self, instance):
        '''
        Removes null fields from response
        '''
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
