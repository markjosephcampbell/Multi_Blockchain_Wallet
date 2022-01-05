# Import dependencies
import subprocess
import json
import os
import web3
import bit
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
from web3.gas_strategies.time_based import medium_gas_price_strategy

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv('mnemonic')

# Import constants.py and necessary functions from bit and web3
from constants import *

w3=web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.set_gas_price_strategy(medium_gas_price_strategy)

# Create a function called `derive_wallets`
def derive_wallets(coin):
    command = ['./derive','--mnemonic=%s'%mnemonic, '--format=json', '--numderive=3','-g','--coin=%s'%coin]
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {BTCTEST:derive_wallets(BTCTEST),ETH:derive_wallets(ETH)}


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return bit.PrivateKeyTestnet(priv_key)
    if coin == ETH:
        return web3.eth.Account.privateKeyToAccount(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == BTCTEST:
        return bit.PrivateKeyTestnet.prepare_transaction(account, [(to, amount, BTC)])
    if coin == ETH:
        am = w3.toWei(amount, "ether")
        gas_est = w3.eth.estimateGas({"from":account, "to":to, "amount":am})
#         w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        #print(w3.isConnected())
        return {'to': to,
                'from': account,
                'value': am,
                'gas': gas_est,
#                 'gasPrice': w3.eth.generateGasPrice(),
                'gasPrice':250000,
                'nonce': w3.eth.getTransactionCount(account),
                'chainId': w3.eth.chain_id
               }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):

    
    if coin == BTCTEST:
        rawtx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(rawtx)
        return bit.network.NetworkAPI.broadcast_tx_testnet(signed)
    if coin == ETH:
        rawtx = create_tx(coin, account.address, to, amount)
        signed = account.signTransaction(rawtx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    
    
#print(priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey']))
#print(priv_key_to_account(ETH, coins[ETH][0]['privkey']))
#privkey=(priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey']))
#print(create_tx(BTCTEST,privkey,'tb1qsgx55dp6gn53tsmyjjv4c2ye403hgxynxs0dnm',0.000001))
#print(send_tx(BTCTEST,privkey,'tb1qsgx55dp6gn53tsmyjjv4c2ye403hgxynxs0dnm',0.000001))
privkey=priv_key_to_account(ETH, coins[ETH][0]['privkey'])
send_tx(ETH,privkey,'0x80464f155168FF5dAE6A41f4977C6794900DA5bb',2)

