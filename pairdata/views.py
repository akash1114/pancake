from django.shortcuts import render
from django.shortcuts import render
import requests
from datetime import datetime
import defi.defi_tools as dft


def collect_data():
    pairs = dft.pcsPairs(as_df=False)
    df = dft.pcsTokens()
    data = []
    i = 0
    for pair in pairs['data'].values():
        single_pair = {'id': pair['pair_address'], 'index': i + 1,
                       'token0': {'id': pair['base_address'], 'symbol': pair['base_symbol'], 'name': pair['base_name']},
                       'token1': {'id': pair['quote_address'], 'symbol': pair['quote_symbol'],
                                  'name': pair['quote_name']}}
        try:
            single_pair['token0Price'] = df[df.index == pair['base_address']].price.item()
            single_pair['token1Price'] = df[df.index == pair['quote_address']].price.item()
        except:
            single_pair['token0Price'] = price(pair['base_address'])
            single_pair['token1Price'] = price(pair['quote_address'])
        data.append(single_pair)

        i += 1
    date = datetime.fromtimestamp(int(pairs['updated_at']/1000))
    return data, date


def price(id):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = requests.get('https://api.pancakeswap.info/api/v2/tokens/' + id, params={'headers': header})
    if data.status_code == 200:
        return data.json()['data']['price']
    else:
        return 0


# Redirecting collected data to home page
def pancake_data(request):
    output = collect_data()
    return render(request, 'pancake.html', {'output': output[0][0:200],'date':output[1]})
