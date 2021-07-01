from flask.json import jsonify
from medic.controller_resource.base import get_identy, identy_token
from medic import logger
from flask_restful import Resource
from medic.models import Appointment, Doctor, RoleUsers, db
from medic.model_schema import AppointSchema, AppointSchemaList, AppointSchemaUpdate
from webargs.flaskparser import use_kwargs
from flask_apispec import marshal_with

class Appointments(Resource):
    
    @identy_token
    @marshal_with(AppointSchema(many=False))
    @use_kwargs(AppointSchema)
    def post(self, **kwargs):
        try:
            doctor = Doctor.get_doctor(kwargs.get("doctor_id"))           
            doctor.check_slot_appoint(kwargs.get("data_time_appoint"))
            kwargs["patient_id"] = get_identy().data_id
            appoin = Appointment(kwargs)
            doctor.appoint_dd.insert(0, appoin)
            db.session.commit()
            return jsonify(AppointSchema(exclude=("patient_appoints","patient_id")).dump(appoin))
        except Exception as e:
            return {'messagee': str(e)}, 400


    @identy_token
    def get(self, *a):
        try:
            user = get_identy() 
            appointment = Appointment.get_patient_list_appointment(user.data_id)
            if user.role_type == RoleUsers.DOCTOR:
               return jsonify(AppointSchemaList(many=True, exclude=("doctor_id",
                "doctor_appoints")).dump(appointment))
            return jsonify(AppointSchemaList(many=True, exclude=("patient_appoints",)).dump(appointment))
        except Exception as e:
            logger.warning(
                f'user: failed with errors: {e}')
            return {'message': str(e)}, 400
        
class AppointmentDetailView(Resource):
    @identy_token
    def get(self, **id_):     
        try: 
            print(id_)       
            user = get_identy()
            appoint = Appointment.get_appointment(id_.get("id_appoint"), user.data_id)
            if user.role_type == RoleUsers.DOCTOR:  
                return jsonify(AppointSchema(exclude=("doctor_id",
                "doctor_appoints")).dump(appoint))
            return jsonify(AppointSchema(exclude=("patient_appoints","patient_id")).dump(appoint))
        except Exception as e:
            logger.warning(
                f'get action failed with errors: {e}')
            return {'message': str(e)}, 400

    @identy_token    
    @use_kwargs(AppointSchemaUpdate)
    def put(self, **id_):
        print(id_)
        try:        
            user = get_identy()
            appoint = Appointment.get_appointment(id_.get("id_appoint"), user.data_id)
            if user.role_type == RoleUsers.DOCTOR:
                appoint.update(id_)
                return jsonify(AppointSchema(exclude=("doctor_id",
                "doctor_appoints")).dump(appoint))
        except Exception as e:
            logger.warning(
                f'get action failed with errors: {e}')
            return {'message': str(e)}, 400

    @identy_token
    def delete(self, **id_):
        try:        
            user = get_identy()
            appoint = Appointment.get_appointment(id_.get("id_appoint"), user.data_id)
            if user.role_type == RoleUsers.PATIENT:
                appoint.delete()
                
        except Exception as e:
            logger.warning(
                f'get action failed with errors: {e}')
            return {'message': str(e)}, 400    