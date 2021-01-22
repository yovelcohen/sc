"""
common docs used by drf spectacular
"""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from common.consts import BRANCH, FARM, GROUP, FILE

STATS_DOCS = """
Dates: if start_date is specified, returns data from given date to yesterday or to end date if specified as well.

IDs : specify one or more IDs of the Farm/Branch/Group you wish to get data for.

Level: specify if you want get data on the Farm, Branch or Group level
"""
API_KEY = OpenApiParameter(name='Authorization', required=True,
                           description="""API-Key <TOKEN>""",
                           location=OpenApiParameter.HEADER)

LEVELS_ENUM = {
    FARM: FARM,
    BRANCH: BRANCH,
    GROUP: GROUP
}

EXPORT_TO_CSV_DOCS = """ 
Same as Get Stats endpoint, only difference is here you have to specify the number of the desired table to export
"""


class DocsParams:
    KPIS = OpenApiParameter(name='kpis',
                            type=OpenApiTypes.STR,
                            description='get tiles for specific kpis')

    TABLE = OpenApiParameter(name='table',
                             type=OpenApiTypes.STR,
                             required=True,
                             description="get specific graph by it's Name")

    TABLE_NAME = OpenApiParameter('table_name', type=OpenApiTypes.STR,
                                  description="get specific graph by it's Name")

    ID = OpenApiParameter(name='id', description='id or array of ids you want to query (branch or group)')

    START_DATE = OpenApiParameter(name='start_date',
                                  type=OpenApiTypes.DATE,
                                  description='format: YYYY-MM-DD')

    END_DATE = OpenApiParameter(name='end_date',
                                type=OpenApiTypes.DATE,
                                description='format: YYYY-MM-DD')

    LEVEL = OpenApiParameter(name='level',
                             type=OpenApiTypes.STR,
                             required=True,
                             enum=LEVELS_ENUM,
                             description='level (farm/branch/group)')

    FARM_ID = OpenApiParameter(name='farm_id',
                               type=OpenApiTypes.STR,
                               required=True,
                               description='specify farm/s'
                               )
    META_FARM_ID = OpenApiParameter(name='farm_id',
                                    type=OpenApiTypes.STR,
                                    required=True,
                                    description="get the farm's branches and groups IDs lists"
                                    )

    KPIS = OpenApiParameter(name=KPIS,
                            type=OpenApiTypes.STR,
                            description='get tiles for specific kpis')


# Example Responses Serializers
class FailedLogin(serializers.Serializer):
    response = serializers.DictField(default={"detail": "This User Could Not Be Authenticated"})


class UserNotFoundResponse(serializers.Serializer):
    response = serializers.DictField(default={"detail": "this user can't be found"})


class CSV_EXPORT(serializers.Serializer):
    file = serializers.CharField(default='<score_name>.csv')

    class Meta:
        fields = [FILE]
