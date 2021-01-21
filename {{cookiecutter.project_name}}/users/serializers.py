from rest_framework import serializers

from base.consts import FIRST_NAME, LAST_NAME, EMAIL, LANGUAGE, TOKEN, USER, ID, NAME
from base_scr.common.consts import SELECTED_KPIS, INTERNAL_NAME, RelatedNames
from configurations.models import KPI, KPIsBundle
from users.models import UserSelectedKPIs, User


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = (ID, INTERNAL_NAME)


class BundlesSerializer(serializers.ModelSerializer):
    bundle_kpis = KPISerializer(many=True)

    class Meta:
        model = KPIsBundle
        fields = (NAME, RelatedNames.BUNDLE_KPIS)


class UpdateSelectedKPIsSerializer(serializers.ModelSerializer):
    """
    Update the User's selected 4 KPIs
    """
    selected_kpis = serializers.SlugRelatedField(slug_field=INTERNAL_NAME, many=True,
                                                 queryset=KPI.objects.all(), help_text='The KPI Name')

    class Meta:
        model = UserSelectedKPIs
        exclude = (USER, ID)

    def update(self, instance, validated_data):
        instance.order = validated_data[SELECTED_KPIS]
        return super(UpdateSelectedKPIsSerializer, self).update(instance, validated_data)


class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    selected_kpis = serializers.SlugRelatedField(many=True, slug_field=INTERNAL_NAME,
                                                 source='user_selected_kpis.selected_kpis',
                                                 read_only=True, help_text='The KPI Name')

    class Meta:
        model = User
        fields = (FIRST_NAME, LAST_NAME, EMAIL, LANGUAGE, TOKEN, SELECTED_KPIS)

    def get_token(self, obj):
        return obj.auth_token.key
