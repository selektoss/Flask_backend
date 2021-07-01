from medic import logger
from flask_restful import Resource, reqparse
from medic.models import Clinic, Doctor, Patient, PlaceWork, Shedule, Specialization, AuthenticationData
from medic.model_schema import AuthSchema, DoctorSchema, PatientSchema
from webargs.flaskparser import use_kwargs, parser, abort
from flask import request
import werkzeug

class RegisterPatient(Resource):
    @use_kwargs(PatientSchema)
    def post(self, **kwargs):                      
        try:                     
            if not AuthenticationData.authenticate(
                kwargs.get('user_data').get('auth_data').get('emailadress')):
                patient = Patient(kwargs)       
                patient.save()
        except Exception as e:
            logger.warning(f'Registration failed with errors: {e}')
            return {'messagee': str(e)}, 400            
        return {'access_token': patient.get_token}, 201


class Register(Resource):  
    @use_kwargs(DoctorSchema)
    def post(self, **kwargs):                      
        try:          
            if not AuthenticationData.authenticate(
                kwargs.get('user_data').get('auth_data').get('emailadress')):
                    doctor = Doctor(kwargs)
                    doctor.id_city = PlaceWork.get_place(kwargs.get("place_work").get('id_place'))
                    doctor.clinic = Clinic.get_clinic(kwargs.get("clinic_work").get('clinic_id'))                 
                    doctor.specializ = Specialization.check_specializ(kwargs)
                    doctor.save_doctor()
                    Shedule(kwargs.get("shedule_doctor")).add_shedule(doctor.doctor_id)     
        except Exception as e:
            logger.warning(f'Registration failed with errors: {e}')
            return {'messagee': str(e)}, 400            
        return {'access_token': doctor.get_token}, 201

    
    @parser.error_handler
    def handle_request_parsing_error(err,req, schema, *, error_status_code, error_headers):
        
        abort(422, errors=err.messages)   


class Authentication(Resource):
    @use_kwargs(AuthSchema)
    def post(self, **kwargs):
        try:
            return {'access_token': AuthenticationData.authenticate(**kwargs).get_token}, 200
        except Exception as e:
            logger.warning(
                f'login with email {kwargs["emailadress"]} failed with errors: {e}')
            return {'message': str(e)}, 401


class FileUpload(Resource):
    def post(self): 
        parse = reqparse.RequestParser()
        print(request.files)
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("your_file_name.jpg")

