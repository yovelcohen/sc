from rest_framework import serializers

from api.models import Account
from common.consts import ALL_FIELDS


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ALL_FIELDS
