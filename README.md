# DelegatorTracker

**DelegatorTracker** is a Python-based tool for tracking validator delegators and stake amounts across various Cosmos SDK-based blockchains. The tool supports three operational modes: CLI, Prometheus exporter, and web interface. Additionally, it can fetch and display the stake values in USD by pulling pricing data from CoinMarketCap.

## Features

App displays summarized data, including:
- Validator ID
- Number of delegators
- Total stake in native denomination
- Total stake in USD (optional, if API key provided)

## Modes

- **CLI Mode**: Display summarized validator and delegator data in the terminal as a table.
- **Prometheus Exporter**: Exposes metrics for monitoring validator data, including total stake and number of delegators.
- **Web Interface**: A FastAPI-powered web interface to visualize validator and delegator data in a table format in the browser.


### 1. CLI Mode
The CLI mode displays summarized data, including:
- Validator ID
- Number of delegators
- Total stake in native denomination
- Total stake in USD (optional, if API key provided)

To run in CLI mode:

```bash
python -m delegator_tracker --mode cli --chain all --config path_to_config.yaml --log-level INFO
```

### 2. Prometheus Exporter Mode

In this mode, the tool exposes metrics on port 8000 to be scraped by Prometheus, allowing for easy integration with Grafana dashboards.

To run in Exporter mode:

```bash
python -m delegator_tracker --mode exporter --config path_to_config.yaml --interval 60 --log-level INFO
```


### 3. Web Mode

The web interface displays validator data in a table format, including the total stake and USD values, using FastAPI.

To run in Web mode:

```bash
python -m delegator_tracker --mode web --config path_to_config.yaml --log-level INFO
```


Visit the web interface at: http://localhost:8000


## Configuration File

DelegatorTracker uses a YAML configuration file to define chain-specific settings, API endpoints, and validator information.

Here’s an example of the configuration structure:

```yaml
nodes:
  - name: "AssetMantle"
    api_url: "https://rest.assetmantle.one:443/"
    cmc_api_id: "23860"  # CoinMarketCap ID for the coin
    base_denom: "umntl"
    display_denom: "MNTL"
    exponent: 6
    validators:
      - validator_id: "mantlevaloper18w60w6fnptk9dhqpl65mzrejmkt0vvr7u5qwp5"

  - name: "Bitcanna"
    api_url: "https://api.bitcanna.chaintools.tech:443/"
    cmc_api_id: "5278"
    base_denom: "ubcna"
    display_denom: "BCNA"
    exponent: 6
    validators:
      - validator_id: "bcnavaloper19jzepfkd9tnndyveqhukwq4aul4cjseksh70fv"
```

### Configuration File Fields
`name`: The name of the blockchain.

`api_url`: The API endpoint for pulling validator and delegator data.

`cmc_api_id`: The CoinMarketCap ID for fetching USD prices (optional).

`base_denom`: The native denomination of the chain’s tokens.

`display_denom`: The user-friendly symbol for the tokens.

`exponent`: The exponent used to convert the smallest denomination to the display denomination.

`validators`: A list of validators with their corresponding validator_id.


## Environment Variables

The application uses environment variables to store sensitive information like the CoinMarketCap API URL and API key.

You can configure these in a .env file in the root directory of the project:

```bash
COINMARKETCAP_API_URL=https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest
COINMARKETCAP_API_KEY=your_coinmarketcap_api_key
```

## Installing Requirements

To install the required packages along with application, run:

```bash
pip install .
```

## Running the App

You can run the app in any of the three modes by specifying the mode (cli, exporter, or web) in the command-line arguments.


## Logging

You can control the verbosity of logs using the `--log-level` parameter (DEBUG, INFO, WARNING).


## Contribution

Feel free to contribute to the project by opening pull requests or submitting issues!

## License

This project is licensed under the MIT License.

---
Internal tag: 001