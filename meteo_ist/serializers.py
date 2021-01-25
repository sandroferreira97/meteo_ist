from rest_framework import serializers

from .models import range_data

class rangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = range_data
        fields = ('start', 'end')