from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response

from account_management_api.models import HasSalesForceApiKey
from account_management_api.serializers import (CreateUpdateAccountsSerializer)
from api.models import Account
from common.base.views import DestroyUpdateCreateViewScr
from common.consts import CONTRACT_EXPIRATION_DATE
from common.consts import ID
from common.dates.utils import convert_str_to_date
from common.utils.utils import get_all_accounts


class AccountsView(DestroyUpdateCreateViewScr):
    """
    Create, Update or Delete an Farm/Site using it's ID
    """
    authentication_classes = []
    permission_classes = [HasSalesForceApiKey]
    serializer_class = CreateUpdateAccountsSerializer

    def get_queryset(self):
        return get_all_accounts()

    @extend_schema(summary='Create Account')
    def create(self, request, *args, **kwargs):
        data = request.data
        _id = data.pop(ID, None)
        if _id is None:
            raise serializers.ValidationError("account ID must be supplied")
        date = data.pop(CONTRACT_EXPIRATION_DATE, None)
        if date is not None:
            data[CONTRACT_EXPIRATION_DATE] = convert_str_to_date(date_to_convert=date)
        account, _ = Account.objects.update_or_create(id=_id, defaults=data)
        serializer = CreateUpdateAccountsSerializer(account, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Update Account')
    def update(self, request, *args, **kwargs):
        super(AccountsView, self).update(request, *args, **kwargs)

    @extend_schema(summary='Partial Update Account')
    def partial_update(self, request, *args, **kwargs):
        super(AccountsView, self).partial_update(request, *args, **kwargs)

    @extend_schema(summary="Delete Account")
    def destroy(self, request, *args, **kwargs):
        super(AccountsView, self).destroy(request, *args, **kwargs)


"""
Below is the implementation of the Farms creation like in MFD, Traceability will implement it differently
"""
# class FarmsView(DestroyUpdateCreateView):
#     """
#     Create, Update or Delete an Account using it's ID
#     """
#     authentication_classes = []
#     permission_classes = [HasSalesForceApiKey]
#     serializer_class = CreateUpdateFarmsSerializer
#
#     def get_queryset(self):
#         # return get_all_farms()
#         pass
#
#     def get_serializer_class(self):
#         return CreateUpdateFarmsSerializer
#
#     @extend_schema(summary='Create Farm')
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         many = True if isinstance(data, list) else False
#
#         farms = [self._create_update_farm(obj) for obj in data] if many is True else self._create_update_farm(data)
#         serializer = CreateUpdateFarmsSerializer(farms, many=many)
#
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def _create_update_farm(self, obj):
#         account_id = obj.pop(ACCOUNT_ID, None)
#         if account_id is None:
#             raise AccountIdNotSupplied
#         else:
#             try:
#                 account = Account.objects.get(id=account_id)
#                 obj[ACCOUNT] = account
#             except Account.DoesNotExist:
#                 raise BadAccountIdSupplied
#
#         try:
#             farm_id = obj.pop(ID, None)
#             if farm_id is None:
#                 raise FarmIdNotSupplied
#
#             farm, _ = Farm.objects.update_or_create(id=farm_id, defaults=obj)
#             return farm
#
#         except IntegrityError:
#             raise SystemKeyOrIdExists
#
#     @extend_schema(summary="Delete Farm")
#     def destroy(self, request, *args, **kwargs):
#         try:
#             farm = self.get_queryset().filter(id=kwargs[PK])
#             if not farm.exists():
#                 raise FarmIdNotFound
#             else:
#                 farm.delete()
#                 return Response(data={'farm deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except Farm.DoesNotExist:
#             raise FarmIdNotFound
#
#     @extend_schema(summary='Update Farm')
#     def update(self, request, *args, **kwargs):
#         super().update(request, *args, **kwargs)
#
#     @extend_schema(summary='Partial Update Farm')
#     def partial_update(self, request, *args, **kwargs):
#         super().partial_update(request, *args, **kwargs)
