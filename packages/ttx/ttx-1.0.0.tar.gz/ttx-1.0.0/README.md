
Python API wrapper for TTX.

## Requirements.

Python 3.9+

## Installation & Usage

### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/ttxdev/ttx.py.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ttxdev/ttx.py.git`)

Then import the package:
```python
import ttx
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ttx
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import ttx
from ttx.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ttx.Configuration(
    host = "http://localhost"
)



# Enter a context with an instance of the API client
with ttx.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ttx.CreatorsApi(api_client)
    username = 'username_example' # str |  (optional)
    ticker = 'ticker_example' # str |  (optional)

    try:
        api_response = api_instance.create_creator(username=username, ticker=ticker)
        print("The response of CreatorsApi->create_creator:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CreatorsApi->create_creator: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*CreatorsApi* | [**create_creator**](docs/CreatorsApi.md#create_creator) | **POST** /creators | 
*CreatorsApi* | [**get_creator**](docs/CreatorsApi.md#get_creator) | **GET** /creators/{slug} | 
*CreatorsApi* | [**get_creator_transactions**](docs/CreatorsApi.md#get_creator_transactions) | **GET** /creators/{creatorSlug}/transactions | 
*CreatorsApi* | [**get_creators**](docs/CreatorsApi.md#get_creators) | **GET** /creators | 
*PlayersApi* | [**gamba**](docs/PlayersApi.md#gamba) | **PUT** /players/me/lootboxes/{lootBoxId}/open | 
*PlayersApi* | [**get_player**](docs/PlayersApi.md#get_player) | **GET** /players/{username} | 
*PlayersApi* | [**get_players**](docs/PlayersApi.md#get_players) | **GET** /players | 
*PlayersApi* | [**get_self**](docs/PlayersApi.md#get_self) | **GET** /players/me | 
*SessionsApi* | [**discord_callback**](docs/SessionsApi.md#discord_callback) | **GET** /sessions/discord/callback | 
*SessionsApi* | [**link_discord_twitch**](docs/SessionsApi.md#link_discord_twitch) | **POST** /sessions/discord/link | 
*SessionsApi* | [**twitch_callback**](docs/SessionsApi.md#twitch_callback) | **GET** /sessions/twitch/callback | 
*TransactionsApi* | [**place_order**](docs/TransactionsApi.md#place_order) | **POST** /transactions | 


## Documentation For Models

 - [CreateTransactionDto](docs/CreateTransactionDto.md)
 - [CreatorDto](docs/CreatorDto.md)
 - [CreatorOrderBy](docs/CreatorOrderBy.md)
 - [CreatorPartialDto](docs/CreatorPartialDto.md)
 - [CreatorPartialDtoPaginationDto](docs/CreatorPartialDtoPaginationDto.md)
 - [CreatorRarityDto](docs/CreatorRarityDto.md)
 - [CreatorShareDto](docs/CreatorShareDto.md)
 - [CreatorTransactionDto](docs/CreatorTransactionDto.md)
 - [DiscordTokenDto](docs/DiscordTokenDto.md)
 - [LinkDiscordTwitchDto](docs/LinkDiscordTwitchDto.md)
 - [LootBoxDto](docs/LootBoxDto.md)
 - [LootBoxResultDto](docs/LootBoxResultDto.md)
 - [ModelId](docs/ModelId.md)
 - [OrderDirection](docs/OrderDirection.md)
 - [PlayerDto](docs/PlayerDto.md)
 - [PlayerDtoPaginationDto](docs/PlayerDtoPaginationDto.md)
 - [PlayerOrderBy](docs/PlayerOrderBy.md)
 - [PlayerPartialDto](docs/PlayerPartialDto.md)
 - [PlayerShareDto](docs/PlayerShareDto.md)
 - [PlayerTransactionDto](docs/PlayerTransactionDto.md)
 - [PlayerType](docs/PlayerType.md)
 - [PortfolioSnapshotDto](docs/PortfolioSnapshotDto.md)
 - [Rarity](docs/Rarity.md)
 - [StreamStatusDto](docs/StreamStatusDto.md)
 - [TimeStep](docs/TimeStep.md)
 - [TokenDto](docs/TokenDto.md)
 - [TransactionAction](docs/TransactionAction.md)
 - [TwitchUserDto](docs/TwitchUserDto.md)
 - [VoteDto](docs/VoteDto.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author




