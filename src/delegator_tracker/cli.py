import argparse
import logging
import os
from tabulate import tabulate
from delegator_tracker.common import process_chain_data

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
    parser.add_argument('--config', default=get_default_config_path(), help="Path to the config file.")
    parser.add_argument('--chain', required=True, help="Name of the chain or 'all' to process all chains.")
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING'], help="Set log level.")
    parser.add_argument('--mode', required=True, choices=['cli', 'web', 'exporter'], help="App mode: cli, web, exporter.")
    parser.add_argument('--interval', type=int, default=60, help="Refresh interval for exporter in seconds. Default is 60.")
    return parser.parse_args()

def run_cli(args, config):
    validators_data = process_chain_data(config)

    # Display the collected data in table format
    headers = ["Chain Name", "Validator ID", "Delegators", "Total Stake", "Total Stake (USD)", "Denomination"]
    table = [[
        v['chain_name'],
        v['validator_id'],
        v['delegators'],
        "{:,.2f}".format(v['total_stake']),
        "${:,.2f}".format(v['total_stake_usd']),
        v['denom']
    ] for v in validators_data]
    print(tabulate(table, headers, tablefmt="grid"))
