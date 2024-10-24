import time
import logging

from decimal import Decimal
from prometheus_client import start_http_server, Gauge
from delegator_tracker.api_client import fetch_delegator_data
from delegator_tracker.price_fetcher import fetch_coin_price
from delegator_tracker.stake_summary import summarize_stakes


# Define Prometheus metrics with a 'delegator_tracker' prefix
delegator_tracker_delegator_count = Gauge('delegator_tracker_delegator_count',
                                          'Number of delegators',
                                          ['validator'])

delegator_tracker_total_stake = Gauge('delegator_tracker_total_stake',
                                      'Total stake amount',
                                      ['validator', 'denom'])

delegator_tracker_total_stake_usd = Gauge('delegator_tracker_total_stake_usd',
                                          'Total stake in USD',
                                          ['validator'])


def run_exporter(config, interval):
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    logging.info("Prometheus exporter running on port 8000")

    while True:
        for chain in config['nodes']:
            exponent = chain.get('exponent', 6)
            display_denom = chain['display_denom']
            cmc_api_id = chain['cmc_api_id']

            # Fetch the USD price for the coin using the globally loaded API key
            usd_price = fetch_coin_price(cmc_api_id, display_denom)
            if usd_price is None:
                logging.warning(f"Could not fetch USD price for {display_denom}, skipping USD calculation.")
                usd_price = 0  # Fallback if price is not available

            # Convert USD price to Decimal
            usd_price = Decimal(usd_price)

            for validator in chain['validators']:
                logging.info(f"Collecting metrics for validator: {validator['validator_id']} on chain: {chain['name']}")
                delegators = fetch_delegator_data(chain['api_url'], validator['validator_id'])
                total_stake = summarize_stakes(delegators, exponent)
                logging.debug(f"Total stake for validator {validator['validator_id']} is {total_stake}")

                # Calculate total stake in USD using Decimal types
                total_stake_usd = total_stake * usd_price
                logging.debug(f"Total stake value in USD for {validator['validator_id']} is: {total_stake_usd}")

                # Update Prometheus metrics
                delegator_tracker_delegator_count.labels(validator['validator_id']).set(len(delegators))
                delegator_tracker_total_stake.labels(validator['validator_id'], display_denom).set(total_stake)
                delegator_tracker_total_stake_usd.labels(validator['validator_id']).set(float(total_stake_usd))

        logging.info(f"Sleeping for {interval} seconds before refreshing metrics...")
        time.sleep(interval)
