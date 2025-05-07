# Solana attestation service
The Solana Attestation Service (SAS) architecture guide is a technical overview of a credibly neutral attestation registry protocol. The SAS is built to enable the association of off-chain data with on-chain wallets through trusted attestations, serving as verifiable claims issued by trusted entities while preserving user privacy.

# Solana attestation service python SDK

## import 

### saslib
```
from saslibpy.credential import Credential
from saslibpy.schema import Schema
from saslibpy.attestation import Attestation
from saslibpy.sas import DEVNET_PROGRAM_ID
```

### solana rpc client
```
from solana.rpc.api import Client
```

### solders tool
```
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
```

## create client
```
client = Client("https://api.devnet.solana.com")
```

## set sas programId
```
#devnet
program_id = DEVNET_PROGRAM_ID
```

## create credential
```
def create_credential():

    _settings = {
            "authority": authority.pubkey(),
            "name": "sdk_credential",
            "signers": [payer.pubkey(), authority.pubkey()]
        }

    credential = Credential(_settings)

    instruction_construct = credential.create_instruction(program_id)

    # Create a message
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = MessageV0.try_compile(payer.pubkey(), [instruction_construct], [], recent_blockhash)

    transaction = VersionedTransaction(message, [payer, authority])

    resp = client.send_transaction(transaction)
    print(resp)

```

## create schema
```
def create_schema():

    from borsh_construct import String

    credential = Credential.from_address(client, credential_pda)

    fields = ["index", "chain", "subject", "score", "timestamp"]

    layout_type = [String, String, String, String, String]
    layout = Schema.encode_layout_data(layout_type)

    _settings = {
        "credential": credential_pda,
        "credential_data": credential,
        "name": "sdk_schema",
        "description": "sdk_schema media score",
        "layout": layout,
        "fieldNames": fields,
        "isPaused": 0,
        "version": "1"
        }

    schema = Schema(_settings)

    #instruction = credential.create_instruction(program_id)
    instruction_construct = schema.create_instruction(program_id)

    # Create a message
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = MessageV0.try_compile(payer.pubkey(), [instruction_construct], [], recent_blockhash)

    transaction = VersionedTransaction(message, [payer, my_account])

    resp = client.send_transaction(transaction)
    print(resp)
    
```

## tokenize schema
```
def tokenize_schema():

    schema = Schema.from_address(client, schema_pda)

    #instruction = credential.create_instruction(program_id)
    instruction_construct = schema.tokenize_instruction(program_id, max_size=100)
    
    # Create a message
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = MessageV0.try_compile(payer.pubkey(), [instruction_construct], [], recent_blockhash)

    transaction = VersionedTransaction(message, [payer, my_account])

    resp = client.send_transaction(transaction)
    print(resp)
```


## create attestation
```
def create_attestation():
    
    schema = Schema.from_address(client, schema_pda)
    attestaion_nonce: Keypair = Keypair.from_bytes(<private_key>)

    attestation_data = {
        "index": "0",
        "chain": "soalna",
        "subject": str(payer.pubkey()),
        "score": "95.43",
        "timestamp": "1746102729"
    }

    _settings = {
        "nonce": attestaion_nonce,
        "credential": schema.credential_pda,
        "credential_data": schema.credential,
        "schema": schema_pda,
        "schema_data": schema,
        "data": attestation_data,
        "signer": schema.credential.signers[0],
        "expiry": 1000
        }
    
    attestation = Attestation(_settings)

    instruction_construct = attestation.create_instruction(program_id)

    # Create a message
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = MessageV0.try_compile(payer.pubkey(), [instruction_construct], [], recent_blockhash)

    transaction = VersionedTransaction(message, [payer, my_account])

    resp = client.send_transaction(transaction)
    print(resp)
```

## create tokenize attestation
```
def create_tokenize_attestation():

    schema = Schema.from_address(client, schema_pda)
    tokenize_attestaion_nonce: Keypair = Keypair.from_bytes(<private_key>)

    attestation_data = {
        "index": "0",
        "chain": "soalna",
        "subject": str(payer.pubkey()),
        "score": "75.3",
        "timestamp": "1746102729"
    }

    mint_name = "Test Asset"
    mint_uri = "https://x.com"
    mint_symbol = "VAT"
    mint_account_space = 1620

    _settings = {
        "nonce": tokenize_attestaion_nonce.pubkey(),
        "credential": schema.credential_pda,
        "credential_data": schema.credential,
        "schema": schema_pda,
        "schema_data": schema,
        "data": attestation_data,
        "signer": schema.credential.signers[0],
        "expiry": 1000,
        "mint_name": mint_name,
        "mint_uri": mint_uri,
        "mint_symbol": mint_symbol,
        "mint_account_space": mint_account_space

        }
    
    attestation = Attestation(_settings)

    #instruction = credential.create_instruction(program_id)
    instruction_construct = attestation.tokenize_instruction(program_id, <recepient>)
    
    # Create a message
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = MessageV0.try_compile(payer.pubkey(), [instruction_construct], [], recent_blockhash)

    transaction = VersionedTransaction(message, [payer, my_account])

    resp = client.send_transaction(transaction)
    print(resp)
```

## fetch credential 
```
def fetch_credential():

    credential = Credential.from_address(client, credential_pda)

    print("credential:", credential)

    instruction = credential.create_instruction(program_id)

    new_credential, pid = Credential.parse_instruction(bytes(instruction))

    print("new_credential:", new_credential)
    print("pid:", pid)
```

## fetch schema
```
def fetch_schema():

    schema = Schema.from_address(client, schema_pda)

    print("schema:", schema)

    instruction = schema.create_instruction(program_id)

    new_schema, pid = Schema.parse_instruction(client, bytes(instruction))

    print("new_schema:", new_schema)
    print("pid:", pid)
```


## fetch attestation 
```
def fetch_attestation():

    attestation = Attestation.from_address(client, attestation_pda)

    print("attestation:", attestation)
    
    instruction = attestation.create_instruction(program_id)

    new_attestation, pid = Attestation.parse_instruction(client, bytes(instruction))

    print("new_attestation:", new_attestation)
    print("pid:", pid)
```
