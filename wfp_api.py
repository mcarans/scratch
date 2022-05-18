# Method to call DataBridges API
from datetime import date

import backoff
import httpx
from dateutil.relativedelta import relativedelta


class HTTPError(Exception):
    pass


class ApiServerError(Exception):
    pass


class TokenScopeError(Exception):
    pass


class ApiNotAuthorizedError(Exception):
    pass


class NotFoundError(Exception):
    pass


API_ENDPOINTS = {
    'commodities': {
        'url': 'vam-data-bridges/1.1.0/Commodities/List',
        'method': 'GET'
    },
    'monthly_prices': {
        'url': 'vam-data-bridges/1.1.0/MarketPrices/PriceMonthly',
        'method': 'GET'
    },
    'alps': {
        'url': 'vam-data-bridges/1.1.0/MarketPrices/Alps',
        'method': 'GET'
    },
}


class WfpApi:
    BASE_URL = 'https://api.wfp.org'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.tokens_by_scopes = {}

    def _refresh_token(self, scopes):
        resp = httpx.post(f'{self.BASE_URL}/token',
                          data={'grant_type': 'client_credentials', 'scope': ' '.join(scopes)},
                          auth=(self.api_key, self.api_secret))
        resp.raise_for_status()
        resp_data = resp.json()
        received_scopes = set(resp_data['scope'].split(' '))
        if not set(scopes).issubset(received_scopes):
            raise TokenScopeError(f'Could not acquire requested scopes: {scopes}')
        self.tokens_by_scopes[scopes] = resp_data['access_token']

    @backoff.on_exception(backoff.expo, (ApiServerError, ApiNotAuthorizedError), max_tries=5)
    def _invoke(self, endpoint_name, params=None, body=None):
        if endpoint_name not in API_ENDPOINTS:
            raise ValueError('Invalid endpoint invoked. Check the system configuration')

        endpoint = API_ENDPOINTS.get(endpoint_name)
        if params is None:
            params = {}
        scopes = endpoint.get('scopes', tuple())
        token = self.tokens_by_scopes.get(scopes, '')
        if token == '':
            self._refresh_token(scopes)
            token = self.tokens_by_scopes.get(scopes, '')

        with httpx.Client(base_url=self.BASE_URL) as client:
            headers = {'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
            resp = client.request(endpoint['method'], endpoint['url'], params=params, json=body, timeout=None,
                                  headers=headers)

            if resp.status_code == httpx.codes.UNAUTHORIZED:
                self._refresh_token(scopes)
                print('unauthorized. Retrying...')
                raise ApiNotAuthorizedError()
            if resp.status_code >= httpx.codes.INTERNAL_SERVER_ERROR:
                print('Internal server error. Retrying...')
                raise ApiServerError()
            if resp.status_code == httpx.codes.NOT_FOUND:
                raise NotFoundError()
            if httpx.codes.BAD_REQUEST <= resp.status_code < httpx.codes.INTERNAL_SERVER_ERROR:
                print('Http client error! Not retrying (as it would be useless)')
                raise HTTPError(f'HTTP Client error ({resp.status_code})')

        return resp.json()

    def get_list(self, endpoint, **kwargs):
        page = 1
        all_data = []
        data = None
        while data is None or len(data) > 0:
            print(f'fetching page {page}')
            kwargs['page'] = page
            data = self._invoke(endpoint, kwargs)['items']
            all_data.extend(data)
            page = page + 1
        return all_data


def dict_of_lists_add(dictionary, key, value):
    """Add value to a list in a dictionary by key

    Args:
        dictionary (DictUpperBound): Dictionary to which to add values
        key (Any): Key within dictionary
        value (Any): Value to add to list in dictionary

    Returns:
        None

    """
    list_objs = dictionary.get(key, list())
    list_objs.append(value)
    dictionary[key] = list_objs




api = WfpApi(api_key=MY_KEY, api_secret=MY_SECRET)
commodities = api.get_list('commodities', CountryCode='GNB')
# prices = api.get_list('monthly_prices', CountryCode='GNB')

six_months_ago = date.today() - relativedelta(months=6)
category_id_weights = {1: 2, 2: 4, 3: 4, 4: 1, 5: 3, 6: 0.5, 7: 0.5}
countryiso3 = 'AFG'
commodities = api.get_list('commodities', CountryCode=countryiso3)
commodity_id_to_category_id = {x['id']: x['categoryId'] for x in commodities}
alps = api.get_list('alps', CountryCode=countryiso3, startDate=six_months_ago)
yearmonth_rows = dict()
for row in alps:
    analysis_value_price_flag = row['analysisValuePriceFlag']
    if analysis_value_price_flag == 'forecast':
        continue
    commodity_id = row['commodityID']
    category_id = commodity_id_to_category_id[commodity_id]
    if category_id >= 8:
        continue
    row['categoryId'] = category_id
    yearmonth = f'{row["commodityPriceDateYear"]}/{row["commodityPriceDateMonth"]}'
    dict_of_lists_add(yearmonth_rows, yearmonth, row)
yearmonths = yearmonth_rows.keys()
latest_yearmonth = max(yearmonths)
commodities_per_market = dict()
commodities_per_market_crisis = dict()
for row in yearmonth_rows[latest_yearmonth]:
    market_id = row['marketID']
    category_id = row['categoryId']
    weighted_value = category_id_weights[category_id]
    commodities_per_market[market_id] = commodities_per_market.get(market_id, 0) + weighted_value
    pewivalue = row['analysisValuePewiValue']
    if pewivalue >= 1.0:
        commodities_per_market_crisis[market_id] = commodities_per_market_crisis.get(market_id, 0) + weighted_value
country_ratio = 0
for market_id in commodities_per_market:
    market_ratio = commodities_per_market_crisis.get(market_id, 0) / commodities_per_market[market_id]
    country_ratio += market_ratio
country_ratio /= len(commodities_per_market)
print(f'{countryiso3} ratio is {country_ratio}')
