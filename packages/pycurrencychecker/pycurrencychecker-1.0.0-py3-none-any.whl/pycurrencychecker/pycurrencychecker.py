import requests
from .utils.urls import ENDPOINTS

class CurrencyChecker:
    def __init__(self, api_key: str):
        """
        Initializes the CurrencyChecker with the user's API key.

        Args:
            api_key (str): The API access key for authentication.
        """
        self.api_key = api_key
        self.ENDPOINTS = ENDPOINTS

    def get_currency_list(self) -> dict:
        """
        Retrieves the list of currencies from the ExchangeRate API.

        Returns:
            dict: A dictionary containing the list of currencies.

        Raises:
            Exception: If the API request fails, an exception is raised with
                the HTTP status code and error message.
        """
        url = f"{self.ENDPOINTS['list']}?access_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_currency_rate(self, source: str = "USD", currencies: str = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB") -> dict:
        """
        Fetches the exchange rates for specified currencies from the ExchangeRate API.

        Args:
            source (str, optional): The source currency code. Defaults to "USD".
            currencies (str, optional): A comma-separated list of target currency codes. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the exchange rate data retrieved from the API.

        Raises:
            Exception: If the API request fails, an exception is raised with the HTTP status
                code and error message.
        """
        url = f"{self.ENDPOINTS['live']}?access_key={self.api_key}&source={source}&currencies={currencies}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_currency_historical(self, date: str = "2023-10-01", source: str = "USD", currencies: str = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB") -> dict:
        """
        Fetches historical currency exchange rates for a specific date.

        Args:
            date (str, optional): The date for historical rates in 'YYYY-MM-DD'. Defaults to "2023-10-01".
            source (str, optional): The source currency code. Defaults to "USD".
            currencies (str, optional): A comma-separated list of target currency codes. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the historical exchange rate data.

        Raises:
            Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
        """
        url = f"{self.ENDPOINTS['historical']}?access_key={self.api_key}&date={date}&source={source}&currencies={currencies}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_currency_convert(self, from_currency: str = "USD", to_currency: str = "EUR", amount: float = 1, date: str = "2023-10-01") -> dict:
        """
        Converts a specified amount from one currency to another.

        Args:
            from_currency (str, optional): The currency code to convert from. Defaults to "USD".
            to_currency (str, optional): The currency code to convert to. Defaults to "EUR".
            amount (float, optional): The amount to convert. Defaults to 1.
            date (str, optional): The date for historical conversion rates. Defaults to "2023-10-01".

        Returns:
            dict: A dictionary containing the conversion result and related data.

        Raises:
            Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
        """
        url = f"{self.ENDPOINTS['convert']}?access_key={self.api_key}&from={from_currency}&to={to_currency}&amount={amount}&date={date}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_currency_time_frame(self, start_date: str = "2023-10-01", end_date: str = "2023-10-31", source: str = "USD", currencies: str = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB") -> dict:
        """
        Fetches historical currency exchange rates for a specified time frame.

        Args:
            start_date (str, optional): The start date for the time frame. Defaults to "2023-10-01".
            end_date (str, optional): The end date for the time frame. Defaults to "2023-10-31".
            source (str, optional): The base currency for the exchange rates. Defaults to "USD".
            currencies (str, optional): A comma-separated list of target currencies. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the historical exchange rates for the specified time frame.

        Raises:
            Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
        """
        url = f"{self.ENDPOINTS['time-frame']}?access_key={self.api_key}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_currency_change(self, start_date: str = "2023-10-01", end_date: str = "2023-10-31", source: str = "USD", currencies: str = "EUR,GBP,JPY,CAD,AUD,CHF,CNY,SEK,NZD,BOB") -> dict:
        """
        Fetches currency exchange rate changes for a specified date range.

        Args:
            start_date (str, optional): The start date for the exchange rate data. Defaults to "2023-10-01".
            end_date (str, optional): The end date for the exchange rate data. Defaults to "2023-10-31".
            source (str, optional): The base currency for the exchange rates. Defaults to "USD".
            currencies (str, optional): A comma-separated list of target currencies. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the exchange rate changes for the specified currencies and date range.

        Raises:
            Exception: If the API request fails, an exception is raised with the HTTP status code and error message.
        """
        url = f"{self.ENDPOINTS['change']}?access_key={self.api_key}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
