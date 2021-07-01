from passlib.hash import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, exc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from enum import Enum
import uuid
import secrets

from sqlalchemy.sql.expression import and_, or_

db = SQLAlchemy()



################################# Enum class ###################################################
class StateUser(Enum):
    ACTIVE = True
    INACTIVE = False

class Gender(Enum):
    M = "Male"
    F = "Female"

class RoleUsers(Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"
    ADMINISTRATOR = "Administrator"

class AppointStatus(Enum):
    WAITING = "Waiting"
    COMPLETED = "Completed"
    CANCELED = "Canceled"
    POSTPONED = "Postponed"

class Nationality(Enum):
    FOREIGN = "Foreign"
    RF = "Russia"

################################# Link table global field ######################################
doctor_specialization = db.Table('doctor_specialization',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.doctor_id', 
        name='fk__doctor_id.>>>.doctors.doctor_id', ondelete="CASCADE", onupdate="RESTRICT"), 
        primary_key=True),
    db.Column('spec_id', db.String(14), db.ForeignKey('specializations.spec_id', 
        name='fk__spec_id.>>>.specializations.spec_id',ondelete="RESTRICT", onupdate="RESTRICT"), 
        primary_key=True))
        
favorites_doctors = db.Table('favorites_doctors',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.doctor_id', 
        name='fk__doctor_favor_id.>>>.doctors.doctor_id', ondelete="CASCADE", onupdate="RESTRICT"), 
        primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.patient_id', 
        name='fk__patients_id.>>>.patients.patient_id',ondelete="CASCADE", onupdate="RESTRICT"), 
        primary_key=True))



class AuthenticationData(db.Model):

