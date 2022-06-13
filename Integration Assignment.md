# Assignment

## About the Assignment
- The goal of this assignment is to create a solution for getting the median prices from any given symbol/symbols. 
- In the case that the symbol does not have at least three sources out of the given five, the code should throw an error.
- In the case that the given results from a specific source deviates significantly from the other results, the code 
should omit that result while doing calculations. You may choose a deviation criteria at your own discretion.


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

Make sure to:
1. Think about how the code is structured, maintain good naming convention and use type hinting.
2. Write the code as if the project would be extended in the future.
3. Write down the trade-offs and decisions you have made, stuff you left out if any and what you would do if you had 
more time.

You can find the documentation for the given API's above here:
- Binance: https://binance-docs.github.io/apidocs/spot/en/#change-log
- CoinGecko: https://www.coingecko.com/en/api/documentation
- CoinMarketCap: https://coinmarketcap.com/api/documentation/v1/
- Kraken: https://docs.kraken.com/rest/
- OKX: https://www.okx.com/docs-v5/

Please be aware you will need to create an account for CoinMarketCap in order to get an API key

If you have any doubts or questions, feel free to contact us with them at any time. 
You can reach us at talent@bandprotocol.com or at +66-87-7529673
