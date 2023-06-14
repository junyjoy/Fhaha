from haversine import haversine
from geopy.geocoders import Nominatim
import json, requests


def geocoding(address:str):
    """주소를 위경도로 변환

    Args:
        address (str): 주소

    Returns:
        tuple: (geo.latitude, geo.longitude)
    """
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    print((geo.latitude, geo.longitude))
    return (geo.latitude, geo.longitude)


def get_location(address:str):
    """주소를 위경도로 변환

    Args:
        address (str): 주소

    Returns:
        tuple: (latitude:float, longitude:float)
    """
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
    # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
    headers = {"Authorization": "KakaoAK d3784c7a2755b1198868ce5e7ceb418f"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    address = api_json['documents'][0]['address']
#   crd = {"lat": str(address['y']), "lng": str(address['x'])}
#   address_name = address['address_name']
    print((float(address['y']), float(address['x'])))

    return (float(address['y']), float(address['x']))




def compare(a_location:tuple, b_location:tuple):
    """a_location과 b_location의 직선 거리를 계산

    Args:
        a_location (tuple): location A (latitude, longitude)
        b_location (tuple): location B (latitude, longitude)

    Returns:
        Any: _description_
    """
    # 거리 계산
    result = haversine(a_location, b_location, unit = 'm')
    return result

r = compare(get_location("서울특별시 강남구 학동로 171"), get_location("서울특별시 강남구 논현로 704"))
print(r,'m')
