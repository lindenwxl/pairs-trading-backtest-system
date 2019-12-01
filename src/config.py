import scipy.stats as st
from assets import active as assets

acceptable_coint_threshold = 0.25
min_spread = 0.03
btc_order_volume = 0.00015
max_concurrent_asset_involvement = 3.0
setup_purchase_value = max_concurrent_asset_involvement * btc_order_volume
starting_wallet_balance_btc = (len(assets) * setup_purchase_value) * 2.0

def z_signal_in(val=0.00006):
    return st.norm.ppf(1 - val / 2)

def z_signal_out(val=0.325):
    return st.norm.ppf(1 - val / 2)
