from rest_framework import serializers

from base_scr.common.consts import (ADMIN_PHONE, ADMIN_EMAIL, LATITUDE, LONGITUDE, NAME, ID,
                                    LOCATION)
from consumer_api.models import Farm


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


class TilesResponse(serializers.Serializer):
    first_kpi = serializers.DictField(default={"health_score_avg_score": 0,
                                               "red": 0,
                                               "yellow": 0,
                                               "green": 0
                                               }
                                      )
    second_kpi = serializers.DictField(default={"daily_rumination_variability_avg_score": 0,
                                                "red": 0,
                                                "yellow": 0,
                                                "green": 0
                                                }
                                       )
    third_kpi = serializers.DictField(
        default={"ten_days_rumination_variability_avg_score": 0,
                 "red": 0,
                 "yellow": 0,
                 "green": 0
                 }
    )
    fourth_kpi = serializers.DictField(default={"average_of_avg_ten_days_rumination": 0,
                                                "yellow": 0,
                                                "green": 0
                                                }
                                       )

    class Meta:
        fields = ['health_score_tile', 'daily_rumination_variability_tile', 'ten_days_rumination_variability_tile',
                  'ten_days_average_rumination_tile']
