from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, TextAreaField, PasswordField, EmailField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    """환자 회원가입 폼 \n
    `email` : email, pk \n
    `password1` : password \n
    `password2` : verify password \n
    `nickname` : nickname \n
    `birth` : birthday \n
    `phone` : phone number \n
    """
    email = EmailField('이메일', validators=[DataRequired(), Email('이메일 형식으로 입력하세요.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    nickname = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    birth = DateField('생년월일', validators=[DataRequired(), Length(min=8, max=8)])    
    phone = StringField('연락처', validators=[DataRequired(), Length(min=11, max=12)])    
    
    
    
class HospitalCreateForm(FlaskForm):
    """환자 회원가입 폼 \n
    `crn` : Company Registration Number, pk \n
    `nickname` : nickname \n
    `password1` : password \n
    `password2` : verify password \n
    `phone` : phone number
    """
    crn = StringField('사업자등록번호', validators=[DataRequired(), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    name = StringField('병원명', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('병원 주소', validators=[DataRequired(), Length(min=2, max=100)])
    tel = StringField('전화번호', validators=[DataRequired(), Length(min=9, max=11)])
    