from fhaa import db

class User(db.Model):
    """환자 테이블  \n
    Variables: \n
        `email`: 이메일 (PK) \n
        `username`: 이름 \n
        `password`: 비밀번호 \n
        `phone`: 핸드폰 \n
        `birth`: 생년월일 \n
    """
    email = db.Column(db.String(), primary_key=True) # 이메일 (PK)    
    username = db.Column(db.String(), unique=True, nullable=False) # 이름
    password = db.Column(db.String(), nullable=False) # 비밀번호
    phone = db.Column(db.String(12), nullable=False) # 핸드폰
    birth = db.Column(db.Date(), nullable=False) # 생년월일
        
class Hospital(db.Model):
    """병원 테이블
    """
    crn = db.Column(db.String(), primary_key=True) # 사업자등록번호
    pwd = db.Column(db.String(), nullable=False) # 비밀번호
    dept = db.Column(db.String(), nullable=False) # 의료종목
    name = db.Column(db.String(), nullable=False) # 병원명
    addr = db.Column(db.String(), nullable=False) # 병원주소
    tel = db.Column(db.String(12), nullable=False) # 전화번호