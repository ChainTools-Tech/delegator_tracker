import requests
import logging
import os
import time

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get API URL and API Key from environment variables
COINMARKETCAP_API_URL = os.getenv("COINMARKETCAP_API_URL", "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

def fetch_coin_price(cmc_api_id, display_denom):
    api_key = COINMARKETCAP_API_KEY
    if not api_key:
        logging.info("No API key provided, skipping price fetch.")
        return 0  # Return 0 when API key is not specified

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    params = {
        'id': cmc_api_id,
        'convert': 'USD'
    }

    try:
        logging.debug(f"CMC API URL: {COINMARKETCAP_API_URL}")
        logging.info(f"Fetching price for {display_denom} with ID {cmc_api_id} from CoinMarketCap...")

        response = requests.get(COINMARKETCAP_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Data received from CMC: {data}")

        usd_price = data['data'][str(cmc_api_id)]['quote']['USD']['price'] or 0
        logging.info(f"Price for {cmc_api_id} is ${usd_price:.10f}")

        time.sleep(3)

        return usd_price
    except (requests.RequestException, KeyError) as e:
        logging.error(f"Failed to fetch price for {cmc_api_id}: {e}")
        return 0  # Return 0 if fetching price fails
