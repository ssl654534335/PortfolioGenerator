#imports
from Library.RiskCalc import *
import os

#example
os.path.abspath("/Stock_Data/TSLA.csv")
TSLA = Asset("Tesla",
             "stock",
             os.path.abspath("Stock_Data/TSLA.csv"),
             30
             )
GOOG = Asset("Alphabet",
             "stock",
             os.path.abspath("Stock_Data/GOOG.csv"),
             20
             )

#example
portf1 = Portfolio(1,30000,0,0,[TSLA,GOOG])
value_at_risk(portf1)




