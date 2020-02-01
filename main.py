#imports
from dataclasses import dataclass
from typing import List

@dataclass
class Asset():
    name: str #could be tinker symbol or full name
    asset_type: str # type of asset stocks, bonds, crypto ..
    price_history_file: str #location of CSV file with historical data of stock
                            #might not be the best way, but im open to ideas for
                            # how to define a member that encapsulates the stocks prices
    shares_owned: int

@dataclass
class Universe():
    count: int
    universe_set: List[Asset]

@dataclass()
class Portfolio():
    user_id: int    # unique identifier for user to know who's portfolio it is
    buying_power: float # Money available for this user to buy more equities
    value_at_risk: float # a risk calculation that I will later implement
    cond_value_at_risk: float # a risk calculation that I will later implement
    assets: List[Asset] # a list of stocks in this portfolio

#example
TSLA = Asset("Tesla","stock","/Stock_Data/TSLA.csv",30)
GOOG = Asset("Alphabet","stock","/Stock_Data/GOOG.csv",20)
portf1 = Portfolio(1,30000,0,0,[TSLA,GOOG])

print(portf1)




