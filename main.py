#imports
from Library.RiskCalc import *
from Library.ReadUniverse import *
from Library.FilterUniverse import *
import os

AKM = Asset(ticker='AKAM', name='Akamai Technologies Inc', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/AKAM.csv')
CSRA = Asset(ticker='CSRA', name='CSRA Inc.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/CSRA.csv')
MCHP = Asset(ticker='MCHP', name='Microchip Technology', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/MCHP.csv')
NKTR = Asset(ticker='NKTR', name='Nektar Therapeutics', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NKTR.csv')
#Asset(ticker='NFLX', name='Netflix Inc.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NFLX.csv'),
#Asset(ticker='NRG', name='NRG Energy', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NRG.csv'),
#Asset(ticker='PCG', name='PG&E Corp.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/PCG.csv'),
#Asset(ticker='STX', name='Seagate Technology', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/STX.csv'),
#Asset(ticker='XL', name='XL Capital', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/XL.csv')]

print(gen_fitness_value([.6,.4,0,0], [AKM,CSRA,MCHP,NKTR]))
print(gen_fitness_value([.4,.3,.2,.1], [AKM,CSRA,MCHP,NKTR]))
print(gen_fitness_value([.9,.1,.0,.0], [AKM,CSRA,MCHP,NKTR]))

#example
#universe = ReadUniverse()
#print(universe.count)
#filtered_universe = filter_universe(universe)
#print(filtered_universe.universe_set)
#print(filtered_universe[0])
