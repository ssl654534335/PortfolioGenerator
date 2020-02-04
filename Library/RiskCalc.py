import numpy as np
import pandas as pd
from scipy.stats import norm
from Library.DataClass import *


# obtain data for each asset and return the historical data and weight of each asset along with the portfolio's
# current value (investment)
def portfolio_get_data(portf: Portfolio):
    historical_data = pd.DataFrame()
    weights = []
    investment = 0

    # Empty Portfolio
    if len(portf.assets) == 0:
        return 0

    for asset in portf.assets:
        # get data and reformat
        asset_data = pd.read_csv(asset.price_history_file).drop(columns=['Open', 'Low', 'High', 'Close', 'Volume'])
        asset_data = asset_data.rename(columns={"Adj Close": asset.name})
        asset_data = asset_data.set_index('Date')

        # join new asset data to overall data table
        if historical_data.empty:
            historical_data = asset_data
        elif len(historical_data) >= len(asset_data):
            historical_data = historical_data.join(asset_data)
        else:
            historical_data = asset_data.join(historical_data)

        # store current value of each asset and calulate total investment
        current_asset_price = asset_data.iloc[-1][
                                  0] * asset.shares_owned  # if csv is ordered in ascending order of dates
        weights.append(current_asset_price)
        investment = investment + current_asset_price  # TODO case when 0 shares owned

    # calculate weights of each asset in portfolio
    weights = weights / investment
    weights = np.array(weights).round(3)

    return historical_data, weights, round(investment, 2)

# confidence level .9,.95,.99 where horizon is number of days Value at risk which to be calculated for
def value_at_risk(portf: Portfolio, conf_level: float, horizon: int):
    historical_data, weights, investment = portfolio_get_data(portf)

    # portfolio estimated parameters calculations
    returns = historical_data.pct_change()
    portf_mean = returns.mean().dot(weights)
    portf_std = np.sqrt(weights.T.dot(returns.cov()).dot(weights))

    # parametric calculations
    mean_investment = (1+portf_mean)*investment
    std_investment = investment * portf_std
    cut = norm.ppf((1-conf_level), mean_investment, std_investment)

    # Value at risk
    vr = round((investment - cut)*np.sqrt(horizon),2)
    # returns Value at Risk as a value and as a percentage of total investment
    return vr,round(vr/investment,2)*100

