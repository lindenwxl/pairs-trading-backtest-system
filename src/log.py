import json
import helpers
import os

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

    def append(self):
        with open(self.name(), mode='r') as f:
            log_entries = json.load(f)

            log_data = {}
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
