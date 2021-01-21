from rest_framework import serializers

from base.consts import ALL_FIELDS
from consumer_api.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ALL_FIELDS
