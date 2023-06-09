"""
Forms 
Authors: jlee (junlee9834@gmail.com)
"""

from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, TextAreaField, PasswordField, EmailField, DateField
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
    email = EmailField('이메일', validators=[DataRequired(), Email('이메일 형식으로 입력하세요.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired()])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired(), EqualTo('password1', '비밀번호가 일치하지 않습니다.')])
    name = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=20)])
    birth = DateField('생년월일', default=date.today(), format='%Y%m%d', validators=[DataRequired()])    
    phone = StringField('연락처', validators=[DataRequired(), Length(min=11, max=11)])    
    
    
    
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
    crn = StringField('사업자등록번호', validators=[DataRequired(), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    name = StringField('병원명', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('병원 주소', validators=[DataRequired(), Length(min=2, max=100)])
    tel = StringField('전화번호', validators=[DataRequired(), Length(min=9, max=11)])
    