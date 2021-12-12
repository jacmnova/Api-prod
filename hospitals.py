from datetime import datetime

import psycopg2
import conection
from flask import jsonify
import medicine
import local
import cid
import doctors
import patients

def save_hospitals(auth):
    version = 0
    name = auth['name'].upper()
    status = 'ACTIVE'
    cur = conection.conn.cursor()
    cur.execute("""SELECT 1 FROM public.hospital WHERE "name" = '""" + name + "'")
    records = cur.fetchall()
    print(name)
    print(records)
    if len(records) > 0 :
        cur.execute("""UPDATE public.hospital
                        SET status='ACTIVE'
                        WHERE name='""" + name + "'")
        conection.conn.commit()
        cur.close()
        return True
    else:
        cur.execute("SELECT MAX(id) FROM public.hospital;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1

        cur.execute("""INSERT INTO public.hospital
                    (id, "version", "name", status)
                    VALUES(%s, %s, %s, %s);""", (max, version, name, status))

        return False

def get_hospitals():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.hospital  WHERE status = 'ACTIVE' ORDER BY "name" ASC """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        content = {'id': result[0], 'name': result[1]}
        payload.append(content)
        content = {}
    return payload

def put_hospitals(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.hospital SET "name" = %s WHERE id = %s;""", (info['name'].upper(), info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def delete_hospitals(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.hospital SET status = %s WHERE id = %s;""", ('DELETED', info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def get_hospitals_info(id_hospital):

    medicines = medicine.get_medicine()
    doctors_ = doctors.get_doctors()
    hospitals_ = get_hospitals()
    local_ = local.get_locals()
    cid_ = cid.get_cid()
    patients_ = patients.get_patients()

    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.hospital  WHERE id = '""" + str(id_hospital) + """'""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}


    for result in records:
        content = {'name': result[1],
                   'id': result[0],
                   'medicines': medicines,
                   'doctors': doctors_,
                   'hospitals': hospitals_,
                   'locals': local_,
                   'cids': cid_,
                   'patients': patients_}
        payload.append(content)
        content = {}


    return payload[0]

def get_hospital_data(info):


    info_patients = patients.get_info_patients(info)
    info_doctor = doctors.get_doctors_by_id(info)
    info_hospital = get_hospital_by_id(info)
    timestampStr = info_patients['birth_date'].strftime("%m/%d/%Y")

    cur = conection.conn.cursor()
    cur.execute("""SELECT id, medicine_item_name, dose, cid_name,data_last_atendimineto, local_id FROM public.appointment_history WHERE patient_id = %s""",
                str(info_patients['id']))
    records = cur.fetchall()
    print(records)

    # "07/06/1989"
    if len(records) > 0:
        content = {
            'attentionNumber': info_patients['medical_record'],
            'cpf': info_patients['cpf'],
            'birthDate': info_patients['birth_date'],
            'birthDateStr': timestampStr,
            'covenant': info_patients['covenant'],
            'createdOn': info_patients['creation_date'],
            'doctor': {
                'id': info_doctor['id'],
                'doctorName': info_doctor['name'],
                'name': info_doctor['name'],
                'status': info_doctor['status']
            },
            'doctorPatient': '',
            'hospital': {
                'id': info_hospital['id'],
                'name': info_hospital['name'],
                'status': info_hospital['status']
            },
            'id': info_patients['id'],
            'lastInfo': {
                'id': records[0][0],
                'medicineItem': {
                    'id': '',
                    'name': records[0][1]
                },
                'dose': records[0][2],
                'date': records[0][4],
                'cpi': records[0][3]
            },
            'medicalRecord': info_patients['medical_record'],
            'name': info_patients['name'],
            'newPatient': True,
            'patient': info_patients['name'],
            'phone': info_patients['phone'],
            'local':  info_patients['local_id']
        }
    else:

        content = {
            'attentionNumber': info_patients['medical_record'],
            'cpf': info_patients['cpf'],
            'birthDate': info_patients['birth_date'],
            'birthDateStr': timestampStr,
            'covenant': info_patients['covenant'],
            'createdOn': info_patients['creation_date'],
            'doctor': {
                'id': info_doctor['id'],
                'doctorName': info_doctor['name'],
                'name': info_doctor['name'],
                'status': info_doctor['status']
            },
            'doctorPatient': '',
            'hospital': {
                'id': info_hospital['id'],
                'name': info_hospital['name'],
                'status': info_hospital['status']
            },
            'id': info_patients['id'],
            'lastInfo': {
                'id': '',
                'medicineItem': {
                    'id': '',
                    'name': ''
                },
                'dose': '',
                'date': '',
                'cpi': ''
            },
            'medicalRecord': info_patients['medical_record'],
            'name': info_patients['name'],
            'newPatient': True,
            'patient': info_patients['name'],
            'phone': info_patients['phone'],
            'local': info_patients['local_id']
        }


    # attentionNumber: "1010101123"
    # cid: {id: 14}
    # covenant: ""
    # date: "2021-11-18T20:10:24.428Z"
    # doctorPatient: 15
    # dose: "1 al dia"
    # hospital: {id: 10}
    # local: {id: ''}
    # medicineItem: {name: 'ACLASTA'}
    # otherPhotos: Array(1)
    # 0: Photo
    # {base64: '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQ…J2HgByFQnvZL/ACn5V7rw97Jf5T8qLETFiTdKhAhAAsv/2Q==',
    #  format: 'jpeg', name: 'afa90aa64fe5813cd3e42de7e8bf1d13510f60b8/addic_0.jpeg', id: 2}
    # length: 1
    # [[Prototype]]: Array(0)
    # patient: {id: 1148}
    return content

def get_hospital_by_id(id):
    content = {}
    cur = conection.conn.cursor()
    cur.execute("""SELECT * FROM public.hospital WHERE id = """ + str(id))
    records = cur.fetchall()
    cur.close()

    #id,
    # "version",
    # "name",
    # status
    for result in records:
        content = {
            'id': result[0],
            'version': result[1],
            'name': result[2],
            'status': result[4],
        }

    return content

def hospital_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "name" FROM public.hospital WHERE status = 'ACTIVE' ORDER BY "name" ASC;""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        content = {
            'name': i[0],
        }
        payload.append(content)
        content = {}
    return payload


## MOBILE

def get_hospitals_mobile():
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT "id", "name" FROM public.hospital  WHERE status = 'ACTIVE' ORDER BY "name" ASC """)
        records = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in records:
            content = {'id': result[0], 'name': result[1]}
            payload.append(content)
            content = {}
        return payload
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()

def get_hospitals_info_mobile(id_hospital):

    medicines = medicine.get_medicine()
    doctors_ = doctors.get_doctors()
    hospitals_ = get_hospitals()
    local_ = local.get_locals()
    cid_ = cid.get_cid()
    patients_ = patients.get_patients()
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT "id", "name" FROM public.hospital  WHERE id = '""" + str(id_hospital) + """'""")
        records = cur.fetchall()
        cur.close()
        payload = []
        content = {}


        for result in records:
            content = {'name': result[1],
                       'id': result[0],
                       'medicines': medicines,
                       'doctors': doctors_,
                       'hospitals': hospitals_,
                       'locals': local_,
                       'cids': cid_,
                       'patients': patients_}
            payload.append(content)
            content = {}
            return payload[0]
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return payload


