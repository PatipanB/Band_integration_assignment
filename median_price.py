import os
import json
import requests
from requests import Session
from dotenv import load_dotenv
from statistics import median

import static_dict

load_dotenv()
CMC_API_KEY = os.getenv('CMC_API_KEY')


def binance_get_price(pair: str) -> (float):
    """Get Price of A pair by Binance
    
    GET /api/v3/ticker/price
    https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
    
    Args:
        pair (str): the trading pair
    
    Return:
        price (float): the price of the trading pair
    """    
    try:
        base_url = 'https://api.binance.com'
        ticker_price_url = '/api/v3/ticker/price'
        
        # transform pair to symbol_pair that match binance parameter
        symbols_pair = pair.split("/")[0]+pair.split("/")[1]
        params = {"symbol": symbols_pair}

        resp = requests.get(base_url+ticker_price_url, params)
        price = float(resp.json()['price'])
        
        return price
        
    except Exception:
        print("Binance cannot get the price")
        return None

def coingecko_get_price(pair: str, cgk_id_symbol_dict: dict) -> (float):
    """Get Price of A pair by CoinGecko
    
    GET /api/v3/simple/price
    https://www.coingecko.com/en/api/documentation
    
    Args:
        pair (str): the trading pair
        cgk_id_symbol_dict (dict): the dict map symbol_id to symbols
        
    Return:
        price (float): the price of the trading pair
    """
    try:
        if not cgk_id_symbol_dict:
            print("Can not find cgk_id_symbol_dict")
            return None
        
        symbols_pair = pair.split("/")
        symbol = cgk_id_symbol_dict[symbols_pair[0].lower()]
        vs_symbol = symbols_pair[1].lower()
        
        base_url = 'https://api.coingecko.com'
        price_url = "/api/v3/simple/price?ids={0}&vs_currencies={1}".format(symbol, vs_symbol)
        
        resp = requests.get(base_url+price_url)
        price = float(resp.json()[symbol][vs_symbol])
        
        return price
    
    except Exception:
        print("Coingecko cannot get the price")
        return None
  
def coinmarketcap_get_price(pair: str, cmc_symbol_id_dict: dict) -> (float):
    """Get Price of A pair by CoinMarketCap
    
    GET /v2/cryptocurrency/quotes/latest
    https://coinmarketcap.com/api/documentation/v1/
    
    Args:
        pair (str): the trading pair
        cmc_symbol_id_dict (dict): the dict map symbols to symbol_id
            
    Return:
        price (float): the price of the trading pair
    """
    try:
        if not cmc_symbol_id_dict:
            print("Can not find cmc_symbol_id_dict")
            return None
        
        base_url = 'https://pro-api.coinmarketcap.com'
        latest_quotes_url = '/v2/cryptocurrency/quotes/latest' 
        
        symbols_pair = pair.split("/")
        symbol_id = cmc_symbol_id_dict[symbols_pair[0]]
        vs_symbol = symbols_pair[1]
        
        parameters = { 'id': symbol_id, 'convert': vs_symbol }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CMC_API_KEY
        }

        session = Session()
        session.headers.update(headers)

        resp = session.get(base_url+latest_quotes_url, params=parameters)
        price = float(json.loads(resp.text)['data'][symbol_id]['quote'][vs_symbol]['price'])

        return price
    
    except Exception:
        print("CoinMarketCap cannot get the price")
        return None

def kraken_get_price(pair: str, kk_symbol_dict: dict) -> (float):
    """Get Price of A pair by Kraken Exchange
    
    GET /public/Ticker
    https://docs.kraken.com/rest/
    
    Args:
        pair (str): the trading pair
        kk_symbol_dict (dict): the dict map symbols to kraken's symbols

    Return:
        price (float): the price of the trading pair
    """
    try:
        if not kk_symbol_dict:
            print("Can not find kk_symbol_dict")
            return None
        
        symbols_pair = pair.split("/")
        # kraken usd XBT instead of BTC
        if symbols_pair[0] == 'BTC':
            symbols_pair[0] = 'XBT'
        if symbols_pair[1] == 'BTC':
            symbols_pair[1] = 'XBT'
            
        symbol = kk_symbol_dict[symbols_pair[0]]
        vs_symbol = kk_symbol_dict[symbols_pair[1]]
        
        base_url = 'https://api.kraken.com/0'
        price_url = "/public/Ticker?pair={0}".format(symbol+vs_symbol)
        
        resp = requests.get(base_url+price_url)
        price = float(resp.json()['result'][symbol+vs_symbol]['c'][0])
        
        return price
    
    except Exception:
        print("Kraken cannot get the price")
        return None

