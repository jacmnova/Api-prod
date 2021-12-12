from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import hospitals
import local
import medicine
import cid
import specialty
import doctors
import newPatientInfo
import patients
import appointments
from routes.auth import routes_auth
from routes.auth import validate_token
import function_jwt
import downloads
import users
import awsupload

app = Flask(__name__)
# app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(routes_auth)
cors = CORS(app)

api = Api(app)


@app.route('/oauth/access_token', methods=['POST'])
def acces_token():
    token = request.headers["Authorization"].split(" ")[1]
    new_token = function_jwt.refresh_token(token)
    return jsonify({
                'token': new_token,
                'access_token': new_token})

@app.route('/api/veificar/mobile')
def verifcarSession():
    token = request.headers["Authorization"].split(" ")[1]
    info = users.validate_sesion(token)
    return jsonify(info)

#Mobile
@app.route('/hospitals/mobile')
def get_hospital_mobile():
    data = hospitals.get_hospitals_mobile()
    return jsonify(data)


@app.route('/api/newPatientInfo/mobile', methods=['GET'])
def new_patient_info_mobile():
    data = newPatientInfo.get_data_mobile()
    return jsonify(data)

@app.route('/api/patients/mobile/<info>', methods=['GET'])
def get_patient_detail_mobile(info):
    aux = patients.get_info_patient_mobile(info)
    return jsonify(aux)

@app.route('/patients/mobile', methods=['POST'])
def patient_save_mobile():
    info = request.json
    token = request.headers["Authorization"].split(" ")[1]
    function_jwt.set_token(token)
    data = patients.new_patient_mobile(info)
    return jsonify(data)

@app.route('/users/forgot', methods=['POST'])
def forgot_users():
    username = request.json
    aux = users.forgot(username['username'])
    if aux == True:
        return jsonify({'resend': True})
    else:
        return jsonify({'resend': False})

@app.route('/api/hospitals/mobile/<id_hospital>', methods=['GET'])
def hopital_info_mobile(id_hospital):
    data = hospitals.get_hospitals_info_mobile(id_hospital)
    return jsonify(data)

@app.route('/api/appointments/mobile/', methods=['POST'])
def appointments_save_mobile():
    info = request.json
    print("INSERTE APPOTIN")
    token = request.headers["Authorization"].split(" ")[1]
    appointments.insert_appointments_mobile(info, token)
    return jsonify({'create': True})

@app.route('/api/appointments/mobile/todays', methods=['POST'])
def appointments_today_mobile():
    token = request.headers["Authorization"].split(" ")[1]
    info = request.json
    data = appointments.appointments_by_user_mobile(token, info)
    return jsonify(data)

@app.route('/api/appointments/mobile/search', methods=['POST'])
def appointments_search_mobile():
    token = request.headers["Authorization"].split(" ")[1]
    info = request.json
    data = appointments.appointments_by_data_mobile(token, info)
    return jsonify(data)


#CHECK CPF
@app.route('/api/check/cpf', methods=['POST'])
def check_valid_cpf():
    info = request.json
    aux = patients.check_cpf(info)
    return jsonify({'isValid': aux})

@app.route('/patients/delete/<id>', methods=['DELETE'])
def patients_delete(id):
    aux = patients.delete(id)
    if aux == True:
        return jsonify({'delete': aux})
    else:
        return 401

# @app.route("/api/patients/delete/v2", methods=['POST'])
# def patients_delete():
#     data = request.json
#     patients.delete(data)
#     # patients.update_patient(data)
#     return jsonify({'create': True})

#Hospitals
class Hospitals(Resource):
    def get(self):
        data = hospitals.get_hospitals()
        return jsonify(data)

    def post(self):
        info = request.json
        token = request.headers["Authorization"].split(" ")[1]
        data = hospitals.put_hospitals(info)
        return jsonify({'update' : data})

@app.route('/api/hospitals/save', methods=['POST'])
def hospital_save():
    auth = request.json
    duplicate = hospitals.save_hospitals(auth)
    return jsonify({'duplicate' : duplicate})

@app.route('/api/hospitals/delete', methods=['POST'])
def hospital_delete():
    info = request.json
    data = hospitals.delete_hospitals(info)
    return jsonify({'delete': data})

