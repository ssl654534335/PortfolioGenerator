#imports
from Library.RiskCalc import *
from Library.ReadUniverse import *
from Library.FilterUniverse import *
from Library.GeneratePortfolio import generate_portfolio
import os

#AKM = Asset(ticker='AKAM', name='Akamai Technologies Inc', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/AKAM.csv',last_price=0)
#CSRA = Asset(ticker='CSRA', name='CSRA Inc.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/CSRA.csv',last_price=0)
#MCHP = Asset(ticker='MCHP', name='Microchip Technology', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/MCHP.csv',last_price=0)
#NKTR = Asset(ticker='NKTR', name='Nektar Therapeutics', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NKTR.csv',last_price=0)
#Asset(ticker='NFLX', name='Netflix Inc.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NFLX.csv'),
#Asset(ticker='NRG', name='NRG Energy', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NRG.csv'),
#Asset(ticker='PCG', name='PG&E Corp.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/PCG.csv'),
#Asset(ticker='STX', name='Seagate Technology', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/STX.csv'),
#Asset(ticker='XL', name='XL Capital', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/XL.csv')]
#data = gen_universe_hist_data([AKM,CSRA,MCHP,NKTR],"Adj. Close")
#n= np.random.dirichlet(np.ones(4),size=20)
#for i in n:
#   print(gen_fitness_value(i, data))

#example
universe = ReadUniverse()
print(universe.count)
filtered_universe = filter_universe(universe)
print(filtered_universe.universe_set)
portf = generate_portfolio(filtered_universe, 10000, 1)
print(portf)