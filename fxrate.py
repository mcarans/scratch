from hdx.utilities.dateparse import parse_date, get_timestamp_from_datetime
from hdx.utilities.downloader import Download


def convert_to_timestamp(date):
    return str(int(round(get_timestamp_from_datetime(date))))


base_url = "https://query2.finance.yahoo.com/v8/finance/chart/{currency}=X?period1={date}&period2={date}&interval=1d&events=div%2Csplit&formatted=false&lang=en-US&region=US&corsDomain=finance.yahoo.com"
currency = "GBP"
date = convert_to_timestamp(parse_date("2004-01-01"))
url = base_url.format(currency=currency, date=date)
with Download(user_agent="test") as downloader:
    result = downloader.download_json(url)
    print(result)
