askNotificationPermission();

function makeNoti() {
  // 사용자 응답에 따라 단추를 보이거나 숨기도록 설정
  if (Notification.permission === "denied" || Notification.permission === "default") {
    alert("알림이 차단된 상태입니다. 알림 권한을 허용해주세요.");
  } else {

    let notification = new Notification("test", { // "test" => 제목
      body: "웹 알림 입니다.", // 메세지
      icon: `/lib/img/novalogo_copy.png`, // 아이콘
    });

    //알림 클릭 시 이벤트
    notification.addEventListener("click", () => {
      window.open('https://www.naver.com/');
    });

  }
}

function askNotificationPermission() {
  console.log("권한 묻기");
  // 권한을 실제로 요구하는 함수
  function handlePermission(permission) {
    // 사용자의 응답에 관계 없이 크롬이 정보를 저장할 수 있도록 함
    if (!("permission" in Notification)) {
      Notification.permission = permission;
    }
  }

  // 브라우저가 알림을 지원하는지 확인
  if (!("Notification" in window)) {
    console.log("이 브라우저는 알림을 지원하지 않습니다.");
  } else {
    if (checkNotificationPromise()) {
      Notification.requestPermission().then((permission) => {
        handlePermission(permission);
      });
    } else {
      Notification.requestPermission(function (permission) {
        handlePermission(permission);
      });
    }
  }
}

function checkNotificationPromise() {
  try {
    Notification.requestPermission().then();
  } catch (e) {
    return false;
  }

  return true;
}