
from medic.controller_resource.appointment import AppointmentDetailView, Appointments
from medic.controller_resource.doctors import DoctorDetailView, DoctorListView
from medic.controller_resource.feature import ClinicList, SpecializationsList, PlacesList
from medic.controller_resource.register import FileUpload, Register, Authentication, RegisterPatient
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Register, '/register')
api.add_resource(Authentication, '/auth')
api.add_resource(FileUpload, '/upload')
api.add_resource(SpecializationsList, '/specializations')
api.add_resource(DoctorListView, '/doctors')
api.add_resource(DoctorDetailView, '/doctors/<int:doctor_id>')
api.add_resource(PlacesList, '/places')
api.add_resource(RegisterPatient, '/registerpatient')
api.add_resource(ClinicList, '/clinics')
api.add_resource(Appointments, '/appointment')
api.add_resource(AppointmentDetailView, '/appointment/<int:id_appoint>')