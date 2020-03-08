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
#n= np.random.randint(2, size=(20,4))
#for i in n:
#    print(i)
#    print(gen_fitness_value(i, data))

####   for testing monte carlo simulations  #####
#period = 10  # in days
#n_inc = 10    # granularity higher number is more smooth
#n_sims = 5   # number of simulations
#df = monte_carlo(period,n_inc,n_sims,'GBM', data, ['NKTR', 'CSRA'])
#print(df)

####  for testing genetic algorithm  ####
#universe = ReadUniverse()
#print(universe.count)
#filtered_universe = filter_universe(universe)
#print(universe.count)
#portf = generate_portfolio(filtered_universe, 10000, 1)
#print(portf)

### for testing RabbitMQ ####
# self trigger a request to Portfolio Generator
rabbitmq = rabbitMqProducer('PortfGen', "localhost", "PortfGen","")
pm_msg = PGMessage(PGMessageType.Generate)
rabbitmq.publish(pm_msg.to_json())

# Portfolio generator waiting for requests
server = rabbitMqConsumer('PortfGen', "localhost")
server.startserver()
