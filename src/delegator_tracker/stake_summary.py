import logging
from decimal import Decimal


def summarize_stakes(delegators, exponent):
    total_stake = Decimal(0)
    factor = Decimal(10) ** Decimal(exponent)  # Conversion factor based on exponent

    for delegator in delegators:
        amount = Decimal(delegator['delegation']['shares'])  # Convert to Decimal for precision
        logging.debug(f'Adding delegator {delegator} with stake amount {amount}')
        total_stake += amount / factor  # Convert to the main denom using exponent

    # Return the stake adjusted by the exponent
    return total_stake.quantize(Decimal('0.000001'))  # Round to 6 decimal places for readability
