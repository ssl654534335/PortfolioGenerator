#imports
from Library.RiskCalc import *
from Library.ReadUniverse import *
from Library.FilterUniverse import *
from Library.GeneratePortfolio import generate_portfolio
from Library.MonteCarloSim import *
from Library.RabbitMQProducer import *
from Library.RabbitMQConsumer import *
import os

#####  sample universe for testing  ######
#AKM = Asset(ticker='AKAM', name='Akamai Technologies Inc', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/AKAM.csv',last_price=0)
#CSRA = Asset(ticker='CSRA', name='CSRA Inc.', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/CSRA.csv',last_price=0)
#MCHP = Asset(ticker='MCHP', name='Microchip Technology', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/MCHP.csv',last_price=0)
#NKTR = Asset(ticker='NKTR', name='Nektar Therapeutics', asset_type='stock', price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NKTR.csv',last_price=0)
#data = gen_universe_hist_data([AKM,CSRA,MCHP,NKTR],"Adj. Close")

#####  for testing genetic algorithm fitness function  #####
#n= np.random.dirichlet(np.ones(4),size=20)
#for i in n:
#   print(gen_fitness_value(i, data))

####   for testing monte carlo simulations  #####
#period = 10  # in days
#n_inc = 10    # granularity higher number is more smooth
#n_sims = 5   # number of simulations
#df = monte_carlo(period,n_inc,n_sims,'GBM', data, ['NKTR', 'CSRA'])
#print(df)

####  for testing genetic algorithm  ####
universe = ReadUniverse()
print(universe.count)
filtered_universe = filter_universe(universe)
print(filtered_universe.count)
portf = generate_portfolio(filtered_universe, 10000, 1)
print(portf)

### for testing RabbitMQ ####
#rabbitmq = rabbitMqProducer('UserDB-PortfGen', "localhost", "UserDB-PortfGen","")
#h1 = UDMHolding('Nektar Therapeutics','NKTR', '',100)
#h2 = UDMHolding('Microchip Technology','MCHP','', 234)
#sample_portf_msg = UDMPortfolio(1, 101, True, datetime.datetime.today(), 1000, 870.40, .78,[h1,h2])
#rabbitmq.publish(sample_portf_msg.to_json())

#server = rabbitMqConsumer('UserDB-PortfGen', "localhost")
#server.startserver()