#Locals
class Local(Resource):
    def get(self):
        data = local.get_locals()
        return jsonify(data)

    def put(self):
        info = request.json
        data = local.put_locals(info)
        return jsonify({'update' : data})

@app.route('/api/local/save', methods=['POST'])
def local_save():
    auth = request.json
    duplicate = local.save_locals(auth)
    return jsonify({'duplicate' : duplicate})

@app.route('/api/local/delete', methods=['POST'])
def local_delete():
    info = request.json
    data = local.delete_locals(info)
    return jsonify({'delete': data})

#Medicines
class Medicine(Resource):
    def get(self):
        data = medicine.get_medicine()
        return jsonify(data)

    def put(self):
        info = request.json
        data = medicine.put_medicine(info)
        return jsonify({'update' : data})

@app.route('/api/medicine/save', methods=['POST'])
def medicine_save():
    auth = request.json
    duplicate = medicine.save_medicine(auth)
    return jsonify({'duplicate' : duplicate})

@app.route('/api/medicine/delete', methods=['POST'])
def medicine_delete():
    info = request.json
    data = medicine.delete_medicine(info)
    return jsonify({'delete': data})

#CIDs
class CID(Resource):
    def get(self):
        data = cid.get_cid()
        return jsonify(data)

    def post(self):
        info = request.json
        token = request.headers["Authorization"].split(" ")[1]
        data = cid.put_cid(info, token)
        return jsonify({'update' : data})

@app.route('/api/cids/save', methods=['POST'])
def cid_save():
    token = request.headers["Authorization"].split(" ")[1]
    auth = request.json
    duplicate = cid.save_cid(auth, token)
    return jsonify({'duplicate' : duplicate})

@app.route('/api/cids/delete', methods=['POST'])
def cid_delete():
    info = request.json
    token = request.headers["Authorization"].split(" ")[1]
    auth = request.json
    data = cid.delete_cid(info, token)
    return jsonify({'delete': data})

#Speciality
class Specialty(Resource):
    def get(self):
        data = specialty.get_specialty()
        return data

#Doctors
class Doctors(Resource):
    def get(self):
        data = doctors.get_doctors()
        return jsonify(data)


@app.route('/api/doctors/save', methods=['POST'])
def doctor_save():
    auth = request.json
    duplicate = doctors.save_doctors(auth)
    return jsonify({'duplicate': duplicate})



@app.route('/api/hospitals/<id_hospital>', methods=['GET'])
def hopital_info(id_hospital):
    data = hospitals.get_hospitals_info(id_hospital)
    return jsonify(data)

@app.route('/api/newPatientInfo', methods=['GET'])
def new_patient_info():
    data = newPatientInfo.get_data()
    return jsonify(data)

@app.route('/api/patients/<info>', methods=['GET'])
def get_patient_detail(info):
    aux = patients.get_info_patient(info)
    return jsonify(aux)

#patients
class Patients(Resource):

    def post(self):
        info = request.json
        token = request.headers["Authorization"].split(" ")[1]
        function_jwt.set_token(token)
        data = patients.new_patient(info)
        return jsonify(data)

    def put(self):
        info = request.json
        data = patients.update_patient(info)
        return 200


@app.route('/api/appointments/', methods=['POST'])
def appointments_info():
    info = request.json
    print("INSERTE APPOTIN")
    token = request.headers["Authorization"].split(" ")[1]
    appointments.insert_appointments(info, token)
    return jsonify({'create': True})

@app.route('/api/appointments/update', methods=['POST'])
def appointments_update():
    info = request.json
    appointments.appointments_update(info)
    return jsonify({'create': True})

@app.route("/api/appointments/update/V2", methods=['POST'])
def appointments_update_v2():
    info = request.json
    appointments.appointments_update_v2(info)
    return jsonify({'create': True})

@app.route("/api/appointments/remove", methods=['POST'])
def appointments_remove():
    info = request.json
    appointments.appointments_delete(info)
    return jsonify({'create': True})

@app.route('/appointments/savePhoto', methods=['POST'])
def savePhoto():
    info = request.json
    info = awsupload.upload(info)
    print("SAVE PHOTO")
    return jsonify({'url': info})

@app.route('/api/appointments/todays', methods=['POST'])
def appointments_today():
    token = request.headers["Authorization"].split(" ")[1]
    info = request.json
    data = appointments.appointments_by_user(token, info)
    return jsonify(data)

