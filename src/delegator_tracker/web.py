import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from delegator_tracker.api_client import fetch_delegator_data
from delegator_tracker.stake_summary import summarize_stakes
from delegator_tracker.price_fetcher import fetch_coin_price
from decimal import Decimal


app = FastAPI()

# Setup Jinja2 template directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
def show_table(request: Request):
    config = app.state.config  # Access the config from the app state
    validators_data = []

    # Loop through chains and gather data for each validator
    for chain in config['nodes']:
        exponent = chain.get('exponent', 6)
        display_denom = chain['display_denom']
        cmc_api_id = chain['cmc_api_id']

        # Fetch USD price for the chain's coin
        usd_price = fetch_coin_price(cmc_api_id, display_denom)
        if usd_price is None:
            logging.warning(f"Could not fetch USD price for {display_denom}, skipping USD calculation.")
            usd_price = 0  # Fallback if price is not available

        # Convert USD price to Decimal for consistent type
        usd_price = Decimal(usd_price)

        for validator in chain['validators']:
            # Fetch delegator data and total stake
            logging.info(f"Collecting metrics for validator: {validator['validator_id']} on chain: {chain['name']}")
            delegators = fetch_delegator_data(chain['api_url'], validator['validator_id'])
            total_stake = summarize_stakes(delegators, exponent)
            logging.debug(f"Total stake for validator {validator['validator_id']} is {total_stake}")

            # Calculate total stake in USD using Decimal
            total_stake_usd = total_stake * usd_price
            logging.debug(f"Total stake value in USD for {validator['validator_id']} is: {total_stake_usd}")

            # Collect data for the table
            validators_data.append({
                'chain_name': chain['name'],
                'validator_id': validator['validator_id'],
                'delegators': len(delegators),
                'total_stake': total_stake,
                'total_stake_usd': total_stake_usd,
                'denom': display_denom
            })

    # Pass the data to the Jinja2 template for rendering
    return templates.TemplateResponse("table.html", {
        "request": request,
        "validators_data": validators_data
    })

def run_web(config):
    app.state.config = config  # Pass the config to the FastAPI app state
    uvicorn.run(app, host="0.0.0.0", port=8000)
