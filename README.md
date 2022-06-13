# Crypto Median Price

## About the project
- [x] The goal of this project is to create a solution for getting the median prices from any given symbol/symbols. 
- [x] In the case that the symbol does not have at least three sources out of the given five, the code should throw an error.
- [x] In the case that the given results from a specific source deviates significantly from the other results, the code 
should omit that result while doing calculations.

The API that are to be used are given below:
- Binance
- CoinGecko
- CoinMarketCap
- Kraken
- OKX

### Input Requirements:
- symbols: List[str]

### Output Requirements:
- median_price: Optional[Decimal]
- error: Optional[Exception]

References of APIs:
- Binance: https://binance-docs.github.io/apidocs/spot/en/#change-log
- CoinGecko: https://www.coingecko.com/en/api/documentation
- CoinMarketCap: https://coinmarketcap.com/api/documentation/v1/
- Kraken: https://docs.kraken.com/rest/
- OKX: https://www.okx.com/docs-v5/

## Installation

### Clone the repo

```bash
git clone https://github.com/PatipanB/Band_integration_assignment.git
```
### Create a virtual environment:
```bash
virtualenv <env_name>
```
See how to install virtualenv here: https://towardsdatascience.com/create-virtual-environment-using-virtualenv-and-add-it-to-jupyter-notebook-6e1bf4e03415

### Activate virtual environment

#### Linux
```bash
source <env_name>/bin/activate
```

#### Windows
```bash
<env_name>\Scripts\activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```

## How To Use This

1. Register and Login to CoinMarketCap account.
2. Get CoinMarketCap's API key and put it in `.env` file like this `CMC_API_KEY="Your API key"`.
3. Run `python create_static_dict.py`. Wait around 1-2 minutes, you will get `static_dict.py` file.
4. Run `python median_price.py`.
5. Enter cryptocurrencies symbols pair in the terminal seperated with space, if have more than one symbols pair.<br/> For exmaple: `BTC/USD ETH/USDT XRP/USDC`.

## Trade-offs
- Seperate static data request in another file. So that users have to run the command for get static data and create `static_dict.py` file means users have to write a file in to local storage. However user will not have to wait for static data request everytimes when run an application.
  
## Future works
- Add input validation when users enter not valid input like `blank space` or don't have `/` in the pairs
- Don't print errors instantly but keep it until the application ends then print
- In the future, if we want to have a private request such as trade orders or wallet balances we can add API key in the `.env` file and declare on the top of `median_price.py` file.