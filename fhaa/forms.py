"""
Forms 
Authors: jlee (junlee9834@gmail.com)
"""

from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, TextAreaField, PasswordField, EmailField, DateField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import  wtforms.validators as test

from datetime import date


class UserCreateForm(FlaskForm):
    """환자 회원가입 폼 \n
    Field:
        `email` : email, pk \n
        `password1` : password 
        `password2` : verify password \n
        `name` : name \n
        `birth` : birthday \n
        `phone` : phone number \n
    Authors: jlee (junlee9834@gmail.com)         
    
    """
    email = EmailField('ID(이메일)', validators=[DataRequired('값이 비었습니다.'), Email('이메일 형식으로 입력하세요.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired('값이 비었습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('값이 비었습니다.'), EqualTo('password1', '비밀번호가 일치하지 않습니다.')])
    name = StringField('이름', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=20)])
    birth = DateField('생년월일', default=date.today(), format='%Y%m%d', validators=[DataRequired('값이 비었습니다.')])    
    phone = StringField('연락처', validators=[DataRequired('값이 비었습니다.'), Length(min=11, max=11)])    
    
    
    
class HospitalCreateForm(FlaskForm):
    """환자 회원가입 폼 \n
    Field:
        `crn` : Company Registration Number, pk \n
        `nickname` : nickname \n
        `password1` : password \n
        `password2` : verify password \n
        `phone` : phone number \n
    Authors: jlee (junlee9834@gmail.com)             
    """
    crn = StringField('ID(사업자등록번호)', validators=[DataRequired('값이 비었습니다.'), Length(min=11, max=11)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('값이 비었습니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('값이 비었습니다.')])
    name = StringField('병원명', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=100)])
    address = StringField('병원 주소', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=100)])
    tel = StringField('전화번호', validators=[DataRequired('값이 비었습니다.'), Length(min=9, max=11)])
    hospital_types = ["내과", "피부과", "비뇨의학과", "산부인과", "안과", "정형외과", "이비인후과", "치과"]
    type = SelectField('의료종목', choices = hospital_types, validators=[DataRequired('값이 비었습니다.'), Length(min=1, max=20)])