@app.route('/api/appointments/search', methods=['POST'])
def appointments_search():
    token = request.headers["Authorization"].split(" ")[1]
    info = request.json
    data = appointments.appointments_by_data(token, info)
    return jsonify(data)

@app.route('/api/appointments/edit')
def appointments_get_data():
    data = appointments.get_data()
    return jsonify(data)

@app.route('/api/appointments/<id>')
def appointments_edit(id):
    data = appointments.get_data_appointments_by_id(id)
    return jsonify(data)

@app.route("/api/verify/token")
def verify():
    token = request.headers["Authorization"].split(" ")[1]
    return validate_token(token, output=True)

@app.route("/api/hospital/get")
def get_hosp():
    data = hospitals.get_hospitals()
    return jsonify(data)

@app.route("/api/patients/get")
def get_patient():
    data = patients.get_patients()
    return jsonify(data)

@app.route("/appointments/search", methods=['POST'])
def get_search():
    data = request.json
    info = appointments.appointments_search(data)
    return jsonify(info)

@app.route("/api/appointments/download", methods=['POST'])
def download_appointments():
    data = request.json
    info = appointments.appointments_search_download(data)
    return jsonify(info)

@app.route("/api/appointments/download/<id>")
def download_appointments_by_id(id):
    info = appointments.appointments_download_by_id(id)
    return jsonify(info)

@app.route("/api/patients/get/v2")
def patients_get_V2():
    data = patients.get_v2()
    return jsonify(data)

@app.route("/api/patients/update/v2", methods=['POST'])
def patients_update_V2():
    data = request.json
    patients.update_patient(data)
    return jsonify({'create': True})


@app.route("/api/suporte/get")
def suporte_get():
    data = appointments.suporte()
    return jsonify(data)

@app.route("/api/suporte/update", methods=['POST'])
def suporte_update_data():
    info = request.json
    data = appointments.suporte_update(info)
    return jsonify(data)


@app.route("/api/users/download", methods=['GET'])
def users_download():
    data = users.user_download()
    return jsonify(data)

@app.route("/api/doctors/checkCpf/<cpf>")
def check_doc_cpf(cpf):
    data = doctors.check_cpf_doctor(cpf)
    return jsonify(data)

@app.route("/api/suporte/download", methods=['GET'])
def suporte_download():
    data = appointments.suporte_download()
    return jsonify(data)

@app.route("/api/patients/download")
def download_patients():
    info = patients.patients_download()
    return jsonify(info)

@app.route("/api/local/download")
def download_local():
    info = local.local_download()
    return jsonify(info)

@app.route("/api/hospital/download")
def download_hospital():
    info = hospitals.hospital_download()
    return jsonify(info)

@app.route("/api/medicines/download")
def download_medicinesl():
    info = medicine.medicines_download()
    return jsonify(info)

@app.route("/api/doctors/download")
def download_doctors():
    info = doctors.doctors_download()
    return jsonify(info)

@app.route("/api/cid/download")
def download_cid():
    info = cid.cid_download()
    return jsonify(info)

@app.route("/api/doctors/getInfo", methods=['POST'])
def doctors_get_info():
    data = request.json
    info = doctors.get_doctors_by_id(data)
    return jsonify(info)

@app.route("/api/doctors/update", methods=['POST'])
def doctors_set_info():
    data = request.json
    info = doctors.set_doctor(data)
    return jsonify({'update': True})

@app.route("/api/doctors/delete", methods=['POST'])
def doctors_delete_info():
    data = request.json
    info = doctors.delete_doctor(data)
    return jsonify({'delete': True})

@app.route("/me/updatePassword", methods=['POST'])
def update_senha():
    token = request.headers["Authorization"].split(" ")[1]
    data = request.json
    update = users.update_password_temp(data, token)
    return jsonify({'update': update})





# api.add_resource(Users, '/api/login')
api.add_resource(Hospitals, '/hospitals')
api.add_resource(Local, '/api/local')
api.add_resource(Medicine, '/api/medicine')
api.add_resource(CID, '/api/cids')
api.add_resource(Specialty, '/api/specialty')
api.add_resource(Doctors, '/doctors')
api.add_resource(Patients, '/patients')
# api.add_resource(Hospitals, '/api/hospitals/save')




if __name__ == '__main__':
    load_dotenv()
    app.run()
