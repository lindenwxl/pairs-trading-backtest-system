from assets import active as assets
import json

def order_already_open(pair, current_orders):
    for order in current_orders:
        if order.pair == pair:
            return True
    return False

def asset_currently_active(current_orders, asset):
    for order in current_orders:
        if order.long_position.asset == asset or order.short_position.asset == asset:
            return True

def reduce_insignificant_amounts(wallet, current_orders, exchange_rates):
    for asset, volume in wallet.volumes.items():
        if (not asset_currently_active(current_orders, asset+'BTC')) and (not asset == 'BTC'):
            if not volume == wallet.starting_volumes[asset]:
                wallet.volumes[asset] = wallet.starting_volumes[asset]
