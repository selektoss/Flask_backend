import datetime
from medic.const import *
from marshmallow import Schema, validate, fields, validates_schema, ValidationError
from marshmallow_enum import EnumField
from .models import AppointStatus, Gender, Nationality, RoleUsers

class AuthSchema(Schema):
    emailadress = fields.String(required = True, 
        validate = [validate.Email(error = EMAIL_MESSAGE), 
        validate.Regexp(EMAIL_REGEX)], load_only = True)
        
    password = fields.String(required = True, 
        validate=[validate.Length(max = 50, min = 5, error = PASSWORD_MESSAGE), 
        validate.Regexp(PASSWORD_REGEX)], load_only = True)
    role_type = EnumField(RoleUsers)

class UserSchema(Schema):    
    gender = EnumField(Gender, required = True, error = GENDER_MESSAGE)
    firstname = fields.String(required = True, validate = [validate.Length(max = 50),validate.Regexp(SYMBOL_REGEX)])
    lastname = fields.String(validate = [validate.Length(max = 50),validate.Regexp(SYMBOL_REGEX)], required = True)
    patname = fields.String(validate = [validate.Length(max = 50),validate.Regexp(SYMBOL_REGEX)])
    phone_number = fields.String(required=True, validate = [validate.Length(min = 12, max = 12),validate.Regexp(PHONE_REGEX)])
    birthday = fields.Date(required = True)
    profile_pic = fields.String(validate = [validate.Length(max = 200)])
    auth_data = fields.Nested(AuthSchema, many = False, required = True)


class SpecializationSchema(Schema):
    spec_id = fields.String(validate = [validate.Length(max = 10)])
    name_spec = fields.String(validate = [validate.Length(max = 200)])


class SheduleSchema(Schema):
    time_val = [validate.Range(min=datetime.time(hour=6, minute=00),max=datetime.time(hour=21, minute=00))]
    monday_start = fields.Time(required = False, validate = time_val)
    monday_end = fields.Time(required = False, validate = time_val)
    tuesday_start = fields.Time(required = False, validate = time_val)
    tuesday_end = fields.Time(required = False, validate = time_val)
    wednesday_start = fields.Time(required = False, validate = time_val)
    wednesday_end = fields.Time(required = False, validate = time_val)
    thursday_start = fields.Time(required = False, validate = time_val)
    thursday_end = fields.Time(required = False, validate = time_val)
    friday_start = fields.Time(required = False, validate = time_val)
    friday_end = fields.Time(required = False, validate = time_val)
    time_step = fields.Integer(required = True, validate = [validate.Range(min = 30,max = 240)])

    
     

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if (len(data) < 3): raise ValidationError("Error json data")
        
        if not self.__time_check(data.get('monday_start'), 
                data.get('monday_end'), data.get('time_step')):
                    raise ValidationError("Wrong range format time __shedule_doctor. Time work incorrect")

        if not self.__time_check(data.get('tuesday_start'), 
                data.get('tuesday_end'), data.get('time_step')):
                   raise ValidationError("Wrong range format time __shedule_doctor. Time work incorrect")

        if not self.__time_check(data.get('wednesday_start'), 
                data.get('wednesday_end'), data.get('time_step')):
                    raise ValidationError("Wrong range format time __shedule_doctor. Time work incorrect")

        if not self.__time_check(data.get('thursday_start'), 
                data.get('thursday_end'), data.get('time_step')):
                    raise ValidationError("Wrong range format time __shedule_doctor. Time work incorrect")

        if not self.__time_check(data.get('friday_start'), 
                data.get('friday_end'), data.get('time_step')):    
                    raise ValidationError("Wrong range format time __shedule_doctor. Time work incorrect")
        
            

    def __time_check(self, time_start, time_end, step_time):
        if(time_start and time_end):  
            start = datetime.datetime(2021, 1, 1,
                hour = time_start.hour, minute = time_start.minute)   
            if not (start + datetime.timedelta(minutes=step_time)).time() <= time_end: 
                return False
            else: return True
        elif (time_start is time_end):
            return True
        return False

