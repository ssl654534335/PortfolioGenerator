from platypus import NSGAII, Problem, Integer
from Library.DataClass import *
from Library.RiskCalc import *
from Library.RabbitMQProducer import *

def calc_total_value(universe: Universe, weights: [float]):
    total = 0
    for i in range(universe.count):
        total += universe.universe_set[i].last_price * weights[i]

    return total

class OptPortfolio(Problem):

    def __init__(self, universe: Universe, buying_power: float):
        super(OptPortfolio, self).__init__(universe.count,1,1)
        self.universe = universe
        self.universe_historical_data = gen_universe_hist_data(universe.universe_set, "Adj. Close")
        self.buying_power = buying_power
        self.typeInt = Integer(0,1)
        self.types[:] = self.typeInt
        self.constraints[:] = "==0"
        self.directions[:] = Problem.MAXIMIZE

    def evaluate(self, solution):
        solution.objectives[:] = gen_fitness_value(solution.variables, self.universe_historical_data)
        solution.constraints[0] = sum(solution.variables) - 10
        #solution.constraints[1] = calc_total_value(self.universe, solution.variables) - self.buying_power        

def generate_portfolio(universe: Universe, buying_power: float, user_id: int):
    problem = OptPortfolio(universe,buying_power)
    algorithm = NSGAII(problem)
    algorithm.run(1000)

    feasible_solutions = [s for s in algorithm.result if s.feasible]

    sol = [problem.typeInt.decode(i) for i in feasible_solutions[0].variables]

    print(sol)

    alloc = {}
    assets = []
    for i, asset in enumerate(universe.universe_set):
        if (sol[i] == 1):
            alloc[asset.ticker] = 0.1
            assets.append(asset)

    print(alloc)

    portf = Portfolio(user_id=user_id,buying_power=buying_power,assets=assets,asset_alloc=alloc)

    return portf

### RabbitMQ request to generate portfolios and push to Database
def Assets_to_UDMHoldings(portf: Portfolio ):
    UDMholdings = []
    for asset in portf.assets:
        quantity = math.trunc((portf.buying_power * portf.asset_alloc[asset.ticker])/asset.last_price)
        holding = UDMHolding(None,None, asset.name, asset.ticker,'',quantity)
        UDMholdings.append(holding)
    return UDMholdings

def Portfolio_to_UDMPortfolio(portf: Portfolio):
    VaR = -.03  # will be set by var function
    stopValue = portf.buying_power - portf.buying_power * VaR
    holdings = Assets_to_UDMHoldings(portf)
    UDMportf = UDMPortfolio(np.NaN, np.NaN, False, datetime.datetime.today(), portf.buying_power, stopValue, None, holdings)
    return UDMportf

def GeneratePortfs():
    # universe = ReadUniverse()
    # filtered_universe = filter_universe(universe)
    # portf = generate_portfolio(filtered_universe, 10000, 1)

    # sample output from genetic algo
    portf = Portfolio(user_id=1, buying_power=10000, assets=[Asset(ticker='AAP', name='Advance Auto Parts', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/AAP.csv',
                                                           last_price=115.01),
                                                     Asset(ticker='CXO', name='Concho Resources', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/CXO.csv',
                                                           last_price=157.0),
                                                     Asset(ticker='COP', name='ConocoPhillips', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/COP.csv',
                                                           last_price=59.14),
                                                     Asset(ticker='CSRA', name='CSRA Inc.', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/CSRA.csv',
                                                           last_price=41.33),
                                                     Asset(ticker='HES', name='Hess Corporation', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/HES.csv',
                                                           last_price=49.87),
                                                     Asset(ticker='INTC', name='Intel Corp.', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/INTC.csv',
                                                           last_price=51.19),
                                                     Asset(ticker='NFLX', name='Netflix Inc.', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/NFLX.csv',
                                                           last_price=300.69),
                                                     Asset(ticker='PCG', name='PG&E Corp.', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/PCG.csv',
                                                           last_price=43.94),
                                                     Asset(ticker='SBAC', name='SBA Communications', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/SBAC.csv',
                                                           last_price=170.1),
                                                     Asset(ticker='TDG', name='TransDigm Group', asset_type='stock',
                                                           price_history_file='C:\\Users\\Francisco\\Documents\\AlgoTradingCode\\portfolio_gen\\Stock_Data/TDG.csv',
                                                           last_price=305.14)],
              asset_alloc={'AAP': 0.1, 'CXO': 0.1, 'COP': 0.1, 'CSRA': 0.1, 'HES': 0.1, 'INTC': 0.1, 'NFLX': 0.1,
                           'PCG': 0.1, 'SBAC': 0.1, 'TDG': 0.1})

    UDMportf = Portfolio_to_UDMPortfolio(portf)
    rabbitmq = rabbitMqProducer('UserDB-PortfGen', "localhost", "UserDB-PortfGen", "")
    request_msg = UDMRequest(None, RequestType.Portfolio, Operation.Insert, None, UDMportf, None, None)
    rabbitmq.publish(request_msg.to_json())
    return
