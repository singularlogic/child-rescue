import json
from web3 import Web3
from sha3 import keccak_256
from django.conf import settings


ETH_PROVIDER = settings.ETH_PROVIDER
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS
ETH_PRIVATE_KEY = settings.ETH_PRIVATE_KEY

W3 = Web3(Web3.HTTPProvider(ETH_PROVIDER))
ETH_ACCOUNT = W3.toChecksumAddress(settings.ETH_ACCOUNT)

if not W3.isConnected():
    print("Failed to connect with provider")

contract_json = []
with open("./blockchain/CaseFactory.json") as f:
    contract_json = json.load(f)
CASE_FACTORY_ABI = contract_json["abi"]

with open("./blockchain/CaseContract.json") as f:
    contract_json = json.load(f)
CASE_CONTRACT_ABI = contract_json["abi"]

try:
    case_factory = W3.eth.contract(address=CONTRACT_ADDRESS, abi=CASE_FACTORY_ABI)
except:
    print("Invalid case factory address")

# Creates new case contract and returns its address
def createCase(status):
    try:
        nonce = W3.eth.getTransactionCount(ETH_ACCOUNT)
        transaction = {"chainId": 4224, "gas": 1000000, "gasPrice": W3.eth.gasPrice, "nonce": nonce}

        txn = case_factory.functions.createCase(status).buildTransaction(transaction)
        signed_txn = W3.eth.account.signTransaction(txn, private_key=ETH_PRIVATE_KEY)
        W3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = W3.eth.waitForTransactionReceipt(signed_txn.hash)
        logs = case_factory.events.CaseContractCreated().processReceipt(receipt)
        case_contract_address = logs[0]["args"]["newCaseContract"]
        return case_contract_address
    except:
        print("Unable to create case contract")
        return None


# Changes the status of a case contract
def changeStatus(address, status):
    try:
        nonce = W3.eth.getTransactionCount(ETH_ACCOUNT)
        transaction = {"chainId": 4224, "gas": 100000, "gasPrice": W3.eth.gasPrice, "nonce": nonce}

        case_contract = W3.eth.contract(address=address, abi=CASE_CONTRACT_ABI)
        txn = case_contract.functions.changeStatus(status).buildTransaction(transaction)
        signed_txn = W3.eth.account.sign_transaction(txn, private_key=ETH_PRIVATE_KEY)
        W3.eth.sendRawTransaction(signed_txn.rawTransaction)
        W3.eth.waitForTransactionReceipt(signed_txn.hash)
        return True
    except:
        print("Invalid case contract address")
        return False


# Returns the status of a case contract
def getStatus(address):
    try:
        case_contract = W3.eth.contract(address=address, abi=CASE_CONTRACT_ABI)
        status = case_contract.functions.status().call()
        return status
    except:
        print("Invalid case contract address")
        return None


# Adds feedback on a specific case contract
# All strings except id, date, created_at
# Dates in timestamp
def createFeedback(
    address,
    id,
    date,
    created_at,
    comment,
    feedback_address,
    latitude,
    longitude,
    current_latitude,
    current_longitude,
    source,
    feedback_image,
):
    try:
        case_contract = W3.eth.contract(address=address, abi=CASE_CONTRACT_ABI)
    except:
        print("Invalid case contract address")
        return False

    nonce = W3.eth.getTransactionCount(ETH_ACCOUNT)
    transaction = {"chainId": 4224, "gas": 1000000, "gasPrice": W3.eth.gasPrice, "nonce": nonce}

    try:
        txn = case_contract.functions.createFeedback(
            id,
            keccak_256(comment.encode("utf-8")).hexdigest(),
            keccak_256(feedback_address.encode("utf-8")).hexdigest(),
            keccak_256(latitude.encode("utf-8")).hexdigest(),
            keccak_256(longitude.encode("utf-8")).hexdigest(),
            keccak_256(current_latitude.encode("utf-8")).hexdigest(),
            keccak_256(current_longitude.encode("utf-8")).hexdigest(),
            keccak_256(source.encode("utf-8")).hexdigest(),
            date,
            created_at,
            keccak_256(feedback_image.encode("utf-8")).hexdigest(),
        ).buildTransaction(transaction)
        signed_txn = W3.eth.account.sign_transaction(txn, private_key=ETH_PRIVATE_KEY)
        W3.eth.sendRawTransaction(signed_txn.rawTransaction)
        W3.eth.waitForTransactionReceipt(signed_txn.hash)
        return True
    except Exception as e:
        print("Failed to create feedback")
        print(e)
        return False


# Returns a feedback
def getFeedback(address, id):
    try:
        case_contract = W3.eth.contract(address=address, abi=CASE_CONTRACT_ABI)
        feedback = case_contract.functions.feedbacks(id).call()
        return feedback
    except:
        print("Invalid case contract address")
        return None


# Validates if a feedback has not changed
def validateFeedback(
    address,
    id,
    date,
    created_at,
    comment,
    feedback_address,
    latitude,
    longitude,
    current_latitude,
    current_longitude,
    source,
    feedback_image,
):
    fields = [
        id,
        date,
        created_at,
        bytes.fromhex(keccak_256(comment.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(feedback_address.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(latitude.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(longitude.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(current_latitude.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(current_longitude.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(source.encode("utf-8")).hexdigest()),
        bytes.fromhex(keccak_256(feedback_image.encode("utf-8")).hexdigest()),
    ]

    feedback = getFeedback(address, id)
    for i in range(len(fields)):
        if feedback[i] != fields[i]:
            return False
    return True
