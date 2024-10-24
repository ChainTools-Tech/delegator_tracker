import logging
from decimal import Decimal
from delegator_tracker.api_client import fetch_delegator_data
from delegator_tracker.price_fetcher import fetch_coin_price
from delegator_tracker.stake_summary import summarize_stakes


def process_chain_data(config):
    """
    Processes chains and validators data, fetching delegator information,
    total stake, and calculates total stake in USD.

    Returns a list of dictionaries with all relevant data.
    """
    all_validators_data = []

    for chain in config['nodes']:
        exponent = chain.get('exponent', 6)  # Default to 6 if not provided
        display_denom = chain['display_denom']
        cmc_api_id = chain['cmc_api_id']

        # Fetch the USD price for the chain's coin
        usd_price = fetch_coin_price(cmc_api_id, display_denom)
        if usd_price is None:
            logging.warning(f"Could not fetch USD price for {display_denom}, using 0.")
            usd_price = 0

        # Convert USD price to Decimal
        usd_price = Decimal(usd_price)

        for validator in chain['validators']:
            logging.info(f"Processing validator {validator['validator_id']} on chain {chain['name']}")
            delegators = fetch_delegator_data(chain['api_url'], validator['validator_id'])
            total_stake = summarize_stakes(delegators, exponent)

            # Calculate total stake in USD
            total_stake_usd = total_stake * usd_price

            # Collect all relevant data in a dictionary
            all_validators_data.append({
                'chain_name': chain['name'],
                'validator_id': validator['validator_id'],
                'delegators': len(delegators),
                'total_stake': total_stake,
                'total_stake_usd': total_stake_usd,
                'denom': display_denom
            })

    return all_validators_data
