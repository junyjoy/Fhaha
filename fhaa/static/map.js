
// 지도 생성 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 2 // 지도의 확대 레벨 
    }; 

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
var marker;

var location_input = document.getElementById('location');


// 현재 위치 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 지도에 마커를 표시하고 중심좌표를 접속위치로 변경하는 함수입니다
function displayMarker(locPosition) {

    // 마커를 생성합니다
    marker = new kakao.maps.Marker({  
        position: locPosition,
        clickable: true // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
    }); 

    marker.setMap(map);
    get_location();
    
    // 지도 중심좌표를 접속위치로 변경합니다
    map.setCenter(locPosition);      

    
    // locatin input에 표시
    searchDetailAddrFromCoords(locPosition, function (result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var detailAddr = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
            document.getElementById('location').value = detailAddr;
        }
    });
}   

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
if (navigator.geolocation) {
    
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function(position) {
        
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        
        var locPosition = new kakao.maps.LatLng(lat, lon); // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
        
        // 마커와 인포윈도우를 표시합니다
        displayMarker(locPosition);
            
      });
    
} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
    var locPosition = new kakao.maps.LatLng(33.450701, 126.570667);
        
    displayMarker(locPosition);
}


// 마커 생성 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 지도에 마커를 생성하고 지도위에 표시하는 함수입니다
function addMarker(position) {
    marker.setMap(null);
    
    // 마커를 생성합니다
    marker = new kakao.maps.Marker({
        position: position,
        clickable: true // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
    });

    // // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);
    get_location();

    // locatin input에 표시
    searchDetailAddrFromCoords(position, function (result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var detailAddr = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
            document.getElementById('location').value = detailAddr;
        }
    });
}

// 지도를 클릭했을때 클릭한 위치에 마커를 추가하도록 지도에 클릭이벤트를 등록합니다
kakao.maps.event.addListener(map, 'click', function (mouseEvent) {        
    // 클릭한 위치에 마커를 표시합니다 
    addMarker(mouseEvent.latLng);        
});


// 좌표<->주소 변환하여 검색창에 입력 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

// 좌표를 주소로 변환
function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청합니다
    geocoder.coord2Address(coords['La'], coords['Ma'], callback);
}


function setLocation() {
    marker.setMap(null);

    geocoder.addressSearch(document.getElementById('location').value, function(result, status) {

        // 정상적으로 검색이 완료됐으면 
        if (status === kakao.maps.services.Status.OK) {
            // marker.setMap(null);

            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

            // 결과값으로 받은 위치를 마커로 표시합니다
            marker = new kakao.maps.Marker({
                map: map,
                position: coords
            });

            // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
            map.setCenter(coords);
            get_location();
        } 
    });    
}

function get_location() {
    x = document.getElementById('location_lon').value = marker.getPosition()['La'];
    y = document.getElementById('location_lat').value = marker.getPosition()['Ma'];
    return x, y;
}