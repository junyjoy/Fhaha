# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from fhaa import db


class Doctor(db.Model):
    __tablename__ = 'doctor'
    __table_args__ = (
        db.ForeignKeyConstraint(['sub_id', 'hos_cid', 'ill_pid'], ['hos_sub.sub_id', 'hos_sub.hos_cid', 'hos_sub.ill_pid']),
        db.Index('fk_doctor_hos_sub1_idx', 'sub_id', 'hos_cid', 'ill_pid')
    )

    doc_name = db.Column(db.String(20), nullable=False)
    doc_type = db.Column(db.String(20), nullable=False)
    doc_pid = db.Column(db.String(11), primary_key=True, nullable=False)
    ill_pid = db.Column(db.Integer, primary_key=True, nullable=False)
    sub_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hos_cid = db.Column(db.String(11), primary_key=True, nullable=False)

    sub = db.relationship('HosSub', primaryjoin='and_(Doctor.sub_id == HosSub.sub_id, Doctor.hos_cid == HosSub.hos_cid, Doctor.ill_pid == HosSub.ill_pid)', backref='doctors')



class HosSub(db.Model):
    __tablename__ = 'hos_sub'

    sub_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hos_cid = db.Column(db.ForeignKey('hospital.hos_cid'), primary_key=True, nullable=False, index=True)
    ill_pid = db.Column(db.ForeignKey('subject.ill_pid'), primary_key=True, nullable=False, index=True)

    hospital = db.relationship('Hospital', primaryjoin='HosSub.hos_cid == Hospital.hos_cid', backref='hos_subs')
    subject = db.relationship('Subject', primaryjoin='HosSub.ill_pid == Subject.ill_pid', backref='hos_subs')



class Hospital(db.Model):
    __tablename__ = 'hospital'

    hos_name = db.Column(db.String(20), nullable=False)
    hos_tel = db.Column(db.String(12), nullable=False)
    hos_addr = db.Column(db.String(80), nullable=False)
    hos_cid = db.Column(db.String(11), primary_key=True)
    hos_pwd = db.Column(db.String(102), nullable=False)
    hos_type = db.Column(db.String(20), nullable=False)



class Matching(db.Model):
    __tablename__ = 'matching'
    __table_args__ = (
        db.ForeignKeyConstraint(['req_rid', 'pat_ema'], ['request.req_rid', 'request.pat_ema']),
        db.Index('fk_matching_request1_idx', 'req_rid', 'pat_ema')
    )

    mat_id = db.Column(db.Integer, primary_key=True, nullable=False)
    req_rid = db.Column(db.Integer, primary_key=True, nullable=False)
    pat_ema = db.Column(db.String(30), primary_key=True, nullable=False)
    hos_cid = db.Column(db.ForeignKey('hospital.hos_cid'), primary_key=True, nullable=False, index=True)

    hospital = db.relationship('Hospital', primaryjoin='Matching.hos_cid == Hospital.hos_cid', backref='matchings')
    request = db.relationship('Request', primaryjoin='and_(Matching.req_rid == Request.req_rid, Matching.pat_ema == Request.pat_ema)', backref='matchings')



class Request(db.Model):
    __tablename__ = 'request'

    req_type = db.Column(db.String(20), nullable=False)
    req_loc = db.Column(db.String(80), nullable=False)
    req_time = db.Column(db.String(20), nullable=False)
    req_req = db.Column(db.String(200), nullable=False)
    req_rid = db.Column(db.Integer, primary_key=True, nullable=False)
    pat_ema = db.Column(db.ForeignKey('user.pat_ema'), primary_key=True, nullable=False, index=True)

    user = db.relationship('User', primaryjoin='Request.pat_ema == User.pat_ema', backref='requests')



class Subject(db.Model):
    __tablename__ = 'subject'
    
    ill_pid = db.Column(db.Integer, primary_key=True, nullable=False)
    ill_name = db.Column(db.String(40), nullable=False)
    ill_sym = db.Column(db.String(100), nullable=False)
    ill_type = db.Column(db.String(20), nullable=False)
    
    
def get_subjects():
    return [(x.ill_pid, x.ill_type) for x in Subject.query.all()]



class User(db.Model):
    __tablename__ = 'user'

    pat_name = db.Column(db.String(10), nullable=False)
    pat_bir = db.Column(db.Date, nullable=False)
    pat_ema = db.Column(db.String(30), primary_key=True)
    pat_pw = db.Column(db.String(102), nullable=False)
    pat_tel = db.Column(db.String(11), nullable=False)
