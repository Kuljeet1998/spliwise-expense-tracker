from datetime import datetime

def convert_date(date):
    datetime_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    converted_date = datetime_object.strftime("%m/%d/%Y")
    return converted_date