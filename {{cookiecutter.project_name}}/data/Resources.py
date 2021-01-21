import requests

BASE_API_URL = 'https://sds-livestock-data-api-dev.scrdairy.com/api'
FARMS = 'farms'


class URLs:
    FARMS_META = f"{BASE_API_URL}/Farm"
    FARM_KPIS = f"{BASE_API_URL}/Farm/kpi"
    WELL_BEING_KPIS = f"{BASE_API_URL}/Wellbeing"
    BRANCHES_KPIS = f"{BASE_API_URL}/Branch/kpi"
    GROUPS_KPIS = f"{BASE_API_URL}/Group/kpi"
    ZOURA_BILLING = 'https://rest.zuora.com/v1/usage'
    ZOURA_SAND_BOX = 'https://rest.apisandbox.zuora.com/v1/usage'
    SALES_FORCE = NotImplementedError


MILKING_NAMES = ['Milking', 'Default']
NON_MILKING_NAMES = ['Dry', 'DryBranch', 'Heifers']


def get_data_platform_auth_token():
    url = "https://dev-185756.okta.com/oauth2/default/v1/token"

    payload = 'grant_type=client_credentials&scope=connected-devices-data-api-dev'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': "Basic MG9hNjEwaHRqN25kSldpMkszNTc6U3lIa2FEejQ4WGIySFVyd1lURTBvb0NLVlJ5ZmVlZnViRExlZzctRw==",
               'Cookie': 'JSESSIONID=CDE9093D4BB89A9AAD98AD8666CE5F03'
               }
    response = requests.request('POST', url, headers=headers, data=payload)
    return response.json()


def get_zoura_auth_token():
    url = "https://rest.apisandbox.zuora.com/oauth/token"

    payload = 'client_id=c49e3886-f9a9-4edd-bed2-704db6257267&grant_type=client_credentials&client_secret=Unm0vTHEsYMBEqudOBm%2BhSG%2BTBf73qeRe%2BG%3D3c'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request('POST', url, headers=headers, data=payload)
    return response.json()
