import numpy as np
import pandas as pd
from scipy.special import erf
from scipy.stats import norm
from Library.DataClass import *
import math

################ For genetic algorithm #################################

# This function returns a pandas dataframe of all the historical prices of all the
# assets in the universe joined in one table
# universe: list of assets in universe
# price_indicator: indicates what column in the orginal .csv file to keep for calculating returns.
# i.e 'open','close', or 'adj. close', etc.
def gen_universe_hist_data(universe:[Asset], price_indicator:str):
    historical_data = pd.DataFrame()

    for asset in universe:
        # get data from csv and reformat dataframe
        asset_data = pd.read_csv(asset.price_history_file)
        col = list(asset_data.columns)
        col.remove(price_indicator)
        col.remove('Date')
        asset_data = asset_data.drop(columns=col)
        asset_data = asset_data.rename(columns={price_indicator: asset.ticker})
        asset_data = asset_data.set_index('Date')
        asset_data = asset_data.dropna()

        # join new asset data to overall data table
        if historical_data.empty:
            historical_data = asset_data
        else:
            historical_data = asset_data.join(historical_data)

    return historical_data

# This function returns historical value at risk
# returns: a single column dataframe holding a list of returns
def gen_var(returns: pd.DataFrame):
    # confidence level for calculating VaR
    # .95 is standard but .99 and .975 can also be used
    conf_level = .95

    # portf_return needs to be sorted in ascending order for VaR Calc
    returns = returns.sort_values()

    # VaR Historical total returns
    tail = 1-conf_level  # the percentile of returns we are cutting off from our distribution
    indx = round((tail*len(returns.index)))  # indx is the index in our portfolio returns where we cut off the tail
    return returns.iloc[indx]  # returns value of our cutoff point aka stop loss

# max entropy possible for any chromosome is the entropy of the universe as a uniform distribution
# since the chromosome is a subset of the universe
# universe: a dataframe of the universe's total returns
def gen_max_entopy(universe: pd.DataFrame):
    n = universe.nunique()  # number of unique returns of all the universe

    # discrete probability of a discrete uniform distribution maximizes shannon entropy
    # so need to define universe as uniform distribution
    p_x = 1 / ((universe.max().max() - universe.min().min()) + 1)

    # discrete shannon equation for discrete uniform distribution
    max_entropy_shannon = -n * p_x * math.log(p_x, 2)

    return max_entropy_shannon

# This function returns the Shannon entropy
# uses square root rule for determining number of subintervals
# returns: a single column dataframe holding a list of returns
# cutoff_value: the cutoff point of our distribution used to reduce risk
def gen_entropy(returns: pd.DataFrame, cutoff_value: float):
    # sort returns in ascending order to ease calculations
    returns = returns.sort_values()

    # need to cut off tail of our returns distribution based on our cutoff value before calculating entropy
    cutoff_indx = 0
    for x in range(0,returns.shape[0]):
        if returns[x] <= cutoff_value:
            cutoff_indx = cutoff_indx+1
        else:
            break
    returns = returns.iloc[cutoff_indx:]

    # entropy conditions
    n = returns.shape[0] # number of returns in distribution
    num_bin = int(round(np.sqrt(n))) # square root choice for how many bins to split all returns into
    bin_width = (returns.iloc[-1] - returns.iloc[0]) / num_bin
    min = round(returns.iloc[0],4)
    summation = 0

    # entropy calculation
    for i in range(0, num_bin+1):
        # mark all returns in current bin
        series = returns.apply(lambda x: True if (min + bin_width * (i+1)) > x >= (min + bin_width * i) else False)
        # count all returns marked
        items_in_bin = len(series[series == True].index)

        if (items_in_bin > 0): #to ignore cases when items_in_bin = 0
            summation = summation + items_in_bin*math.log(items_in_bin / (n * bin_width),2) # shannon formula

    entropy = (1/n)*summation # shannon formula
    return entropy

# This function returns historical probability that our portfolio daily returns are positive.
def gen_pos_returns(returns: pd.DataFrame):
    returns = returns.sort_values()
    array = np.asarray(returns)
    idx = (np.abs(array)).argmin() # index of closest return = 0%
    prob = 1 - (idx)/len(array)  # 1 - probability return is less than 0% = probability returns are greater than 0%
    return prob

# this function returns a fitness score for a particular individual given a chromosome
# and universe that chromosome is from
def gen_fitness_value(chromosome: [int], universe_data: pd.DataFrame):

    # the total universe returns is the average of asset returns, in an equally weighted portfolio
    universe_returns = universe_data.pct_change().dropna(how='all')  # drop all dates that have no data of any asset
    cnt = universe_returns.count(axis='columns')
    universe_total_returns = universe_returns.apply(np.sum, axis=1) / cnt  # average = sum/#assets

    # reduces universe dataframe to a portfolio of assets indicated by the chromosome
    portf_asset_indicies = np.where(np.array(chromosome) == 1)
    universe_assets = np.array(universe_data.columns)
    assets_in_portf = universe_assets[portf_asset_indicies]
    portf_data = universe_data[assets_in_portf]

    # the total portfolio returns is the average of asset returns, in an equally weighted portfolio
    portf_returns = portf_data.pct_change()
    portf_returns = portf_returns.dropna(how='all') # drop all dates that have no data of any asset
    cnt = portf_returns.count(axis='columns')
    portf_total_returns = portf_returns.apply(np.sum, axis=1)/cnt # average = sum/#assets

    # VaR
    VaR = gen_var(portf_total_returns)

    # entropy
    max_entropy = gen_max_entopy(universe_total_returns)
    portf_entropy = gen_entropy(portf_total_returns, VaR)
    entropy = portf_entropy/max_entropy

    # returns
    prob_pos_returns = gen_pos_returns(portf_total_returns)

    # all objectives are in range [0,1] so they have equal weight in fitness function
    # a higher fitness score is more desirable
    fitness_score = VaR + entropy + prob_pos_returns
    return round(fitness_score,5)