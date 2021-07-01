from marshmallow import fields
from medic.models import Doctor
from medic.model_schema import DoctorSchema, DoctorSchemaList
from flask.json import jsonify
from medic.controller_resource.base import identy_token
from flask_restful import Resource, reqparse
from webargs.flaskparser import parser
from flask_apispec import marshal_with

class DoctorListView(Resource):
    @identy_token
    @parser.use_args({"city": fields.Int(), "clinic_work": fields.Int(), "specializ": fields.Str()}, location="query")
    def get(self, args):
            doctor_list = Doctor.get_list(args)
            return jsonify(DoctorSchemaList(many=True).dump(doctor_list))
            

class DoctorDetailView(Resource):
    @identy_token
    @marshal_with(DoctorSchema(exclude=("user_data.phone_number",)))
    def get(self, **doctor_id):
        try:
            print(doctor_id)
            doctor = Doctor.get_doctor(doctor_id.get("doctor_id"))
            
        except Exception as e:
            return {'message': str(e)}, 400
        return doctor