def okx_get_price(pair: str) -> (float):
    """Get Price of A pair by OKX Exchange
    
    GET /api/v5/market/ticker
    https://www.okx.com/docs-v5/
    
    Args:
        pair (str): the trading pair
            
    Return:
        price (float): the price of the trading pair
    """
    try:
        symbols_pair = pair.split("/")
        symbol = symbols_pair[0]
        vs_symbol = symbols_pair[1]
        
        base_url = 'http://www.okx.com'
        price_url = "/api/v5/market/ticker?instId={0}-{1}-SWAP".format(symbol, vs_symbol)
        
        resp = requests.get(base_url+price_url)
        price = float(resp.json()['data'][0]['last'])
        
        return price
    
    except Exception:
        print("OKX cannot get the price")
        return None
    
def calculate_median_price(price_list: list):
    
    if len(price_list)>=3:
        outliers = []
        
        for i in range(len(price_list)):
            price_i = price_list[i]
            median_exclude = median(price_list)
            ceiling = median_exclude + 0.5*median_exclude
            floor = median_exclude - 0.5*median_exclude
            
            if price_i > ceiling or price_i < floor:
                outliers.append(price_i)
        
        for o in outliers:
            price_list.remove(o)
            
        if len(price_list)>=3:
            median_price = median(price_list)
            return median_price
        
        else:
            print("Some price source deviates more than 50 percent that make all the sources less than 3 sources")
            return None
    
    else:
        print("The prices are retrieved less than 3 sources")
        return None

def main():
    
    # static dict for mapping
    cgk_id_symbol_dict = static_dict.cgk_id_symbol_dict
    cmc_symbol_id_dict = static_dict.cmc_symbol_id_dict
    kk_symbol_dict = static_dict.kk_symbol_dict
    
    pairs = []
    median_prices = {}
    
    print("".center(75, "="))
    print("".center(75, "="))
    print(" This application will calculate the median price of symbols pairs ".center(75, " "))
    print(" It will receive a list of symbol pairs ".center(75, " "))
    print(" For example: BTC/USD eth/usdt Xrp/Usd ".center(75, " "))
    print(" Then returns a dict of median price of symbols pair ".center(75, " "))
    print("".center(75, "="))
    print("".center(75, "="))
    print("")
    
    input_string = input("Enter the list of symbol separated by space: ")
    pairs = [symbol.upper() for symbol in input_string.split(" ")]
    
    print("")
    print("Symbol pairs retrieved: ", pairs)
    print("".center(75, "="))
    
    # iterating in symbol pairs the list
    for i in range(0, len(pairs)):
        
        print("".center(75, "="))
        print("Pair "+str(i+1)+": ", pairs[i])
        
        # get price of each pair 
        bn = binance_get_price(pairs[i])
        cgk = coingecko_get_price(pairs[i], cgk_id_symbol_dict)
        cmc = coinmarketcap_get_price(pairs[i], cmc_symbol_id_dict)
        kk = kraken_get_price(pairs[i], kk_symbol_dict)
        okx = okx_get_price(pairs[i])
        
        print("Binance: ", bn)
        print("CoinGecko: ", cgk)
        print("CoinMarketCap: ", cmc)
        print("Kraken: ", kk)
        print("OKX: ", okx)
        print("".center(75, "="))
        
        price_list = [x for x in [bn, cgk, cmc, kk, okx] if x != None]
        
        median_price = calculate_median_price(price_list)
        
        if median_price != None:
            print("Median of pair: "+pairs[i]+" equals to " + "{:.8f}".format(median_price))
            median_prices[pairs[i]] = float("{:.8f}".format(median_price))
        
        print("".center(75, "="))

    if len(median_prices) > 0:
        print("\nMedian Prices: ", median_prices)
        print("")
        
    else:
        print("\nCan not get median price of any symbols pair\n")
    
    print("".center(75, "="))
    
if __name__ == "__main__":
    main()
