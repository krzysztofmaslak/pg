import datetime

__author__ = 'root'

class TimeUtil:
    def unix_time_millis(dt):
        return dt.strftime('%Y%m%d%H%M%S%f')