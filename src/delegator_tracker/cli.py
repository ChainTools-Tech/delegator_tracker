import argparse
import logging
import os

from tabulate import tabulate
from decimal import Decimal

from delegator_tracker.api_client import fetch_delegator_data
from delegator_tracker.price_fetcher import fetch_coin_price
from delegator_tracker.stake_summary import summarize_stakes


def ensure_config_directory():
    config_dir = os.path.join(os.path.expanduser("~"), ".chaintools")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)


def get_default_config_path():
    home_dir = os.path.expanduser("~")
    default_config_dir = os.path.join(home_dir, ".chaintools")
    return os.path.join(default_config_dir, "delegator_tracker.yaml")


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch validator delegators and summarize stakes.")

    # Default to ~/.chaintools/delegator_tracker.yaml if config is not provided
    parser.add_argument('--config', default=get_default_config_path(),
                        help="Path to the config file. Default is ~/.chaintools/delegator_tracker.yaml")
    parser.add_argument('--chain', required=True, help="Name of the chain or 'all' to process all chains.")
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING'], help="Set log level.")

    # New mode parameter to define the app mode (CLI, web, exporter)
    parser.add_argument('--mode', required=True, choices=['cli', 'web', 'exporter'],
                        help="Mode to run the application: cli, web, or exporter")

    # Interval for the exporter mode (default is 60 seconds)
    parser.add_argument('--interval', type=int, default=60,
                        help="Refresh interval for exporter in seconds. Default is 60.")

    return parser.parse_args()


def run_cli(args, config):
    validators_data = []  # Collect data for tabular display

    for chain in config['nodes']:
        if args.chain.lower() == 'all' or chain['name'].lower() == args.chain.lower():
            exponent = chain.get('exponent', 6)  # Default to 6 if not provided
            display_denom = chain['display_denom']
            cmc_api_id = chain['cmc_api_id']

            # Fetch the USD price for the coin
            usd_price = fetch_coin_price(cmc_api_id, display_denom)
            if usd_price is None:
                usd_price = 0  # Fallback if price is not available

            # Convert USD price to Decimal for consistent type
            usd_price = Decimal(usd_price)

            for validator in chain['validators']:
                logging.debug(f"Fetching data for validator: {validator['validator_id']} on chain: {chain['name']}")
                delegators = fetch_delegator_data(chain['api_url'], validator['validator_id'])
                total_stake = summarize_stakes(delegators, exponent)

                # Calculate total stake in USD
                total_stake_usd = total_stake * usd_price

                # Format numbers to display with commas and two decimal places
                formatted_total_stake = "{:,.2f}".format(total_stake)
                formatted_total_stake_usd = "${:,.2f}".format(total_stake_usd)

                # Collect data for the table
                validators_data.append([
                    chain['name'],  # Chain name
                    validator['validator_id'],  # Validator ID
                    len(delegators),  # Number of delegators
                    formatted_total_stake,  # Total stake (formatted)
                    formatted_total_stake_usd,  # Total stake in USD (formatted)
                    display_denom  # Denomination
                ])

    # Display the collected data in table format
    headers = ["Chain Name", "Validator ID", "Delegators", "Total Stake", "Total Stake (USD)", "Denomination"]
    print(tabulate(validators_data, headers, tablefmt="grid"))