from config import z_signal_in, z_signal_out
from helpers import asset_currently_active
import config

class PositionRules:
    @classmethod
    def close_for_profit_loss(self, cp, order, z_out):
        short_asset = order.short_position.asset
        long_asset = order.long_position.asset

        return ((cp.asset_B() == short_asset
                and (cp.z_score() >= -config.z_signal_out(z_out)).bool())
                or (cp.asset_B() == long_asset
                and (cp.z_score() <= config.z_signal_out(z_out)).bool()))

    @classmethod
    def short_A_long_B(self, cp, current_orders, z_in):
        return ((not asset_currently_active(current_orders, cp.asset_B()))
                and (cp.z_score() > config.z_signal_in(z_in)).bool())

    @classmethod
    def short_B_long_A(self,cp, current_orders, z_in):
        return ((not asset_currently_active(current_orders, cp.asset_B()))
                and (cp.z_score() < -config.z_signal_in(z_in)).bool())
