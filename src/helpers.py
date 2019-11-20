from assets import active as assets
import json

def get_possible_pairs():
    pairs = []
    for asset_A in assets:
        for asset_B in assets:
            if (asset_A != asset_B
                and not asset_in_list(asset_A, asset_B, pairs)):
                pairs.append([asset_A, asset_B])
    return pairs

def asset_in_list(asset_A, asset_B, possible_pairs):
    return [asset_A, asset_B] in possible_pairs

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
