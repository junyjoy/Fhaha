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