class ClinicSchema(Schema):
    clinic_id = fields.Integer(validate = [validate.Range(min = 0,max = 100)], required = False)
    clinic_name = fields.String(validate=[validate.Length(max = 150), validate.Regexp(TXT_REGEX)], required = False)
    clinic_phone = fields.String(required=False, validate = [validate.Length(min = 12, max = 12),validate.Regexp(PHONE_REGEX)])
    adress_clinic = fields.String(validate=[validate.Length(max = 200), validate.Regexp(TXT_REGEX)], required = False)

class PlaceWorkSchema(Schema):
    id_place = fields.Integer(validate = [validate.Range(min = 0,max = 100)], required = False)
    name_city = fields.String(required=False, validate=[validate.Length(max = 500), validate.Regexp(TXT_REGEX)])

class DoctorSchema(Schema):
    description = fields.String(validate=[validate.Length(max = 4000), validate.Regexp(TXT_REGEX)], required = True)
    experience = fields.Integer(validate=[validate.Range(min = 0,max = 100)], required = True)
    clinic_work = fields.Nested(ClinicSchema, many = False, required = True)
    education = fields.String(required=False, validate=[validate.Length(max = 500), validate.Regexp(TXT_REGEX)])
    user_data = fields.Nested(UserSchema, many = False, required = True)
    specializ = fields.Nested(SpecializationSchema, many = True, required = True)
    shedule_doctor = fields.Nested(SheduleSchema, many = False, required = True)
    place_work = fields.Nested(PlaceWorkSchema, many = False, required = True)

class DoctorSchemaList(Schema):
    
    doctor_id = fields.Integer(required = True, dump_only=True)
    user_data = fields.Nested(UserSchema, many = False, required = True, only=("firstname", "lastname", "patname", "profile_pic"))
    specializ = fields.Nested(SpecializationSchema, many = True, required = True, only=("name_spec",))
    place_work = fields.Nested(PlaceWorkSchema, many = False, required = True)
    clinic_work = fields.Nested(ClinicSchema, many = False, required = True)

class PatientSchema(Schema):
    user_data = fields.Nested(UserSchema, many = False, required = True)
    сitizenship = EnumField(Nationality)
    

class AppointSchema(Schema):
    id_appoint = fields.Integer(required = True, dump_only=True)
    patient_appoints = fields.Nested(PatientSchema, many = True, required = True, dump_only=True, exclude=("user_data.auth_data",))
    patient_id = fields.Integer(dump_only=True)
    doctor_id = fields.Integer(required = True, load_only=True)
    description = fields.String(validate=[validate.Length(max = 255), validate.Regexp(TXT_REGEX)], required = True)
    data_time_appoint = fields.DateTime(required = True, validate=[validate.Range(min = datetime.datetime.today())])
    status = EnumField(AppointStatus, dump_only=True)
    doctor_appoints = fields.Nested(DoctorSchema, many = True, required = True, dump_only=True, 
        only=("clinic_work.adress_clinic","clinic_work.clinic_name",
        "place_work.name_city", "specializ","user_data.firstname","user_data.firstname",
        "user_data.lastname", "user_data.phone_number"))


class AppointSchemaList(Schema):
    id_appoint = fields.Integer(required = True, dump_only=True)
    data_time_appoint = fields.DateTime(required = True, dump_only=True)
    description = fields.String(required = True, dump_only=True)
    status = EnumField(AppointStatus, dump_only=True)
    doctor_id = fields.Integer(required = True, dump_only=True)
    patient_id = fields.Integer(required = True, dump_only=True)
    doctor_appoints = fields.Nested(DoctorSchema, many = True, required = True, 
        dump_only=True, only=("user_data.firstname","user_data.lastname",
            "user_data.phone_number", "clinic_work.adress_clinic", "clinic_work.clinic_name"))
    patient_appoints = fields.Nested(PatientSchema, many = True, required = True, dump_only=True,
    only=("user_data.firstname","user_data.lastname",
            "user_data.phone_number"))
    

class AppointSchemaUpdate(Schema):
    status = EnumField(AppointStatus, required = True)
    data_time_appoint = fields.DateTime(load_only=True)