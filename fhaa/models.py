"""
Models for Database 
Authors: jlee (junlee9834@gmail.com)
"""

from fhaa import db

class User(db.Model):
    """환자 테이블  \n
    Variables: \n
        `pat_ema`: 이메일 (PK) \n
        `pat_name`: 환자 이름 \n
        `pat_pw`: 비밀번호 \n
        `pat_tel`: 핸드폰 \n
        `pat_bir`: 생년월일 \n
        
    Authors: jlee (junlee9834@gmail.com)         
    """
    pat_ema = db.Column(db.String(), primary_key=True) 
    pat_name = db.Column(db.String(), unique=True, nullable=False) 
    pat_pw = db.Column(db.String(), nullable=False)
    pat_tel = db.Column(db.String(), nullable=False)
    pat_bir = db.Column(db.Date(), nullable=False)
        
class Hospital(db.Model):
    """병원 테이블
    Variables: \n
        `hos_cid`: 사업자등록번호 (PK) \n
        `hos_pw`: 비밀번호 \n
        `hos_type`: 의료종목 \n
        `hos_name`: 병원명 \n
        `hos_addr`: 병원주소 \n
        `hos_tel`: 전화번호 \n
        
    Authors: jlee (junlee9834@gmail.com) 
    """
    hos_cid = db.Column(db.String(), primary_key=True) 
    hos_pw = db.Column(db.String(), nullable=False)
    hos_type = db.Column(db.String(), nullable=False) 
    hos_name = db.Column(db.String(), nullable=False)
    hos_addr = db.Column(db.String(), nullable=False)
    hos_tel = db.Column(db.String(), nullable=False) 