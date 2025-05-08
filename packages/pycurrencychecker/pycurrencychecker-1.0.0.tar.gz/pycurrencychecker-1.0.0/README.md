# pycurrencychecker
A simple and easy-to-use Python library for retrieving current currency exchange rates. It uses free services to provide up-to-date data and requires API keys from https://exchangerate.host/.

## Installation

You can install the library directly from PyPI using pip:

```bash
pip install pycurrencychecker
```

## Usage

Below is a basic example of how to use the library:

```python
from pycurrencychecker import CurrencyChecker

# Initialize the CurrencyChecker object
checker = CurrencyChecker(api_key="YOUR_API_KEY")

# Get the exchange rate from USD to EUR
rate = checker.get_exchange_rate("USD", "EUR")
print(f"Exchange rate from USD to EUR: {rate}")
```

## Features

- Retrieve up-to-date exchange rates for multiple currencies.
- Support for over 150 global currencies.
- Easy integration with Python projects.

## Requirements

- Python 3.7 or higher.
- A valid API key from [ExchangeRate Host](https://exchangerate.host/).

## Contributions

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

If you have questions or suggestions, feel free to open an issue in the repository or contact me directly.
