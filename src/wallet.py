from custom_exceptions import NotEnoughFundsException
import helpers
import config
from exchange_rates import ExchangeRates
from currency_convertor import CurrencyConvertor

class Wallet:
    def __init__(self, exchange_rates):
        self.volumes = { 'BTC': config.starting_wallet_balance_btc }

        for asset, exchange_rate in exchange_rates.items():
            if not asset[:3] == 'BTC':
                self.volumes[asset[:3]] = CurrencyConvertor.btc_vol_to_asset_vol(
                    config.setup_purchase_value,
                    exchange_rate
                )
                self.volumes['BTC'] -= config.setup_purchase_value

        self.starting_btc_volume = self.volumes['BTC']
        self.starting_volumes = self.volumes.copy()
        self.rolling_profit = 0

    def buy(self, asset, exchange_rate, asset_volume):
        btc_volume = CurrencyConvertor.asset_vol_to_btc_vol(
            asset_volume,
            exchange_rate
        )

        self.volumes['BTC'] -= btc_volume
        self.volumes[asset] += asset_volume

        self.apply_market_charges(btc_volume)

        return asset_volume

    def sell(self, asset, exchange_rate, asset_volume):
        btc_volume = CurrencyConvertor.asset_vol_to_btc_vol(
            asset_volume,
            exchange_rate
        )

        self.volumes[asset] -= asset_volume
        self.volumes['BTC'] += btc_volume

        self.apply_market_charges(btc_volume)

        return asset_volume

    def apply_market_charges(self, btc_volume):
        self.volumes['BTC'] -= (0.26 * btc_volume)/100.0

    def current_btc_volume(self):
        return self.volumes['BTC']
