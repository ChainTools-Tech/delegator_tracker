import requests
import logging


def fetch_delegator_data(api_url, validator_id):
    endpoint = f"{api_url}/cosmos/staking/v1beta1/validators/{validator_id}/delegations"
    delegators = []
    next_key = None

    while True:
        params = {}
        if next_key:
            params['pagination.key'] = next_key

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Append the current page of delegators to the list
            delegators.extend(data.get('delegation_responses', []))

            # Check for the next pagination key
            next_key = data.get('pagination', {}).get('next_key')

            if not next_key:
                break  # No more pages, exit the loop

        except requests.RequestException as e:
            logging.error(f"Failed to fetch delegator data: {e}")
            break

    return delegators
