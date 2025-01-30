import requests
import os

BLOCKCHAIR_API_KEY = os.getenv('BLOCKCHAIR_API_KEY', '')
TRONSCAN_API_KEY = os.getenv('TRONSCAN_API_KEY', '')
XMRCHAIN_ENDPOINT = os.getenv('XMRCHAIN_ENDPOINT', 'https://xmrchain.net')

def check_crypto_tx(currency, tx_id):
    if currency == 'BTC':
        url = f"https://api.blockchair.com/bitcoin/dashboards/transaction/{tx_id}"
        params = {}
        if BLOCKCHAIR_API_KEY:
            params['key'] = BLOCKCHAIR_API_KEY
        try:
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            tx_data = data.get('data',{}).get(tx_id,{}).get('transaction',{})
            block_id = tx_data.get('block_id', -1)
            confirmations = tx_data.get('confirmations', 0)
            if block_id != -1 and confirmations > 0:
                return True
        except:
            return False

    elif currency == 'XMR':
        try:
            url = f"{XMRCHAIN_ENDPOINT}/api/transaction/{tx_id}"
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            if data.get('status') == 'success':
                conf = data.get('data',{}).get('confirmations', 0)
                if conf >= 10:
                    return True
        except:
            return False

    elif currency == 'USDT':
        try:
            url = f"https://apilist.tronscan.org/api/transaction-info?hash={tx_id}"
            headers = {}
            if TRONSCAN_API_KEY:
                headers['API-KEY'] = TRONSCAN_API_KEY
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            contract_ret = data.get('contractRet', None)
            confirmed_bool = data.get('confirmed', False)
            if contract_ret == "SUCCESS" and confirmed_bool:
                return True
        except:
            return False

    return False
