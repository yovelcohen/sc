from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

NOT_IMPLEMENTED_ERROR = NotImplementedError('Endpoint Not Implemented Yet')


class ModelNotFound(APIException):
    model_name = None
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _(f'No farm associated with this user found')
    default_code = f'farm_not_found'


class ObjectsNotFound(APIException):
    model_name = None
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _(f'No {model_name} associated with this user found')
    default_code = f'{model_name}_not_found'


class ModelStatesNotFound(APIException):
    model_name = None
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _(f'No scores associated with this {model_name} found')
    default_code = 'score_not_found'


class ModelIdNotSupplied(APIException):
    model_name = None
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(f'you have to supply {model_name} ID to get the stats')
    default_code = f'{model_name}_id_not_found'


class DateError(APIException):
    field = None
    base_msg = "can't be after the current date"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(f"end date or start date {base_msg}" if not field else f"{field} {base_msg}")
    default_code = 'wrong_date'


class ContractExpirationDateError(APIException):
    base_msg = "can't be before the current date"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(f"contract expiration date {base_msg}")
    default_code = 'wrong_date'


class DateParamsError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("you can't specify start and end dates")
    default_code = 'use_of_both_params_type_is_not_allowed'


class DatesRangeError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('if using start or end date you must specify both')
    default_code = "can't_accept_only_one_param"


class TableIdNotProvided(ModelIdNotSupplied):
    model_name = 'table'
    default_detail = _('you have to supply table ID/Name to get the csv')


class TableDoesNotExistError(TableIdNotProvided):
    default_detail = _('you have to supply table ID between 1 and 4 to get the csv')
    default_code = 'table_id_not_found_out_of_range'


class TableNotFoundError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('you have to supply table ID to get the csv')
    default_code = 'table_not_found'


class SystemKeyOrIdExists(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _(
        "this System key already exist, if you want to update them, remove and the system key and try again")
    default_code = 'unique key exists'


class BadAccountIdSupplied(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("account with this ID could not be matched")
    default_code = "account_not_found"


class AccountIdNotSupplied(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("you have to supply account id")
    default_code = "account_not_found"


class UserTokenNotProvided(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authentication Token was not provided or is not valid")
    default_code = f'failed_authentication'


class UserCouldNotBeAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("This User Could Not Be Authenticated")
    default_code = f'failed_authentication'


class FarmIdNotSupplied(APIException):
    model_name = 'farm'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(f'you have to supply {model_name} ID to get the stats')
    default_code = f'{model_name}_id_not_found'


class IdsNotProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(f'you have to supply ID/s to get the stats')
    default_code = 'ids_not_found'


class FieldsNotSpecified(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("you have to supply the fields if you want to use this method without specific table")
    default_code = "fields not supplied"


class LevelIsMissingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("you have to supply the level parameter: farm, branch or group")
    default_code = "level_not_supplied"


class WrongRequestParams(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("you can't use farm_id and level=farm, if you want to get these farm,"
                       "request it as the `id` parameter")
    default_code = "bad_ids_supplied"


class LevelMaxAllowedItemsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("you can't compare one farm's groups/branches with another."
                       " specify one farm id when level= branch/group")
    default_code = "bad_ids_supplied"


class GroupNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Couldn't find this group on this farm")
    default_code = "bad_ids_supplied"


class BranchNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Couldn't find this branch on this farm")
    default_code = "bad_ids_supplied"


#    One Object Not Found     #
class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _(f"this user can't be found")
    default_code = f'user_not_found'


class SiteNotFound(ModelNotFound):
    model_name = 'site'


class FarmNotFound(ModelNotFound):
    model_name = 'farm'


class FarmIdNotFound(ModelNotFound):
    model_name = 'farm'
    default_detail = _("one or more of farms IDs supplied was not found or this farm does not belong to this user")


#    Multiple Objects Not Found     #
class FarmsNotFound(ObjectsNotFound):
    model_name = 'farms'


#    Scores Not Found               #
class FarmScoresNotFound(ModelStatesNotFound):
    model_name = 'farm'


#    Supplied ID Errors             #
class AccountsIdNotSupplied(ModelIdNotSupplied):
    model_name = 'account'


class UserHasNoAccessToThisKPI(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("User has no access to this KPI or has not selected it")
    default_code = 'user_kpi_not_found'
