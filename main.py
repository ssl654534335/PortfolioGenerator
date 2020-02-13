#imports
from Library.RiskCalc import *
from Library.ReadUniverse import *
from Library.FilterUniverse import *
import os

#example
# os.path.abspath("/Stock_Data/TSLA.csv")
# TSLA = Asset('TSLA',
#             "Tesla",
#              "stock",
#              os.path.abspath("Stock_Data/TSLA.csv"),
#              3
#              )
# GOOG = Asset('GOOG',
#             "Alphabet",
#              "stock",
#              os.path.abspath("Stock_Data/GOOG.csv"),
#              30
#              )

#example
# portf1 = Portfolio(1,30000,0,0,[TSLA,GOOG])
# VaR_value,VaR_perc =value_at_risk(portf1,.95,1)
# print(VaR_value,VaR_perc)

#example
universe = ReadUniverse()
print(universe.count)
filtered_universe = filter_universe(universe)
print(filtered_universe.universe_set)
print(filtered_universe.count)