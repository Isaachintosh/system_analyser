from datetime import datetime

def odometry_treatment(data, preliminar_result):
    performance_per_minute = sum(preliminar_result)
    performance_per_hour = performance_per_minute * 60
    performance_per_day = performance_per_hour * 24
    
    datetime_now = datetime.now()
    datetime_format = "%Y%m%d%H%M%S"
    datetime_formated = datetime.strftime(datetime_now, datetime_format)
    
    data.update({
        'id': datetime_formated,
        'name': 'CPU Lifetime Report',
        'proccesses_per_hour': performance_per_hour,
        'proccesses_per_day': performance_per_day,
    })