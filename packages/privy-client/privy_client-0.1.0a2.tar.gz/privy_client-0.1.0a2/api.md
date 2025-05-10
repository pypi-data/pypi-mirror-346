# Wallets

Types:

```python
from privy_client.types import (
    Wallet,
    WalletAuthenticateWithJwtResponse,
    WalletCreateWalletsWithRecoveryResponse,
    WalletRpcResponse,
)
```

Methods:

- <code title="post /v1/wallets">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">create</a>(\*\*<a href="src/privy_client/types/wallet_create_params.py">params</a>) -> <a href="./src/privy_client/types/wallet.py">Wallet</a></code>
- <code title="patch /v1/wallets/{wallet_id}">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">update</a>(wallet_id, \*\*<a href="src/privy_client/types/wallet_update_params.py">params</a>) -> <a href="./src/privy_client/types/wallet.py">Wallet</a></code>
- <code title="get /v1/wallets">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">list</a>(\*\*<a href="src/privy_client/types/wallet_list_params.py">params</a>) -> <a href="./src/privy_client/types/wallet.py">SyncCursor[Wallet]</a></code>
- <code title="post /v1/user_signers/authenticate">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">authenticate_with_jwt</a>(\*\*<a href="src/privy_client/types/wallet_authenticate_with_jwt_params.py">params</a>) -> <a href="./src/privy_client/types/wallet_authenticate_with_jwt_response.py">WalletAuthenticateWithJwtResponse</a></code>
- <code title="post /v1/wallets_with_recovery">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">create_wallets_with_recovery</a>(\*\*<a href="src/privy_client/types/wallet_create_wallets_with_recovery_params.py">params</a>) -> <a href="./src/privy_client/types/wallet_create_wallets_with_recovery_response.py">WalletCreateWalletsWithRecoveryResponse</a></code>
- <code title="get /v1/wallets/{wallet_id}">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">get</a>(wallet_id) -> <a href="./src/privy_client/types/wallet.py">Wallet</a></code>
- <code title="post /v1/wallets/{wallet_id}/rpc">client.wallets.<a href="./src/privy_client/resources/wallets/wallets.py">rpc</a>(wallet_id, \*\*<a href="src/privy_client/types/wallet_rpc_params.py">params</a>) -> <a href="./src/privy_client/types/wallet_rpc_response.py">WalletRpcResponse</a></code>

## Transactions

Types:

```python
from privy_client.types.wallets import TransactionGetResponse
```

Methods:

- <code title="get /v1/wallets/{wallet_id}/transactions">client.wallets.transactions.<a href="./src/privy_client/resources/wallets/transactions.py">get</a>(path_wallet_id, \*\*<a href="src/privy_client/types/wallets/transaction_get_params.py">params</a>) -> <a href="./src/privy_client/types/wallets/transaction_get_response.py">TransactionGetResponse</a></code>

## Balance

Types:

```python
from privy_client.types.wallets import BalanceGetResponse
```

Methods:

- <code title="get /v1/wallets/{wallet_id}/balance">client.wallets.balance.<a href="./src/privy_client/resources/wallets/balance.py">get</a>(wallet_id, \*\*<a href="src/privy_client/types/wallets/balance_get_params.py">params</a>) -> <a href="./src/privy_client/types/wallets/balance_get_response.py">BalanceGetResponse</a></code>

# Users

Types:

```python
from privy_client.types import User, UserDeleteResponse, UserCreateCustomMetadataResponse
```

Methods:

- <code title="post /v1/users">client.users.<a href="./src/privy_client/resources/users.py">create</a>(\*\*<a href="src/privy_client/types/user_create_params.py">params</a>) -> <a href="./src/privy_client/types/user.py">User</a></code>
- <code title="get /v1/users">client.users.<a href="./src/privy_client/resources/users.py">list</a>(\*\*<a href="src/privy_client/types/user_list_params.py">params</a>) -> <a href="./src/privy_client/types/user.py">SyncCursor[User]</a></code>
- <code title="delete /v1/users/{user_id}">client.users.<a href="./src/privy_client/resources/users.py">delete</a>(user_id) -> UserDeleteResponse</code>
- <code title="post /v1/users/{user_id}/custom_metadata">client.users.<a href="./src/privy_client/resources/users.py">create_custom_metadata</a>(user_id) -> <a href="./src/privy_client/types/user_create_custom_metadata_response.py">UserCreateCustomMetadataResponse</a></code>
- <code title="get /v1/users/{user_id}">client.users.<a href="./src/privy_client/resources/users.py">get</a>(user_id) -> <a href="./src/privy_client/types/user.py">User</a></code>

# Policies

Types:

```python
from privy_client.types import Policy
```

Methods:

