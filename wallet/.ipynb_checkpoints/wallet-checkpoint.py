# Import dependencies
import subprocess
import json
import os
import web3
import bit
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv('mnemonic')

# Import constants.py and necessary functions from bit and web3
from constants import *
 
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
        return bit.PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    if coin == ETH:
        return {'to': to, 'from':account.wallet[0], 'value':amount, 'gas':1000, 'gasPrice':web3.eth.gasPrice(), 'nonce':web3.eth.getTransactionCount(), 'chainID':web3.eth.net.getId()}

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx():
    pass

print(priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey']))
#print(priv_key_to_account(ETH, coins[ETH][0]['privkey']))
privkey=(priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey']))
print(create_tx(BTCTEST,privkey,'tb1qsgx55dp6gn53tsmyjjv4c2ye403hgxynxs0dnm',0.000001))