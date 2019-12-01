import json
import helpers
import os
from profit_calculator import ProfitCalculator as pc

class Log:
    def __init__(self, time_frame, z_in, z_out, analysis_size):
        self.time_frame = time_frame
        self.z_in = z_in
        self.z_out = z_out
        self.analysis_size = analysis_size

        if os.path.isfile(self.name()):
            raise Exception('The log already exists')
        else:
            self.create()

    def create(self):
        with open(self.name(), mode='w') as f:
            json.dump([], f)

    def append(self, wallet, order_count, exchange_rates):
        with open(self.name(), mode='r') as f:
            log_entries = json.load(f)

            log_data = {
                'wallet_value_btc': pc.wallet_value_btc(wallet, exchange_rates),
                'change_in_btc_volume': pc.change_in_btc_volume(wallet, exchange_rates),
                'change_in_btc_volume_pct': pc.change_in_btc_volume_pct(wallet, exchange_rates),
                'avg_btc_change_as_pct_of_order_value': pc.avg_btc_change_as_pct_of_order_value(wallet, exchange_rates, order_count),
                'rolling_profit': wallet.rolling_profit,
                'order_count': order_count
            }
            log_entries.append(log_data)

        with open(self.name(), mode='w') as f:
            json.dump(log_entries, f)

    def name(self):
        return 'logs/log_'+self.time_frame+'_'+str(self.z_in)+'_'+str(self.z_out)+'_'+str(self.analysis_size)+'.json'

    def length(self):
        with open(self.name(), mode='r') as f:
            log_entries = json.load(f)
            return len(log_entries)

    def remove(self):
        if os.path.exists(self.name()):
            os.remove(self.name())
