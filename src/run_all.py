from bot import Bot
import numpy
from multiprocessing import Pool, cpu_count
from candles import Candles
import os
import re
import subprocess
import cpu_count

def run_pass(args_dict):
    Bot(
        args_dict['time_frame'],
        args_dict['block_size'],
        args_dict['z_in'],
        args_dict['z_out'],
        args_dict['analysis_size'],
        args_dict['candles']
    )

if __name__ == '__main__':
    block_sizes_hours = {
        '7D': 168.0,
        '1D': 24.0,
        '12h': 12.0,
        '6h': 6.0,
        '3h': 3.0,
        '1h': 1.0,
        '30m': 0.5,
        '15m': 0.25,
        '5m': 0.08333333333333333,
        '1m': 0.01666666666666666
    }
    minute_intervals = {
        '7D': 60*24*7,
        '1D': 60*24,
        '12h': 60*12,
        '6h': 60*6,
        '3h': 60*3,
        '1h': 60,
        '30m':30,
        '15m': 15,
        '5m': 5,
        '1m': 1
    }

    z_in_vals = numpy.arange(0.00005, 0.00015, 0.00002)
    z_out_vals = numpy.arange(0.35, 0.8, 0.02)
    analysis_sizes = range(72, 2000, 100)

    args_list = []
    current_time_frame = ''

    minute_candles = Candles.get_all(
        block_sizes_hours['1m'],
        '1m',
        2
    )

    for time_frame, block_size in block_sizes_hours.items():
        for z_in in z_in_vals:
            for z_out in z_out_vals:
                for analysis_size in analysis_sizes:
                    candles = minute_candles[::minute_intervals[time_frame]]

                    args_dict = {
                        'time_frame': time_frame,
                        'block_size': block_size,
                        'z_in': z_in,
                        'z_out': z_out,
                        'analysis_size': analysis_size,
                        'candles': candles
                    }
                    args_list.append(args_dict)


    pool = Pool(cpu_count.num_available())
    pool.map(run_pass, args_list)
