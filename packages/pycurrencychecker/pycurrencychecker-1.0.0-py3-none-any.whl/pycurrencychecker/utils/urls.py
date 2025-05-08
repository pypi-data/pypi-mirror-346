# /home/guillerch/personal/test-python/libraries/pycurrencychecker/pycurrencychecker/utils/urls.py

BASE_URL = "https://api.exchangerate.host"

ENDPOINTS = {
    "live": f"{BASE_URL}/live",
    "historical": f"{BASE_URL}/historical",
    "convert": f"{BASE_URL}/convert",
    "time-frame": f"{BASE_URL}/timeframe",
    "change": f"{BASE_URL}/change",
    "list": f"{BASE_URL}/list",
}