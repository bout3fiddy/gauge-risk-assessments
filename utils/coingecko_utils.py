from datetime import datetime
from datetime import timedelta
from time import sleep

import pytz
from pycoingecko import CoinGeckoAPI


COINGECKO = CoinGeckoAPI()


def get_current_price_coingecko(
    token_contract: str, currency: str = "usd"
) :

    token_price = COINGECKO.get_token_price(
        id="ethereum",
        contract_addresses=token_contract,
        vs_currencies=currency,
    )

    return token_price


def get_historical_price_coingecko(
    token_contract: str, query_datetime: datetime, currency: str = "usd"
) :

    from_timestamp = query_datetime.timestamp()

    response: dict = {"prices": [], "market_caps": [], "total_volumes": []}
    add_minutes = 60
    while not response["prices"]:
        to_timestamp = (
            query_datetime + timedelta(minutes=add_minutes)
        ).timestamp()
        response = (
            COINGECKO.get_coin_market_chart_range_from_contract_address_by_id(
                id="ethereum",
                contract_address=token_contract,
                vs_currency=currency,
                from_timestamp=int(from_timestamp),
                to_timestamp=int(to_timestamp),
            )
        )
        if response["prices"]:
            break
        print("Warning: Coingecko Rate Limit might get breached.")
        add_minutes += 1
        sleep(1)  # can't make too many calls to CoinGecko ...

    response_price = response["prices"][0][1]
    response_date = pytz.utc.localize(datetime.utcfromtimestamp(to_timestamp))

    return {response_date: response_price}
