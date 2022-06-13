import requests
from requests import Session
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
CMC_API_KEY = os.getenv('CMC_API_KEY')


def coingecko_create_id_symbol_dict():
    """Get List of all supported coins_id, and symbol of CoinGecko's coins list.
    Then create a dict mapping of coins_id and symbol 
    
    Args:
        None
    
    Return:
        id_symbol_dict (dict): the dict mapping of coins_id and symbols
    """
    base_url = 'https://api.coingecko.com'
    coins_list_url = "/api/v3/coins/list"

    resp = requests.get(base_url+coins_list_url)
    coins_list = resp.json()
    
    id_symbol_dict = {}
    
    df = pd.DataFrame(coins_list)
    symbol_list = df[['id', 'symbol']]['symbol'].unique()
    
    for symbol in symbol_list:
        id_list =  df[df['symbol'] == symbol]['id']
        
        if len(id_list) > 0:
            id = min(id_list, key=len)
            id_symbol_dict[symbol] = id

    return id_symbol_dict

def coinmarketcap_create_symbols_id_dict():
    """Create dict of symbol and id in CoinMarketCap
    including crypto currencies and fiat currencies
    
    GET /v1/cryptocurrency/map\n
    GET /v1/fiat/map
    https://coinmarketcap.com/api/documentation/v1/
    
    Args:
        None
    
    Return:
        symbol_id_dict (dict): the dict mapping of symbols and symbol_id

    """
    base_url = 'https://pro-api.coinmarketcap.com'
    coins_map_url = '/v1/cryptocurrency/map' # crypto currencies ID Map
    fiat_map_url = '/v1/fiat/map' # fiat currencies ID Map

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }

    session = Session()
    session.headers.update(headers)
    
    coin_data = json.loads(session.get(base_url+coins_map_url).text)['data']
    fiat_data = json.loads(session.get(base_url+fiat_map_url).text)['data']

    coin_df = pd.DataFrame(coin_data, columns=['id', 'symbol', 'rank'])
    fiat_df = pd.DataFrame(fiat_data, columns=['id', 'symbol'])
    
    coin_symbol_list = coin_df.symbol.unique()
    fiat_symbol_list = fiat_df.symbol.unique()
    
    symbol_id_dict = {}

    for s in coin_symbol_list:
        id_list =  coin_df[coin_df['symbol'] == s]['id']
        if len(id_list) > 0:
            max_rank = min(coin_df[coin_df['symbol'] == s]['rank'])
            id = coin_df[coin_df['rank']==max_rank]['id'].values[0]
            symbol_id_dict[s] = str(id)
    
    for s in fiat_symbol_list:
        id =  fiat_df[fiat_df['symbol'] == s]['id'].values[0]
        symbol_id_dict[s] = str(id)
        
    return symbol_id_dict

def kraken_create_symbols_dict():
    """Get List of all Kraken's symbols.
    Then create a dict mapping of symbols and Kraken's symbols
    
    Args:
        None
    
    Return:
        kk_symbol_dict (dict): the dict mapping of symbols and Kraken's symbols
    """
    
    assets = requests.get('https://api.kraken.com/0/public/Assets')
    assets = assets.json()['result']
    
    df = pd.DataFrame(assets).T
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'kk_symbol'})
    
    symbol_list = df.altname.unique()
    kk_symbol_dict = {}
    
    for s in symbol_list:
        kk_symbol =  df[df['altname'] == s]['kk_symbol'].values[0]
        kk_symbol_dict[s] = kk_symbol
    
    return kk_symbol_dict


def main():
    cgk_id_symbol_dict = coingecko_create_id_symbol_dict()
    cmc_symbol_id_dict = coinmarketcap_create_symbols_id_dict()
    kk_symbol_dict = kraken_create_symbols_dict()
    
    cgk_object = json.dumps(cgk_id_symbol_dict)
    cmc_object = json.dumps(cmc_symbol_id_dict)
    kk_object = json.dumps(kk_symbol_dict)
    
    dict_list = ['cgk_id_symbol_dict', 'cmc_symbol_id_dict', 'kk_symbol_dict']
    object_list = [cgk_object, cmc_object, kk_object]
    for i in range(3):
        f = open("static_dict.py", "a")
        f.write(dict_list[i] + " = " + str(object_list[i])+ "\n")
        f.close()
    
    print("Created static dict success")

if __name__ == "__main__":
    main()