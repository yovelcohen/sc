from rest_framework import serializers

from base.dates.consts import TWO_DAYS_AGO
from base_scr.common.consts import (DATE, NAME, ID,
                                    RelatedNames, FARM_GROUPS, BRANCH,
                                    GROUP_NUMBER, COWS)
from common.consts import (HEALTH_SCORE, TEN_DAYS_AVG_RUMINATION, TEN_DAYS_RUMINATION,
                           DAILY_RUMINATION_VAR, HEALTH_RATE, FILE)
from consumer_api.models import Farm, FarmKPIs, BranchKPIs, Group, Branch, GroupKPIs


class OnlyKPIsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmKPIs
        fields = [HEALTH_SCORE, DAILY_RUMINATION_VAR, TEN_DAYS_RUMINATION, TEN_DAYS_AVG_RUMINATION]


class GroupsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source=GROUP_NUMBER)
    cows = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [ID, NAME, BRANCH, COWS]

    def get_cows(self, obj):
        try:
            score = obj.group_scores.filter(group=obj, date=TWO_DAYS_AGO).latest(DATE).assigned_tag_count
        except GroupKPIs.DoesNotExist:
            score = 0
        return score


class BranchesSerializer(serializers.ModelSerializer):
    cows = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [ID, NAME, COWS]

    def get_cows(self, obj):
        try:
            score = obj.branch_scores.filter(branch=obj, date=TWO_DAYS_AGO).latest(DATE).assigned_tag_count
        except BranchKPIs.DoesNotExist:
            score = 0

        return score


class GraphsSerializer(serializers.ModelSerializer):
    farm_branches = BranchesSerializer(many=True)
    farm_groups = serializers.SerializerMethodField()

    class Meta:
        model = Farm
        fields = [ID, NAME, RelatedNames.FARM_BRANCHES, FARM_GROUPS]

    def get_farm_groups(self, obj):
        query = Group.objects.filter(branch__farm=obj).select_related(BRANCH, 'branch__farm').prefetch_related(
            RelatedNames.GROUPS_SCORES)
        return GroupsSerializer(query, many=True).data


class StatesRequestSerializer(serializers.ModelSerializer):
    health_rate = serializers.ListField(
        child=serializers.DictField(default={
            "health_score_of_farm_72317": 0,
            "date": "2020-12-13",
            "health_score_of_farm_72029": 0
        }, ))
    daily_rumination_variability = serializers.ListField(
        child=serializers.DictField(default={
            "daily_rumination_variability_of_farm_72317": 0,
            "date": "2020-12-13",
            "daily_rumination_variability_of_farm_72029": 0
        }))
    ten_days_rumination_variability = serializers.ListField(
        child=serializers.DictField(default={
            "ten_days_rumination_variability_of_farm_72317": 0,
            "date": "2020-12-13",
            "ten_days_rumination_variability_of_farm_72029": 0
        }))
    ten_days_average_rumination = serializers.ListField(
        child=serializers.DictField(default={
            "ten_days_average_rumination_of_farm_72317": 0,
            "date": "2020-12-05",
            "ten_days_average_rumination_of_farm_72029": 0
        }))

    class Meta:
        model = Farm
        fields = [HEALTH_RATE, DAILY_RUMINATION_VAR, TEN_DAYS_RUMINATION, TEN_DAYS_AVG_RUMINATION]


class CSV_EXPORT(serializers.Serializer):
    file = serializers.CharField(default='<score_name>.csv')

    class Meta:
        fields = [FILE]
