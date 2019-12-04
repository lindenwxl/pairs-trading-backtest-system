from historic_data import HistoricData

class Candles:
    @classmethod
    def get_all(self, block_size, time_frame, years_to_gather=2):
        return HistoricData(block_size, time_frame, years_to_gather).gather()

    @classmethod
    def get_subset(self, start, end, candles):
        subset = {}

        for asset, candle in candles.items():
            subset[asset] = candle[start:end]

        return subset
