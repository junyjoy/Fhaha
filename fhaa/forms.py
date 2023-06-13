"""
Forms 
Authors: jlee (junlee9834@gmail.com)
"""

from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, TextAreaField, PasswordField, EmailField, DateField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, Email, StopValidation
import  wtforms.validators as test
from wtforms import widgets
from flask import g


from datetime import date

from fhaa import db
from fhaa.models import Subject


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
    birth = DateField('생년월일', default='', format='%Y%m%d', validators=[DataRequired('값이 비었습니다.')])    
    phone = StringField('연락처', validators=[DataRequired('값이 비었습니다.'), Length(min=11, max=11)])    
    

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        print(field.data)
        
        if len(field.data) == 0:
            raise StopValidation(self.message)
    
    
class HospitalCreateForm(FlaskForm):
    """병원 회원가입 폼 \n
    Field:
        `crn` : Company Registration Number, pk \n
        `password1` : password \n
        `password2` : verify password \n
        `name` : hospital name \n
        `address1` : hospital address \n
        `address2` : hospital address \n
        `tel` : telephone number \n
        `type` : NULL \n
    Authors: jlee (junlee9834@gmail.com)             
    """
        
    crn = StringField('ID(사업자등록번호)', validators=[DataRequired('값이 비었습니다.'), Length(min=10, max=10, message='사업자등록번호는 10자 입니다.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired('값이 비었습니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('값이 비었습니다.')])
    name = StringField('병원명', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=100)])
    address1 = StringField('병원 주소', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=100)])
    address2 = StringField('병원 상세주소', validators=[DataRequired('값이 비었습니다.'), Length(min=2, max=100)])
    tel = StringField('전화번호', validators=[DataRequired('값이 비었습니다.'), Length(min=9, max=11)])

    type = StringField('', default='')
    
    subject = MultiCheckboxField('진료과목', choices=[(x.ill_pid, x.ill_type) for x in Subject.query.all()], validators=[MultiCheckboxAtLeastOne()], coerce=int)
    

class UserLoginForm(FlaskForm):
    email = EmailField('사용자이메일', validators=[DataRequired(), Length(min=9, max=50)])
    password = PasswordField('비밀번호', validators=[DataRequired('값이 비었습니다.'),Length(min=8)])
    

class HospitalLoginForm(FlaskForm):
    crn = StringField('사업자등록번호', validators=[DataRequired(), Length(min=9, max=50)])
    password = PasswordField('비밀번호', validators=[DataRequired('값이 비었습니다.'),Length(min=8)])