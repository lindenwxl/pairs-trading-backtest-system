class TimeFormatter:
    def __init__(self, granularity):
        self.granularity = granularity

    def display(self, seconds):
        result = []

        for name, count in self.intervals():
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:self.granularity])

    def intervals(self):
        return (
            ('weeks', 604800),
            ('days', 86400),
            ('hours', 3600),
            ('minutes', 60),
            ('seconds', 1),
        )
