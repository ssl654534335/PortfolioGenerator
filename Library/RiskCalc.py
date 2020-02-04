import numpy as np
import pandas as pd
from Library.DataClass import *

# obtain data for each asset
def portfolio_get_data(portf: Portfolio):
    historical_data=[]
    weights = []
    investment = 0

    if len(portf.assets) == 0:
        return 0

    for asset in portf.assets:
        # get data
        asset_data= pd.read_csv(asset.price_history_file).drop(columns = ['Open','Low', 'High','Close','Volume'])
        historical_data.append(asset_data)

        current_asset_price = asset_data.iloc[-1][1] * asset.shares_owned  # if csv is ordered in ascending order of dates
        weights.append(current_asset_price)
        investment = investment + current_asset_price  # TODO case when 0 shares owned
    weights = weights/investment
    weights = np.array(weights).round(3)

    return historical_data, weights, round(investment,2)


def value_at_risk(portf: Portfolio):
    port_data = portfolio_get_data(portf)

    print(port_data)

