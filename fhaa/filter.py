# UnicodeEncodeError 오류가 발생 시 주석해제
# import locale
# locale.setlocale(locale.LC_ALL, '')
import datetime

def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M 까지'):
    return value.strftime(fmt)

def add_datetime(args):
    req_date = args['req_date']
    req_time = datetime.timedelta(minutes=int(args['req_time']))
    return req_date+req_time    
