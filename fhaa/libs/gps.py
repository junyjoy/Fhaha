"""위치 관련 함수

Authors: jlee (junlee9834@gmail.com)
"""
from haversine import haversine
from geopy.geocoders import Nominatim
import json, requests
import time


def logging_time(original_fn):
    """
    함수의 실행 시간을 측정하여 출력함.
    데코레이터로 사용.

    Examples:
    ```
        @logging_time
        def test():
            time.sleep(2)
    ```
    Print:
        WorkingTime[main]: 2.004459857940674 sec

    Args:
        original_fn (_type_): 함수
    """
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print(
            "WorkingTime[{}]: {} sec".format(
                original_fn.__name__, end_time - start_time
            )
        )
        return result

    return wrapper_fn


def geocoding(address:str):
    """주소를 위경도로 변환
    
    geopy 모듈을 사용하는데 오차가 꽤 큼

    Args:
        address (str): 주소

    Returns:
        tuple: (geo.latitude, geo.longitude)
        
    Authors: jlee (junlee9834@gmail.com)
    """
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    print((geo.latitude, geo.longitude))
    return (geo.latitude, geo.longitude)


def get_location(address:str):
    """주소를 위경도로 변환
    
    카카오 API를 이용함

    Args:
        address (str): 주소

    Returns:
        tuple: (latitude:float, longitude:float)
        
    Authors: jlee (junlee9834@gmail.com)
    """
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
    # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
    headers = {"Authorization": "KakaoAK d3784c7a2755b1198868ce5e7ceb418f"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    address = api_json['documents'][0]['address']
    # crd = {"lat": str(address['y']), "lng": str(address['x'])}
    # address_name = address['address_name']
    # print((float(address['y']), float(address['x'])))

    return (float(address['y']), float(address['x']))


def compare(a_location:tuple, b_location:tuple):
    """a_location과 b_location의 직선 거리를 계산

    Args:
        a_location (tuple): location A (latitude, longitude)
        b_location (tuple): location B (latitude, longitude)

    Returns:
        Any: meter(float)
        
    Authors: jlee (junlee9834@gmail.com)
    """
    # 거리 계산
    result = haversine(a_location, b_location, unit = 'm')
    return result



# r = compare(get_location("서울특별시 강남구 학동로 171"), get_location("서울특별시 강남구 논현로 704"))
# print(f"{r:.2f}",'m')


def read_csv_for_test():
    import csv
    
    retValue = []
    with open('20191128.csv','r') as f:
        rdr = csv.reader(f)
        for line in rdr:
            retValue.append({"name":line[1], "address":line[5]})
            
    return retValue
        

@logging_time
def match_hospital(patient_location:tuple, hospitals):
    result = []
    for hospital in hospitals:
        print(f"patient: {patient_location}")
        print(hospital['name'], hospital['address'])
        distance = compare(patient_location, get_location(hospital['address']))
        print(f"distance: {distance}")
        print()
        result.append({hospital['name']:distance})
    return result



# print(read_csv_for_test())  

# hos = match_hospital(
#     get_location("서울특별시 강남구 학동로 171"), 
#     read_csv_for_test()
# )
# print(hos)



# print(get_location("전라북도 익산시 목천로 120 (목천동)"))

# import random

# a = [
#     '서울특별시 성동구 동일로 133 (성수동2가)',
#     '서울특별시 성동구 왕십리로 269 (행당동)',
#     '서울특별시 성동구 천호대로 436, 2~7층 (용답동)',
#     '서울특별시 성동구 왕십리로 382 (하왕십리동)',
#     '서울특별시 성동구 자동차시장1길 85, 지하1,지상3~5층 (용답동, JS빌딩)',
#     '서울특별시 성동구 광나루로 243 (송정동)',
#     '서울특별시 성동구 왕십리로 296 (행당동)',
#     '서울특별시 성동구 동일로 93 (성수동2가)',
#     '서울특별시 성동구 마장로 207 (홍익동)',
#     '서울특별시 성동구 무학로2길 8 (도선동)',
#     '서울특별시 성동구 왕십리로 222-1 (사근동)',
#     '서울특별시 성동구 독서당로 302, 3층 (금호동4가)',
#     '서울특별시 성동구 고산자로 234, 5층 2호 (행당동)',
#     '서울특별시 성동구 왕십리로 331, 공영빌딩 2층 (하왕십리동)',
#     '서울특별시 성동구 왕십리로 410, 상가 L동 1층 132호 (하왕십리동, 센트라스)',
#     '서울특별시 성동구 독서당로 302, 3층 01호 (금호동4가)',
#     '서울특별시 성동구 금호산길 71, 2층 (금호동2가)',
#     '서울특별시 성동구 아차산로 92, S TOWER 201호 (성수동2가)',
#     '서울특별시 성동구 독서당로 302, 301호 (금호동4가)',
#     '서울특별시 성동구 독서당로 302, 3층 12호 (금호동4가)',
#     '서울특별시 성동구 마장로 137, 221동 2층 2120,2121호 (상왕십리동, 텐즈힐)',
#     '서울특별시 성동구 독서당로 302, 대도빌딩 311호 (금호동4가)',
#     '서울특별시 성동구 독서당로 434, 대림종합상가 2층 212호 (응봉동)',
#     '서울특별시 성동구 성수이로 119, 덕산빌딩 2층 (성수동2가)',
#     '서울특별시 성동구 아차산로 126, 더리브 세종타워 203호 (성수동2가)',
#     '서울특별시 성동구 천호대로 308, 인암빌딩 3층 (용답동)',
#     '서울특별시 성동구 아차산로 41, 안동빌딩 2층 (성수동1가)',
#     '서울특별시 성동구 독서당로 202, 2층 (옥수동)',
#     '서울특별시 성동구 왕십리로 315, 한동타워 9층 (행당동)',
#     '서울특별시 성동구 행당로 84, 행당 한진타운 종합상가 314호 (행당동)',
#     '서울특별시 성동구 왕십리로 363-1, 2층 (하왕십리동)',
#     '서울특별시 성동구 고산자로 207, 3층 (행당동)',
#     '서울특별시 성동구 독서당로 202, 3층 (옥수동)',
#     '서울특별시 성동구 독서당로 290, 1층일부,2,3층 (금호동4가)',
#     '서울특별시 성동구 아차산로 49, 서울숲 코오롱디지털타워 Ⅲ 2층 204호 (성수동1가)',
#     '서울특별시 성동구 아차산로 120, 베델 플레이스 8층 (성수동2가)',
#     '서울특별시 성동구 독서당로 223, 래미안 옥수 리버젠 상가 지하3층 309,310,311호 (옥수동)',
#     '서울특별시 성동구 독서당로40길 39, 옥수 어울림 109,110호 (옥수동)',
#     '서울특별시 성동구 매봉길 48, 201,202호 (옥수동)',
#     '서울특별시 성동구 금호로 105, 래미안하이리버 상가동 B306호 (금호동2가)',
#     '서울특별시 성동구 성수일로6길 53, 유원지식산업센터 2층 (성수동2가)',
#     '서울특별시 성동구 왕십리로 50, 지하1층 (성수동1가)',
#     '서울특별시 성동구 매봉길 50, 2층 204.205.206호 (옥수동, 이편한세상옥수파크힐스)',
#     '서울특별시 성동구 왕십리로 326, 3층 (도선동)',
#     '서울특별시 성동구 상원1길 26, 서울숲A타워 214,215호 (성수동1가)',
#     '서울특별시 성동구 왕십리로 350, 7층 (도선동)',
#     '서울특별시 성동구 아차산로 92, 3,5층 (성수동2가)',
#     '서울특별시 성동구 왕십리로 350, BM빌딩 301호 (도선동)',
#     '서울특별시 성동구 성수이로 113, 제강빌딩 6층 (성수동2가)'
# ]

# from werkzeug.security import generate_password_hash

# with open("insert_hospital.sql", "a", encoding="utf-8") as f:
#     for x in enumerate(a):
#         addr = x[1].split(", ")[0].split(" (")[0]
        
#         cid = str(int(random.random() * 10000000000))
#         tel = '02'+str(int(random.random() * 10000000))
#         lat, lnt = get_location(addr)
#         pwd = generate_password_hash("testtest")
#         query = f"INSERT INTO fhaa.hospital(hos_cid, hos_name, hos_tel, hos_addr1, hos_pwd, hos_type, hos_lat, hos_lnt) VALUES('{cid}', '나보다정형외과{x[0]}', '{tel}', '{addr}', '{pwd}', '', {lat}, {lnt});"
#         f.write(query+"\n")
    
#         for y in range(25, 34):
#             query2 = f"INSERT INTO fhaa.hos_sub(hos_cid, ill_pid) VALUES('{cid}', '{y}');"
#             f.write(query2+"\n")
        