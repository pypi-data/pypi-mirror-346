import requests
from .utils.urls import ENDPOINTS

def get_currency_list(token: str) -> dict:
    """
    Retrieves the list of currencies from the ExchangeRate API.

    Args:
        token (str): The API access key for authentication. This is a required parameter.

    Returns:
        dict: A dictionary containing the list of currencies.

    Raises:
        Exception: If the API request fails, an exception is raised with
            the HTTP status code and error message.
    """
    url = f"{ENDPOINTS['list']}?access_key={token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_currency_rate(
    token: str,
    source: str = None,
    currencies: str = None,
) -> dict:
    """
    Fetches the exchange rates for specified currencies from the ExchangeRate API.

    Args:
        source (str, optional): The source currency code (e.g., "USD"). Defaults to "USD".
        currencies (str, optional): A comma-separated list of target currency codes
            (e.g., "EUR,GBP,JPY"). Defaults to "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB".
        token (str): The API access key for authentication. This is a required parameter.

    Returns:
        dict: A dictionary containing the exchange rate data retrieved from the API.

    Raises:
        Exception: If the API request fails, an exception is raised with the HTTP status
            code and error message.
    """
    if not source:
        source = "USD"
    if not currencies:
        currencies = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB"

    url = f"{ENDPOINTS['live']}?access_key={token}&source={source}&currencies={currencies}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_currency_historical(
    token: str,
    date: str = None,
    source: str = None,
    currencies: str = None,
) -> dict:
    """
    Fetches historical currency exchange rates for a specific date, source currency,
    and a list of target currencies using an API.
    Args:
        date (str, optional): The date for which to retrieve historical exchange rates
            in the format 'YYYY-MM-DD'. Defaults to "2023-10-01".
        source (str, optional): The source currency code (e.g., "USD"). Defaults to "USD".
        currencies (str, optional): A comma-separated list of target currency codes
            (e.g., "EUR,GBP,JPY"). Defaults to "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB".
        token (str): The API access token. This is a required parameter.
    Returns:
        dict: A dictionary containing the historical exchange rate data.
    Raises:
        Exception: If the API request fails, an exception is raised with the HTTP
            status code and error message.
    """
    if not date:
        date = "2023-10-01"
    if not source:
        source = "USD"
    if not currencies:
        currencies = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB"

    url = f"{ENDPOINTS['historical']}?access_key={token}&date={date}&source={source}&currencies={currencies}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_currency_convert(
    token: str,
    from_currency: str = None,
    to_currency: str = None,
    amount: float = None,
    date: str = None,
) -> dict:
    """
    Converts a specified amount from one currency to another using a currency conversion API.
    Args:
        from_currency (str, optional): The currency code to convert from (e.g., "USD"). Defaults to "USD".
        to_currency (str, optional): The currency code to convert to (e.g., "EUR"). Defaults to "EUR".
        amount (float, optional): The amount to convert. Defaults to 1.
        date (str, optional): The date for historical conversion rates in "YYYY-MM-DD" format. Defaults to "2023-10-01".
        token (str): The API access key for authentication. This is a required parameter.
    Returns:
        dict: A dictionary containing the conversion result and related data.
    Raises:
        Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
    """
    if not from_currency:
        from_currency = "USD"
    if not to_currency:
        to_currency = "EUR"
    if not amount:
        amount = 1
    if not date:
        date = "2023-10-01"

    url = f"{ENDPOINTS['convert']}?access_key={token}&from={from_currency}&to={to_currency}&amount={amount}&date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_currency_time_frame(
    token: str,
    start_date: str = None,
    end_date: str = None,
    source: str = None,
    currencies: str = None,
) -> dict:
    """
    Fetches historical currency exchange rates for a specified time frame from the exchangerate API.

    Args:
        start_date (str, optional): The start date for the time frame in the format 'YYYY-MM-DD'.
                                    Defaults to "2023-10-01" if not provided.
        end_date (str, optional): The end date for the time frame in the format 'YYYY-MM-DD'.
                                    Defaults to "2023-10-31" if not provided.
        source (str, optional): The base currency for the exchange rates. Defaults to "USD" if not provided.
        currencies (str, optional): A comma-separated list of target currencies to fetch rates for.
                                    Defaults to "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB" if not provided.
        token (str): The API access key for authentication. This is a required parameter.

    Returns:
        dict: A dictionary containing the historical exchange rates for the specified time frame.

    Raises:
        Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
    """
    if not start_date:
        start_date = "2023-10-01"
    if not end_date:
        end_date = "2023-10-31"
    if not source:
        source = "USD"
    if not currencies:
        currencies = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB"

    url = f"{ENDPOINTS['time-frame']}?access_key={token}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_currency_change(
    token: str,
    start_date: str = None,
    end_date: str = None,
    source: str = None,
    currencies: str = None,
) -> dict:
    """
    Fetches currency exchange rate changes for a specified date range from the exchangerate API.

    Args:
        start_date (str, optional): The start date for the exchange rate data in "YYYY-MM-DD" format.
                                    Defaults to "2023-10-01" if not provided.
        end_date (str, optional): The end date for the exchange rate data in "YYYY-MM-DD" format.
                                    Defaults to "2023-10-31" if not provided.
        source (str, optional): The base currency for the exchange rates. Defaults to "USD" if not provided.
        currencies (str, optional): A comma-separated list of target currencies to fetch rates for.
                                    Defaults to "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB" if not provided.
        token (str): The API access key for authentication. This is a required parameter.

    Returns:
        dict: A dictionary containing the exchange rate changes for the specified currencies and date range.

    Raises:
        Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
    """
    if not start_date:
        start_date = "2023-10-01"
    if not end_date:
        end_date = "2023-10-31"
    if not source:
        source = "USD"
    if not currencies:
        currencies = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB"

    url = f"{ENDPOINTS['change']}?access_key={token}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