- <code title="post /v1/policies">client.policies.<a href="./src/privy_client/resources/policies.py">create</a>(\*\*<a href="src/privy_client/types/policy_create_params.py">params</a>) -> <a href="./src/privy_client/types/policy.py">Policy</a></code>
- <code title="patch /v1/policies/{policy_id}">client.policies.<a href="./src/privy_client/resources/policies.py">update</a>(policy_id, \*\*<a href="src/privy_client/types/policy_update_params.py">params</a>) -> <a href="./src/privy_client/types/policy.py">Policy</a></code>
- <code title="delete /v1/policies/{policy_id}">client.policies.<a href="./src/privy_client/resources/policies.py">delete</a>(policy_id) -> <a href="./src/privy_client/types/policy.py">Policy</a></code>
- <code title="get /v1/policies/{policy_id}">client.policies.<a href="./src/privy_client/resources/policies.py">get</a>(policy_id) -> <a href="./src/privy_client/types/policy.py">Policy</a></code>

# Transactions

Types:

```python
from privy_client.types import TransactionGetResponse
```

Methods:

- <code title="get /v1/transactions/{transaction_id}">client.transactions.<a href="./src/privy_client/resources/transactions.py">get</a>(transaction_id) -> <a href="./src/privy_client/types/transaction_get_response.py">TransactionGetResponse</a></code>

# KeyQuorums

Types:

```python
from privy_client.types import KeyQuorum
```

Methods:

- <code title="post /v1/key_quorums">client.key_quorums.<a href="./src/privy_client/resources/key_quorums.py">create</a>(\*\*<a href="src/privy_client/types/key_quorum_create_params.py">params</a>) -> <a href="./src/privy_client/types/key_quorum.py">KeyQuorum</a></code>
- <code title="patch /v1/key_quorums/{key_quorum_id}">client.key_quorums.<a href="./src/privy_client/resources/key_quorums.py">update</a>(key_quorum_id, \*\*<a href="src/privy_client/types/key_quorum_update_params.py">params</a>) -> <a href="./src/privy_client/types/key_quorum.py">KeyQuorum</a></code>
- <code title="delete /v1/key_quorums/{key_quorum_id}">client.key_quorums.<a href="./src/privy_client/resources/key_quorums.py">delete</a>(key_quorum_id) -> <a href="./src/privy_client/types/key_quorum.py">KeyQuorum</a></code>
- <code title="get /v1/key_quorums/{key_quorum_id}">client.key_quorums.<a href="./src/privy_client/resources/key_quorums.py">get</a>(key_quorum_id) -> <a href="./src/privy_client/types/key_quorum.py">KeyQuorum</a></code>

# Fiat

## Accounts

Types:

```python
from privy_client.types.fiat import AccountCreateResponse, AccountGetResponse
```

Methods:

- <code title="post /v1/users/{user_id}/fiat/accounts">client.fiat.accounts.<a href="./src/privy_client/resources/fiat/accounts.py">create</a>(user_id, \*\*<a href="src/privy_client/types/fiat/account_create_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/account_create_response.py">AccountCreateResponse</a></code>
- <code title="get /v1/users/{user_id}/fiat/accounts">client.fiat.accounts.<a href="./src/privy_client/resources/fiat/accounts.py">get</a>(user_id, \*\*<a href="src/privy_client/types/fiat/account_get_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/account_get_response.py">AccountGetResponse</a></code>

## KYC

Types:

```python
from privy_client.types.fiat import KYCCreateResponse, KYCUpdateResponse, KYCGetResponse
```

Methods:

- <code title="post /v1/users/{user_id}/fiat/kyc">client.fiat.kyc.<a href="./src/privy_client/resources/fiat/kyc.py">create</a>(user_id, \*\*<a href="src/privy_client/types/fiat/kyc_create_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/kyc_create_response.py">KYCCreateResponse</a></code>
- <code title="patch /v1/users/{user_id}/fiat/kyc">client.fiat.kyc.<a href="./src/privy_client/resources/fiat/kyc.py">update</a>(user_id, \*\*<a href="src/privy_client/types/fiat/kyc_update_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/kyc_update_response.py">KYCUpdateResponse</a></code>
- <code title="get /v1/users/{user_id}/fiat/kyc">client.fiat.kyc.<a href="./src/privy_client/resources/fiat/kyc.py">get</a>(user_id, \*\*<a href="src/privy_client/types/fiat/kyc_get_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/kyc_get_response.py">KYCGetResponse</a></code>

## Onramp

Types:

```python
from privy_client.types.fiat import OnrampCreateResponse
```

Methods:

- <code title="post /v1/users/{user_id}/fiat/onramp">client.fiat.onramp.<a href="./src/privy_client/resources/fiat/onramp.py">create</a>(user_id, \*\*<a href="src/privy_client/types/fiat/onramp_create_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/onramp_create_response.py">OnrampCreateResponse</a></code>

## Offramp

Types:

```python
from privy_client.types.fiat import OfframpCreateResponse
```

Methods:

- <code title="post /v1/users/{user_id}/fiat/offramp">client.fiat.offramp.<a href="./src/privy_client/resources/fiat/offramp.py">create</a>(user_id, \*\*<a href="src/privy_client/types/fiat/offramp_create_params.py">params</a>) -> <a href="./src/privy_client/types/fiat/offramp_create_response.py">OfframpCreateResponse</a></code>
