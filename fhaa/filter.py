# UnicodeEncodeError 오류가 발생 시 주석해제
# import locale
# locale.setlocale(locale.LC_ALL, '')


import datetime
from fhaa.libs.gps import get_location, compare

def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M 까지'):
    return value.strftime(fmt)

def add_datetime(args):
    req_date = args['req_date']
    req_time = datetime.timedelta(minutes=int(args['req_time']))
    return req_date+req_time    

def get_distance(args):
    loc = args['loc']
    lat = args['hos_lat']
    lnt = args['hos_lnt']
    result = compare(get_location(loc), (lat, lnt))
    print(result)
    

# args = {
#     'loc': "서울 성동구 아차산로 2-1",
#     'lat': 37.547,
#     'lnt': 127.049
# }
# get_distance(args)