from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
import datetime
from enum import Enum

@dataclass()
class Asset():
    ticker: str #asset ticker symbol
    name: str #full name
    asset_type: str # type of asset stocks, bonds, crypto ..
    price_history_file: str #absolute path location of CSV file with historical data of stock
                            #might not be the best way, but im open to ideas for
                            # how to define a member that encapsulates the stocks prices
    last_price: float # latest price of asset, used for generating portfolio to ensure correct allocation

@dataclass
class Universe():
    count: int
    universe_set: List[Asset]

@dataclass()
class Portfolio():
    user_id: int    # unique identifier for user to know who's portfolio it is
    buying_power: float # Money available for this user that has not being invested yet
    # value_at_risk: float # a risk calculation that I will later implement
    # cond_value_at_risk: float # a risk calculation that I will later implement
    assets: List[Asset] # a list of stocks in this portfolio
    asset_alloc: dict

#### User Database data classes for messaging ######
class RequestType(Enum):
    Holding = 0
    Portfolio = 1
    PortfolioHistory = 2
    User = 3

class Operation(Enum):
    Insert = 0
    Read = 1
    Update = 2
    Delete = 3

@dataclass_json()
@dataclass()
class UDMHolding():
    Id: int
    PortfolioId: int
    Name: str
    Abbreviation: str
    Description: str
    Quantity: int

@dataclass_json()
@dataclass()
class UDMPortfolio():
    Id: int
    OwnerId: int
    Active: bool
    Generated: datetime.datetime
    InitialValue: float
    StopValue: float
    DesiredRisk: float
    Holdings: List[UDMHolding]

@dataclass_json()
@dataclass()
class UDMPortfolioHistory():
    Id: int
    PortfolioId: int
    Date: datetime.datetime
    Valuation: float
    Risk: float
    ActionTakenId: int

@dataclass_json()
@dataclass()
class UDMUser():
    Email: str
    FirstName: str
    LastName: str
    BrokerageAccount: str

@dataclass_json()
@dataclass()
class UDMRequest():
    Email: str
    RequestType: int
    Operation: int
    Holding: UDMHolding
    Portfolio: UDMPortfolio
    PortfolioHistory: UDMPortfolioHistory
    User: UDMUser

#### Portfolio generator data classes for messaging ######
class PGMessageType(Enum):
    Generate = 0
    BackTestResults = 1

@dataclass_json()
@dataclass()
class PGMessage():
    PGMessageType: int
    # back test elements