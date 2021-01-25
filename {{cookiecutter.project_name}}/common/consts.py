from pytz import country_names

TILE = 'tile'
TREND = 'trend'
SCORE = 'score'

FARMNAME = 'FARMNAME'
SystemKey = 'SystemKey'
FARM__NAME = 'farm__name'
FARM = 'farm'
ASSIGNED_TAG_COUNT = 'assigned_tag_count'
ACCOUNT__ID = 'account__id'
BRANCH__FARM = 'branch__farm'
FARM__ACCOUNT = 'farm__account'
FARM__LOCATION = 'farm__location'
FARM__LOCATION__COUNTRY = 'farm__location__country'
FARM__ACCOUNT__SUBSCRIPTION_ID = 'farm__account__zoura_subscription_id'
FARM__ACCOUNT__ID = "farm__account__id"
FARM__ACCOUNT__BILLING_ID = "farm__account__zoura_billing_account_id"
SUBSCRIPTION_ID = 'zoura_subscription_id'
FARM__ACCOUNT__USER = 'farm__account__user'
BRANCH__FARM__NAME = 'branch__farm__name'
BRANCH_FARM_ACCOUNT = 'branch__farm__account'
GROUP__BRANCH = 'group__branch'
GROUP__BRANCH__FARM = 'group__branch__farm'
GROUP__BRANCH__FARM__NAME = 'group__branch__farm__name'
GROUP__BRANCH__FARM__ACCOUNT__NAME = 'group__branch__farm__account__name'

GREEN = 'green'
YELLOW = 'yellow'
RED = 'red'
### FARM, ACCOUNT, USER ###
CONTRACT_EXPIRATION_DATE = 'contract_expiration_date'
ZOURA_BILLING_ID = 'zoura_billing_account_id'
HAS_EXPIRED = 'has_expired'
HOUSING = 'farm_housing'
FARM_TYPE = 'farm_type'
FARM_HOUSING = 'farm_housing'
DEALER = 'dealer_name'
SYSTEM_TYPE = 'system_type'
FARMS_KEYS = 'farms_keys'
BRANCHES = 'branches'

LOCATION__COUNTRY = 'location__country'

TABLE = 'table'
TABLE_NAME = 'table_name'
THRESHOLD = 'threshold'
DATE = 'date'
DATE_UNIX = 'dateUnix'
STARTDATE = 'STARTDATE'
ENDDATE = 'ENDDATE'
QTY = 'QTY'
TAG = 'tag'
UOM = 'UOM'  # Unit of measure
CHARGE_ID = 'CHARGE_ID'
DESCRIPTION = 'DESCRIPTION'
COSTUMERID = 'CUSTOMERID'

SITEID = 'SITEID'
WORKFLOWRUNNUMBER = 'WORKFLOWRUNNUMBER'
EXTERNALRECORDID = 'EXTERNALRECORDID'
EXTERNALBATCHID = 'EXTERNALBATCHID'
USER = 'user'
ACCOUNT = 'account'
KEY = 'key'
CREATED = 'created'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
LANGUAGE = 'language'
IS_ACTIVE = 'is_active'
IS_ADMIN = 'is_admin'
TOKEN = 'token'
EMAIL = 'email'
PASSWORD = 'password'
TYPE = 'type'
EMAIL_ADDRESS = 'email_address'
LOCATION = 'location'
LOCATION_COUNTRY = 'location_country'
EN = 'en'
ALL_FIELDS = '__all__'
ORDER = 'order'
ID = 'id'
PK = 'pk'
NAME = 'name'
ZOURA_SUBSCRIPTION_ID = 'zoura_subscription_id'
SYSTEM_KEY = 'system_key'
MULTIPLE_FARMS = 'multiple_farms'
ACCOUNT_ID = 'account_id'
ACTIVE = 'active'
SHOWN_IN = 'shown_in'

LAT = 'lat'
LON = 'lon'
LATITUDE = 'latitude'
ADMIN_PHONE = 'admin_phone'
ADMIN_EMAIL = 'admin_email'
LONGITUDE = 'longitude'
COUNTRY = 'country'
STREET = 'street'
CITY = 'city'
ADDRESS = 'address'
STATE = 'state'
COUNTRIES_CHOICES: dict = country_names.items()

STATUS = 'status'

DEFAULT = 'default'

AUTHORIZATION = 'Authorization'
FILE = 'file'
TIME_STAMP = 'read_time_local'
ACCESS_TOKEN = 'access_token'
DP = 'DP'
ZOURA = 'ZOURA'
TELEMETRIES = 'telemetries'
DEVICES = 'devices'
SITES = 'sites'
ACCOUNTS = 'accounts'
FARMS = 'farms'
SITE_DEVICES = 'devices'
ACCOUNTS_IDS = 'account_ids'
EXPIRATION_END_DATE = 'expiration_end_date'
SW_VERSION = 'sw_version'
DEALER_NAME = 'dealer_name'
UTC_OFFSET = 'utc_offset'
LAST_SW_UPDATE = 'last_sw_update'
TIMEZONE = 'timezone'
HW_VERSION = 'hw_version'
SOFTWARE_VERSION = 'software_version'
HARDWARE_VERSION = 'hardware_version'
DISCONNECTED = 'Disconnected'
FARM_ID = 'farm_id'
MILKING = 'milking'
GROUP = 'group'
BRANCH = 'branch'
LEVEL = 'level'
POPULATION = 'population'


class RelatedNames:
    ACCOUNT_USERS = 'account_users'
    LOCATION = 'location'