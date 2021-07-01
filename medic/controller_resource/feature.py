
from sqlalchemy.orm import load_only
from medic.controller_resource.base import identy_token
from flask.json import jsonify
from flask_restful import Resource
from medic.models import Clinic, PlaceWork, Specialization
from medic.model_schema import ClinicSchema, PlaceWorkSchema, SpecializationSchema
from webargs.flaskparser import use_kwargs
from medic import logger

class SpecializationsList(Resource):
    def get(self): return jsonify(SpecializationSchema(many=True).dump(Specialization.get_list()))

class PlacesList(Resource):
    def get(self): return jsonify(PlaceWorkSchema(many=True).dump(PlaceWork.get_list()))
    
    @use_kwargs(PlaceWorkSchema)
    def post(self, **kwargs):
                          
            if not PlaceWork.get_place_name(kwargs.get('name_city')):
                place = PlaceWork(kwargs)       
                place.save()
                return {'message': "Place added. Its OK"}, 201
       
            return {'messagee': "Place already exists"}, 400            
    
class ClinicList(Resource):
    def get(self): return jsonify(ClinicSchema(many=True).dump(Clinic.get_list()))

    @use_kwargs(ClinicSchema)
    def post(self, **kwargs):                     
            if not Clinic.get_clinic_name(kwargs.get('clinic_name')):
                clinic = Clinic(kwargs)       
                clinic.save()
                return {'message': "Clinic added. Its OK"}, 201
        
            return {'messagee': "Clinic already exists"}, 400            
        