import time
import logging
from prometheus_client import start_http_server, Gauge
from delegator_tracker.common import process_chain_data

# Prometheus metrics
delegator_tracker_delegator_count = Gauge('delegator_tracker_delegator_count', 'Number of delegators', ['validator'])
delegator_tracker_total_stake = Gauge('delegator_tracker_total_stake', 'Total stake amount', ['validator', 'denom'])
delegator_tracker_total_stake_usd = Gauge('delegator_tracker_total_stake_usd', 'Total stake in USD', ['validator'])


def run_exporter(config, interval):
    start_http_server(8000)
    logging.info("Prometheus exporter running on port 8000")

    while True:
        validators_data = process_chain_data(config)
        for v in validators_data:
            delegator_tracker_delegator_count.labels(v['validator_id']).set(v['delegators'])
            delegator_tracker_total_stake.labels(v['validator_id'], v['denom']).set(v['total_stake'])
            delegator_tracker_total_stake_usd.labels(v['validator_id']).set(v['total_stake_usd'])

        logging.info(f"Sleeping for {interval} seconds before refreshing metrics...")
        time.sleep(interval)
