from rest_framework import serializers

from api.models import Farm
from common.consts import (ADMIN_PHONE, ADMIN_EMAIL, LATITUDE, LONGITUDE, NAME, ID, LOCATION)


class FarmSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    location = serializers.StringRelatedField(many=False)

    class Meta:
        model = Farm
        fields = (ID, NAME, LATITUDE, LONGITUDE, LOCATION, ADMIN_EMAIL, ADMIN_PHONE)
        depth = 1

    def get_latitude(self, obj):
        lat = obj.location.get_lat()
        return lat

    def get_longitude(self, obj):
        long = obj.location.get_long()
        return long
