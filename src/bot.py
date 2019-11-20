import time
import helpers
from wallet import Wallet
import config
from position_rules import PositionRules
from order_builder import OrderBuilder
from exchange_rates import ExchangeRates
from cointegration_analysis import CointegrationAnalysis
from order_remover import OrderRemover
from log import Log
from time_formatter import TimeFormatter
from candles import Candles

class Bot:
    def __init__(
        self,
        time_frame,
        block_size,
        z_in_val,
        z_out_val,
        analysis_size,
        candles
    ):
        self.set_initial_values(
            time_frame,
            block_size,
            z_in_val,
            z_out_val,
            analysis_size
        )
        self.time_formatter = TimeFormatter(4)
        self.backtesting_candles = candles
        self.possible_pairs = helpers.get_possible_pairs()
        self.generate_log()
        self.run_test()

    def run_test(self):
        while True:
            try:
                self.prepare_pass()
                self.make_pass()
                # self.log_pass()

                self.start_candle += 1
                self.current_step += 1
            except:
                break

    def log_pass(self):
        self.log.append()

    def make_pass(self):
        self.detect_cointegrated_pairs()
        self.remove_existing_orders()
        self.place_new_orders()
        helpers.reduce_insignificant_amounts(
            self.wallet,
            self.current_orders,
            self.exchange_rates
        )

    def place_new_orders(self):
        for cp in self.cointegrated_pairs:
            if helpers.order_already_open(cp.pair, self.current_orders):
                continue
            elif (abs(cp.current_spread()) > config.min_spread).bool():
                ob = OrderBuilder(cp, self.wallet)

                if PositionRules.short_A_long_B(cp, self.current_orders, self.z_in_val):
                    short, long = ob.short_A_long_B()
                    ob.place(short, long, self.current_orders)
                    self.order_count += 1
                if PositionRules.short_B_long_A(cp, self.current_orders, self.z_in_val):
                    short, long = ob.short_B_long_A()
                    ob.place(short, long, self.current_orders)
                    self.order_count += 1

    def remove_existing_orders(self):
        order_remover = OrderRemover(
            self.wallet,
            self.exchange_rates,
            self.cointegrated_pairs
        )
        self.current_orders = order_remover.for_non_cointegration(
            self.current_orders
        )
        self.current_orders = order_remover.for_profit_loss(
            self.z_out_val,
            self.current_orders
        )

    def detect_cointegrated_pairs(self):
        for pair in self.possible_pairs:
            coint_analysis = CointegrationAnalysis(
                pair,
                self.exchange_rates,
                self.candles
            )
            if (coint_analysis.asset_lengths_equal()
                and coint_analysis.suitably_cointegrated()):
                self.cointegrated_pairs.append(
                    coint_analysis.generate_cointegrated_pair()
                )

    def prepare_pass(self):
        self.display_elapsed_time()
        self.end_candle = self.start_candle + self.analysis_size
        self.cointegrated_pairs = []
        self.candles = Candles.get_subset(self.start_candle, self.end_candle, self.backtesting_candles)
        self.exchange_rates = ExchangeRates.from_candles(self.candles)
        if self.current_step == 0:
            self.wallet = Wallet(self.exchange_rates)

    def display_elapsed_time(self):
        print 'starting pass at: ', self.time_formatter.display(
            self.current_step*60*60*self.block_size
        )

    def set_initial_values(
        self,
        time_frame,
        block_size,
        z_in_val,
        z_out_val,
        analysis_size
    ):
        self.time_frame = time_frame
        self.block_size = block_size
        self.z_in_val = z_in_val
        self.z_out_val = z_out_val
        self.analysis_size = analysis_size
        self.current_step = 0
        self.wallet = None
        self.start_candle = 0
        self.current_orders = []
        self.order_count = 0

    def generate_log(self):
        self.log = Log(
            self.time_frame,
            self.z_in_val,
            self.z_out_val,
            self.analysis_size
        )
