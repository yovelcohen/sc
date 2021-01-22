from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.consts import FIRST_NAME, LAST_NAME, EMAIL, LANGUAGE, TOKEN


class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (FIRST_NAME, LAST_NAME, EMAIL, LANGUAGE, TOKEN)

    def get_token(self, obj):
        return obj.auth_token.key
