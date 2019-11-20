class CurrencyConvertor:
    @classmethod
    def btc_vol_to_asset_vol(self, btc_vol, exchange_rate):
        return btc_vol * (1/exchange_rate)

    @classmethod
    def asset_vol_to_btc_vol(self, asset_vol, exchange_rate):
        return asset_vol*exchange_rate
