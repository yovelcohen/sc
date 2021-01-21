from rest_framework import serializers

from base_scr.common.consts import *
from consumer_api.models import Account, Farm


class CreateUpdateFarmsSerializer(serializers.ModelSerializer):
    account_id = serializers.CharField()

    class Meta:
        model = Farm
        fields = [ID, NAME, SYSTEM_KEY, ACCOUNT_ID, ACTIVE]

    def create(self, validated_data):
        account_id = validated_data.pop(ACCOUNT_ID, None)
        if account_id is None:
            raise serializers.ValidationError('account ID must be supplied')
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError("an Account with this ID not found")

        id_ = validated_data.pop(ID, None)
        if id_ is None:
            raise serializers.ValidationError("Farm ID must be supplied")

        farm, created = Farm.objects.update_or_create(id=id_, defaults=validated_data)
        return farm


class CreateUpdateAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [ID, ZOURA_SUBSCRIPTION_ID, NAME, CONTRACT_EXPIRATION_DATE, ZOURA_BILLING_ID]