################################# Class attribute ##############################################
    data_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailadress = db.Column(db.String(100), nullable=False, unique=True)
    __password = db.Column("password", db.String(100), nullable=False)
    __token_save = db.Column("token_save", db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    role_type = db.Column(db.Enum(RoleUsers), nullable=False, default="PATIENT")

################################# Relationship #################################################
    users = db.relationship('User', backref=backref('auth_data', uselist=False))

################################# Table properties #############################################
    __tablename__ = 'authenticate_data'
    __mapper_args__ = {'polymorphic_identity':'authenticate_data'}
    __table_args__ = {'mysql_row_format': 'COMPRESSED'}

################################# Class Methods ################################################
    @classmethod
    def check_token(self, key):
        
        return self.query.filter(self.__token_save == key).one_or_none()
      
    @classmethod
    def authenticate(self, emailadress, password=""):
        user_data = self.query.filter(self.emailadress == emailadress).one_or_none()
        if password and user_data:
            if not bcrypt.verify(password, user_data.__password): raise Exception('Invalid password') 
            else: return user_data      
        elif user_data: raise Exception('User exists') 
        elif password: raise Exception('User not exists')
        return user_data 

################################# Get, Set Methods #############################################
    @property
    def get_token(self)-> str: return self.__token_save

################################# Object Methods ###############################################
    def __init__(self, kwargs) -> None:       
        super().__init__()
        self.emailadress = kwargs.get("emailadress")
        self.__password = self.__hash_passwoord(kwargs.get("password"))
        self.__token_save = self.__generation_token()


    def __hash_passwoord(self, password) -> str: return bcrypt.using(rounds=6).hash(password)


    def __generation_token (self): return uuid.UUID(bytes=secrets.token_bytes(16)).hex


class User(AuthenticationData):

################################# ForeignKey ##################################################
    user_data_id = db.Column(db.Integer, db.ForeignKey(
        'authenticate_data.data_id', name="fk__users.user_data_id_>>>_authenticate_data.data_id", 
        ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)   

################################# Class attribute ############################################## 
    gender = db.Column(db.Enum(Gender),nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    patname = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)
    profile_pic = db.Column(db.String(50), nullable=True, default="/profile_pic/no_pic.jpg")
    is_state = db.Column(db.Enum(StateUser), nullable=False, default="ACTIVE")

################################# Relationship #################################################
    doctors = db.relationship('Doctor', backref=backref('user_data', uselist=False), 
        foreign_keys="Doctor.doctor_id")
    patients = db.relationship('Patient', backref=backref('user_data', uselist=False), 
        foreign_keys="Patient.patient_id")

################################# Table properties #############################################
    __tablename__ = 'users'   
    __mapper_args__ = {'polymorphic_identity':'users'}
    __table_args__ = (db.Index('firstname_lastname', "firstname", "lastname", unique=False),
        {'mysql_row_format': 'COMPRESSED'}) 

################################# Object Methods ###############################################
    def __init__(self, kwargs) -> None:       
        super().__init__(kwargs.get("auth_data"))
        del kwargs["auth_data"]      
        self.gender = kwargs.get("gender")
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.patname = kwargs.get("patname")
        self.phone_number = kwargs.get("phone_number")
        self.birthday = kwargs.get("birthday")

   
    def _save_user(self) -> None:
        try:
            db.session.add(self)
            db.session.commit() 
        except SQLAlchemyError as err_sql:
            db.session.rollback()
            db.session.close()
            raise err_sql

    
class Shedule(db.Model):

################################# ForeignKey ##################################################
    doctor_id_s = db.Column(
        db.Integer, db.ForeignKey('doctors.doctor_id', name='fk__doctor_id_s.>>>.doctors.doctor_id',
        ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)

################################# Class attribute ##############################################
    monday_start = db.Column(db.Time(), nullable=True)
    monday_end = db.Column(db.Time(), nullable=True)
    tuesday_start = db.Column(db.Time(), nullable=True)
    tuesday_end = db.Column(db.Time(), nullable=True)
    wednesday_start = db.Column(db.Time(), nullable=True)
    wednesday_end = db.Column(db.Time(), nullable=True)
    thursday_start = db.Column(db.Time(), nullable=True)
    thursday_end = db.Column(db.Time(), nullable=True)
    friday_start = db.Column(db.Time(), nullable=True)
    friday_end = db.Column(db.Time(), nullable=True)
    time_step = db.Column(db.SmallInteger, default=30)

################################# Table properties #############################################
    __tablename__ = "shedules"
    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'shedules'}
    
################################# Object Methods ###############################################
    def __init__(self, kwargs) -> None:
        super().__init__(**kwargs)


    def add_shedule(self, idDoctor):
        try:
            self.doctor_id_s = idDoctor
            db.session.add(self)
            db.session.commit()     
        except SQLAlchemyError as err_sql:
            db.session.rollback()
            db.session.close()
            raise err_sql

class Specialization(db.Model):

################################# Class attribute ##############################################
    spec_id = db.Column(db.String(14), primary_key=True)
    name_spec = db.Column(db.String(200), nullable=False, unique=True)

################################# Relationship #################################################
    doctors = db.relationship('Doctor', secondary=doctor_specialization,
        back_populates='specializ', lazy=True)

################################# Table properties #############################################
    __tablename__ = "specializations"
    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'specializations'}

################################# Class Methods ################################################
    @classmethod
    def get_list(self):
        try:
            spec_doctor = self.query.all()
            db.session.commit()
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            db.session.close()
            raise Exception(err_sql)
        
        return spec_doctor


    @classmethod
    def check_specializ(self, kwargs):
        special = []
        try:
            for spec_id in kwargs["specializ"]:
                special.append(Specialization.query.filter(self.spec_id==spec_id["spec_id"]).one())
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            db.session.close()
            raise Exception(err_sql)
        return special

################################# Object Methods ###############################################
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.spec_id = kwargs.get('spec_id')
        self.name_spec = kwargs.get('name_spec')

    def __repr__(self):
        return self.spec_id


class Doctor(User):

################################# ForeignKey ##################################################
    doctor_id = db.Column(
        db.Integer, db.ForeignKey('users.user_data_id', name='fk__doctor_id.>>>.users.user_data_id',
        ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    id_city = db.Column(
        db.Integer, db.ForeignKey('places.id_place', name='fk__id_city.>>>.places.id_place',
        ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    clinic = db.Column(
        db.Integer, db.ForeignKey('clinics.clinic_id', name='fk__clinic.>>>.clinics.clinic_id',
        ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)

################################# Class attribute ##############################################
    description = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(500), nullable=False)
    __approved_status = db.Column("approved_status", db.Boolean, default=0, nullable=False)
    __count_patient = db.Column("count_patient", db.Integer, nullable=False, default=0)

################################# Relationship #################################################
    specializ = db.relationship('Specialization', secondary=doctor_specialization, back_populates='doctors', lazy=True)
    favor_doctor = db.relationship('Patient', secondary=favorites_doctors, back_populates='doctors_favor', lazy=True)
    shedule_doctor = db.relationship('Shedule', backref=backref('doctor', uselist=False))
    place_work = db.relationship('PlaceWork', backref=backref('doctor_place', uselist=False))
    clinic_work = db.relationship('Clinic', backref=backref('doctor_clinic', uselist=False))
    appoint_dd = db.relationship('Appointment', backref=backref('doctor_appoints', uselist=True))
################################# Table properties #############################################
    __tablename__ = "doctors"
    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'doctors'}

################################# Get, Set Methods #############################################
    @property
    def get_count_patient(self)-> int: return self.__count_patient

################################# Class Methods ################################################
    @classmethod
    def get_list(self, kwargs):
        if(kwargs): 
            print(kwargs)
            if(len(kwargs)==3):
                doctors_list = self.query.filter(and_(self.id_city == kwargs.get("city"),
                    self.__approved_status == True, 
                    self.clinic == kwargs.get("clinic_work"), 
                    self.specializ.any(Specialization.spec_id == kwargs.get("specializ")))).all()
                return doctors_list
            elif(len(kwargs) > 1):
                if ("city" in kwargs.keys() and "clinic_work" in kwargs.keys()):
                    doctors_list = self.query.filter(and_(self.id_city == kwargs.get("city"), 
                        self.__approved_status == True,
                        self.clinic == kwargs.get("clinic_work"))).all()
                    return doctors_list
                if ("city" in kwargs.keys() and "specializ" in kwargs.keys()):
                    doctors_list = self.query.filter(and_(self.id_city == kwargs.get("city"),
                    self.__approved_status == True, 
                    self.specializ.any(Specialization.spec_id == kwargs.get("specializ")))).all()
                    return doctors_list
                else:
                    doctors_list = self.query.filter(and_(self.id_city == kwargs.get("clinic_work"),
                    self.__approved_status == True, 
                    self.specializ.any(Specialization.spec_id == kwargs.get("specializ")))).all()
                    return doctors_list
            else:
                
                doctors_list = self.query.filter(or_(self.id_city == kwargs.get("city"), 
                    self.clinic == kwargs.get("clinic_work"), 
                    self.specializ.any(Specialization.spec_id == kwargs.get("specializ")))
                    ).all()
                return doctors_list               

        try:
            doctors_list = self.query.filter(self.__approved_status == True).all()
            db.session.commit()
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            db.session.close()
            raise Exception(err_sql)
        return doctors_list


    @classmethod
    def get_doctor(self, id_doctor):
        doctor = self.query.get(id_doctor)
        
        if not doctor:
            db.session.rollback()
            db.session.close()
            raise Exception('No doctor with this id')   
        db.session.commit()           
        return doctor

    

################################# Object Methods ###############################################
    def __init__(self, kwargs) -> None:        
        super().__init__(kwargs.get("user_data"))
        del kwargs["user_data"]
        self.description = kwargs.get('description')
        self.experience = kwargs.pop('experience')
        self.education = kwargs.pop('education')   
        

    def save_doctor(self) -> None: self._save_user()

    def check_slot_appoint(self, data_time):
        
        future_appointment = Appointment.query.filter(and_(Appointment.doctor_id == self.doctor_id, 
                        Appointment.status == AppointStatus.WAITING)).all()
        for i in range(len(future_appointment)):
            if (datetime.strftime(future_appointment[i].data_time_appoint, '%d:%H:%M') == \
                datetime.strftime(data_time, '%d:%H:%M')): 
                raise Exception ("The time for making an appointment is already taken")
                
            


class PlaceWork(db.Model):
    __tablename__ = "places"
    
    id_place = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_city = db.Column(db.String(200), nullable=False, unique=True)
    

    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'places'}

    def __repr__(self):
        return self.name_city
    
    def __init__(self, kwargs) -> None:        
        super().__init__(**kwargs)

        
    def save(self) -> None: 
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_place(self, place_id)->int:
        try:
            self.query.filter(self.id_place == place_id).one()
        except exc.NoResultFound as err_sql:
            db.session.rollback() 
            db.session.close()
            raise Exception(err_sql)
        return place_id
    
    @classmethod
    def get_list(self):
        try:
            places = self.query.all()
            db.session.commit()
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            db.session.close()
            raise Exception(err_sql)
        
        return places

    @classmethod
    def get_place_name(self, name)->int:
        return self.query.filter(self.name_city == name).one_or_none()


class Patient(User):


    patient_id = db.Column(
        db.Integer, db.ForeignKey('users.user_data_id', name='fk__patient_ids.>>>.users.user_data_id',
        ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    сitizenship =  db.Column(db.Enum(Nationality), nullable=False)
    doctors_favor = db.relationship('Doctor', secondary=favorites_doctors,
        back_populates='favor_doctor', lazy=True) 
    appointment_patient = db.relationship('Appointment', backref=backref('patient_appoints', uselist=True))

    __tablename__ = "patients"
    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'patients'}

    def __init__(self, kwargs) -> None:        
        super().__init__(kwargs.get("user_data"))
        del kwargs["user_data"]
        self.сitizenship = kwargs.get('сitizenship')

    def save(self) -> None: self._save_user()  

    @classmethod
    def get_patient(self, key):
        return self.check_token(key)



class Appointment(db.Model):

    __tablename__ = "appointments"

    id_appoint = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(
        db.Integer, db.ForeignKey('doctors.doctor_id', name='fk__app_doctor_id.>>>.doctors.doctor_id',
        ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)   
    patient_id = db.Column(
        db.Integer, db.ForeignKey('patients.patient_id', name='fk__patient_id.>>>.patients.patient_id',
        ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    data_time_appoint = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(AppointStatus), nullable=False, default="WAITING", onupdate="POSTPONED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    
    

    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'appointments'}

    def __init__(self, kwargs) -> None:
        super().__init__(**kwargs)

    @classmethod
    def get_patient_list_appointment(self, patient_id):
        try:

            appointment = self.query.filter(or_(self.doctor_id == patient_id, self.patient_id == patient_id)).all()
            for i in range(len(appointment)):
                if (appointment[i].status == AppointStatus.WAITING and appointment[i].data_time_appoint < datetime.today()):
                    appointment[i].status = AppointStatus.CANCELED
                    db.session.commit()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return appointment


    @classmethod
    def get_appointment(self, id_, iduser):
        try:
            appointment = self.query.get(id_)
            if appointment:          
                if (appointment.status == AppointStatus.WAITING and appointment.data_time_appoint < datetime.today()):
                    appointment.status = AppointStatus.CANCELED
                    db.session.commit()
                if(appointment.doctor_id == iduser or appointment.patient_id == iduser):
                    db.session.commit()
                    return appointment
            raise Exception ("Appointment does not exist")
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            raise Exception(err_sql)

    def update(self, kwargs):
        try:
            print(kwargs)
            for key, value in kwargs.items():
                print(value)
                setattr(self, key, value)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error update")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise



    
    


class Clinic(db.Model):

    __tablename__ = "clinics"

    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_name = db.Column(db.String(150), nullable=False, unique=True)
    clinic_phone = db.Column(db.String(12), nullable=False, unique=True)
    adress_clinic = db.Column(db.String(200), nullable=False)

    __table_args__ = {'mysql_row_format': 'COMPRESSED'}
    __mapper_args__ = {'polymorphic_identity':'clinics'}

    @classmethod
    def get_clinic(self, clinic_id)->int:
        try:
            self.query.filter(self.clinic_id == clinic_id).one()
        except exc.NoResultFound as err_sql:
            db.session.rollback() 
            db.session.close()
            raise Exception(err_sql)
        return clinic_id
    
    

    @classmethod
    def get_list(self):
        try:
            clinic = self.query.all()
            db.session.commit()
        except exc.NoResultFound as err_sql:
            db.session.rollback()
            db.session.close()
            raise Exception(err_sql)
        
        return clinic
    def save(self) -> None: 
        db.session.add(self)
        db.session.commit()

    def __init__(self, kwargs) -> None:        
        super().__init__(**kwargs)
        
