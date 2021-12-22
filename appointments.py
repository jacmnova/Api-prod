import psycopg2
from datetime import datetime
import conection
from routes import auth
import cid
import doctors
import hospitals
import local
import medicine
import patients
from function_jwt import validate_token
import datetime
import pytz
import specialty


# {
#     'patient': {'id': 3},
#     'cid': {'id': 1},
#     'medicineItem': {'name': 'ATAMEL'},
#     'attentionNumber': '0000001',
#     'date': '2021-11-27T00:50:56.943Z',
#     'dose': '1 al dia',
#     'covenant': None,
#     'hospital': {'id': 2},
#     'local': {'id': None}
#  }


# CREATE TABLE public.appointment_complete (
# 	id serial4 NOT NULL,
# 	"version" int8 NOT NULL,
# 	patient_id int8 NOT NULL,
# 	patient_name varchar(255) NULL,
# 	patient_medical_record varchar(255) NULL,
# 	patient_covenat varchar(255) NULL,
# 	patient_cpf varchar(255) NULL,
# 	patient_phone varchar(255) NULL,

# 	medicine varchar(255) NULL,


# 	hospital_id int8 NOT NULL,
# 	hospital_name varchar(255) NULL,

# 	login_user_id int8 NULL,

# 	created_on timestamp NOT NULL,

# 	cid_id int8 NULL,
# 	cid_name varchar(255) NULL,
# 	covenant varchar(255) NULL,

# 	local_id int8 NULL,
# 	local_name varchar(255) NULL,

# 	dose varchar(255) NULL,
# 	medicine_item_name varchar(255) NULL,
# 	doctor_id int8 NULL,
# 	doctor_name varchar(255) NULL,
# 	doctor_specialty varchar(255) NULL,
# 	doctor_cpf varchar(255) NULL,

# 	doctor_atention_id int8 NULL,
# 	doctor_atention_name varchar(255) NULL,
# 	doctor_atention_specialty varchar(255) NULL,
# 	doctor_atention_cpf varchar(255) NULL,

# 	attention_number varchar(255) NULL
# );
def insert_appointments(info, token):

    print("INSERTANDO APPOINTMENT! ")
    patient_info = patients.get_info_patients(info['patient']['id'])

    version = 0
    patient_id = patient_info['id']
    patient_name = patient_info['name'].upper()
    patient_medical_record = patient_info['attentionNumber'].upper()
    patient_covenat = patient_info['covenant'].upper()
    patient_cpf = patient_info['cpf']
    patient_phone = patient_info['phone']
    medicines = info['medicineItem']['name'].upper()

    hospital_info = hospitals.get_hospital_by_id(info['hospital']['id'])
    hospital_id = hospital_info['id']
    hospital_name = hospital_info['name']

    info_user = validate_token(token, True)
    login_user_id = info_user['id']



    info_cid = cid.get_cid_by_id(info['cid']['id'])
    cid_id = info_cid['id']
    cid_name = info_cid['name']
    covenant = patient_info['covenant'].upper()

    local_id = 0
    local_name = ''

    dose = str(info['dose']).upper()
    medicine_item_name = str(info['medicineItem']['name']).upper()

    info_doctor = doctors.get_doctors_by_id(patient_info['doctor_id'])
    doctor_id = info_doctor['id']
    doctor_name = info_doctor['name']

    specialty_info = specialty.get_specialty_by_id(info_doctor['specialty'])
    doctor_specialty = specialty_info['name']
    doctor_cpf = info_doctor['cpf']

    info_doctor_atention = doctors.get_doctors_by_id(info_user['doctor_id'])
    doctor_atention_id = info_doctor_atention['id']
    doctor_atention_name = info_doctor_atention['name']
    specialty_info = specialty.get_specialty_by_id(info_doctor_atention['specialty'])
    doctor_atention_specialty = specialty_info['name']
    doctor_atention_cpf = info_doctor_atention['cpf']

    attention_number = info['attentionNumber']

    aux = str(info['medicineItem']['name']).upper()
    medicine_info = medicine.get_medicine_by_name(aux)
    if not medicine_info:
        medicine.save_medicine_v2(aux)
    my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    created_on = my_date.strftime("%Y/%m/%d %H:%M:%S")
    cur = conection.conn.cursor()

    cur.execute("""
    INSERT
    INTO
    public.appointment_complete
    ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone, medicine,
     hospital_id, hospital_name, login_user_id, created_on, cid_id, cid_name, covenant, local_id, local_name, dose,
     medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id, doctor_atention_name,
     doctor_atention_specialty, doctor_atention_cpf, attention_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """,(version, patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone, medicines,
         hospital_id, hospital_name, login_user_id, created_on, cid_id, cid_name, covenant, local_id, local_name, dose,
         medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id, doctor_atention_name,
         doctor_atention_specialty, doctor_atention_cpf, attention_number))
    conection.conn.commit()
    cur.close()


    content = {
        'version': version,
        'patient_id': patient_id,
        'patient_name': patient_name,
        'patient_medical_record': patient_medical_record,
        'patient_covenat': patient_covenat,
        'patient_cpf': patient_cpf,
        'patient_phone': patient_phone,
        'medicines': medicines,
        'hospital_id': hospital_id,
        'hospital_name': hospital_name,
        'login_user_id': login_user_id,
        'created_on': created_on,
        'cid_id': cid_id,
        'cid_name': cid_name,
        'covenant': covenant,
        'local_id': local_id,
        'local_name': local_name,
        'dose': dose,
        'medicine_item_name': medicine_item_name,
        'doctor_id': doctor_id,
        'doctor_name': doctor_name,
        'doctor_specialty': doctor_specialty,
        'doctor_cpf': doctor_cpf,
        'doctor_atention_id': doctor_atention_id,
        'doctor_atention_name': doctor_atention_name,
        'doctor_atention_specialty': doctor_atention_specialty,
        'doctor_atention_cpf': doctor_atention_cpf,
        'attention_number': attention_number
    }

    insert_history(content)
    return

def insert_history(info):
    medicine_item_id = medicine.get_medicine_by_name(info['medicine_item_name'])['id']
    cur = conection.conn.cursor()
    cur.execute("SELECT 1 FROM public.appointment_history WHERE patient_id = " + str(info['patient_id']))
    records = cur.fetchone()
    if records is None:
        if info['cid_id'] == '':
            try:
                cur.execute("""
                INSERT INTO public.appointment_history
                    ("version", patient_id, patient_name, patient_medical_record, patient_covenat, 
                    patient_cpf, doctor_id, doctor_name, doctor_specialty, doctor_cpf, local_id, local_name, 
                    hospital_id, hospital_name, cid_name, medicine_item_id, medicine_item_name, 
                    dose, nro_atendimiento, data_last_atendimineto)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                    info['version'],
                    str(info['patient_id']),
                    info['patient_name'],
                    info['patient_medical_record'],
                    info['patient_covenat'],
                    str(info['patient_cpf']),
                    str(info['doctor_id']),
                    info['doctor_name'],
                    info['doctor_specialty'],
                    str(info['doctor_cpf']),
                    str(info['local_id']),
                    info['local_name'],
                    str(info['hospital_id']),
                    info['hospital_name'],
                    info['cid_name'],
                    str(medicine_item_id),
                    info['medicine_item_name'],
                    info['dose'],
                    1,
                    info['created_on']
                ))
                conection.conn.commit()
                cur.close()
            except:
                curs = conection.conn.cursor()
                curs.execute("ROLLBACK")
                conection.conn.commit()
                curs.close()
                return False
        else:
            try:
                cur.execute("""
                        INSERT INTO public.appointment_history
                            ("version", patient_id, patient_name, patient_medical_record, patient_covenat, 
                            patient_cpf, doctor_id, doctor_name, doctor_specialty, doctor_cpf, local_id, local_name, 
                            hospital_id, hospital_name, cid_id, cid_name, medicine_item_id, medicine_item_name, 
                            dose, nro_atendimiento, data_last_atendimineto)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                    info['version'],
                    str(info['patient_id']),
                    info['patient_name'],
                    info['patient_medical_record'],
                    info['patient_covenat'],
                    str(info['patient_cpf']),
                    str(info['doctor_id']),
                    info['doctor_name'],
                    info['doctor_specialty'],
                    str(info['doctor_cpf']),
                    str(info['local_id']),
                    info['local_name'],
                    str(info['hospital_id']),
                    info['hospital_name'],
                    str(info['cid_id']),
                    info['cid_name'],
                    str(medicine_item_id),
                    info['medicine_item_name'],
                    info['dose'],
                    1,
                    info['created_on']
                ))
                conection.conn.commit()
                cur.close()
                set_active(info['patient_id'])
            except:
                curs = conection.conn.cursor()
                curs.execute("ROLLBACK")
                conection.conn.commit()
                curs.close()
                return False

    else:
        print("update")
        if info['cid_id'] == '':
            try:
                cur.execute("""
                                UPDATE public.appointment_history
                                SET "version"=%s, patient_id=%s, patient_name=%s, patient_medical_record=%s, patient_covenat=%s, 
                                     patient_cpf=%s, doctor_id=%s, doctor_name=%s, doctor_specialty=%s, doctor_cpf=%s, local_id=%s, 
                                     local_name=%s, hospital_id=%s, hospital_name=%s, cid_id=NULL, cid_name=%s, medicine_item_id=%s, 
                                     medicine_item_name=%s, dose=%s, nro_atendimiento = nro_atendimiento::int + 1, data_last_atendimineto=%s
                                WHERE patient_id=%s """, (
                    info['version'],
                    str(info['patient_id']),
                    info['patient_name'],
                    info['patient_medical_record'],
                    info['patient_covenat'],
                    str(info['patient_cpf']),
                    str(info['doctor_id']),
                    info['doctor_name'],
                    info['doctor_specialty'],
                    str(info['doctor_cpf']),
                    str(info['local_id']),
                    info['local_name'],
                    str(info['hospital_id']),
                    info['hospital_name'],
                    info['cid_name'],
                    str(medicine_item_id),
                    info['medicine_item_name'],
                    info['dose'],
                    info['created_on'],
                    str(info['patient_id'])
                ))
                conection.conn.commit()
                cur.close()
            except:
                curs = conection.conn.cursor()
                curs.execute("ROLLBACK")
                conection.conn.commit()
                curs.close()
                return False

        else:
            try:
                cur.execute("""
                    UPDATE public.appointment_history
                    SET "version"=%s, patient_id=%s, patient_name=%s, patient_medical_record=%s, patient_covenat=%s, 
                         patient_cpf=%s, doctor_id=%s, doctor_name=%s, doctor_specialty=%s, doctor_cpf=%s, local_id=%s, 
                         local_name=%s, hospital_id=%s, hospital_name=%s, cid_id=%s, cid_name=%s, medicine_item_id=%s, 
                         medicine_item_name=%s, dose=%s, nro_atendimiento = nro_atendimiento::int + 1, data_last_atendimineto=%s
                    WHERE patient_id=%s """, (
                        info['version'],
                        str(info['patient_id']),
                        info['patient_name'],
                        info['patient_medical_record'],
                        info['patient_covenat'],
                        str(info['patient_cpf']),
                        str(info['doctor_id']),
                        info['doctor_name'],
                        info['doctor_specialty'],
                        str(info['doctor_cpf']),
                        str(info['local_id']),
                        info['local_name'],
                        str(info['hospital_id']),
                        info['hospital_name'],
                        str(info['cid_id']),
                        info['cid_name'],
                        str(medicine_item_id),
                        info['medicine_item_name'],
                        info['dose'],
                        info['created_on'],
                        str(info['patient_id'])
                ))
                conection.conn.commit()
                cur.close()
                set_active(info['patient_id'])
            except:
                curs = conection.conn.cursor()
                curs.execute("ROLLBACK")
                conection.conn.commit()
                curs.close()
                return False
    return

def set_active(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("UPDATE public.patient SET status='ACTIVE' WHERE id = " + str(info))
        conection.conn.commit()
        cur.close()
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return False
    return

def appointments_set(info):


    cur = conection.conn.cursor()
    cur.execute("""SELECT id, name, medical_record, covenant, cpf, phone  FROM cobra.patient WHERE id = """ + str(info['patient']['id']))
    patient = cur.fetchall()

    cur.execute("""SELECT id, name FROM cobra.hospital WHERE id = """ + str(info['hospital']['id']))
    hospital = cur.fetchall()

    cur.execute("""SELECT id, name FROM cobra.cid WHERE id = """ + str(info['cid']['id']))
    cid = cur.fetchall()

    cur.execute("""SELECT doctor_id FROM cobra.login_user WHERE id = """ + str(info['doctorAtendimento']))
    doctorAtendimiento = cur.fetchall()

    cur.execute("""SELECT * FROM cobra.doctor WHERE id = """ + str(doctorAtendimiento[0][0]))
    doctor = cur.fetchall()

    cur.execute("""SELECT id, name FROM cobra.local WHERE id = """ + str(info['local']['id']))
    local = cur.fetchall()


    cur.execute("""SELECT * FROM cobra.doctor WHERE id = """ + str(info['doctorPatient']))
    doctorPresciptor = cur.fetchall()


    version = 0
    patient_id = patient[0][0]
    patient_name = patient[0][1]
    patient_medical_record = patient[0][2]
    patient_covenat = patient[0][3]
    patient_cpf = patient[0][4]
    patient_phone = patient[0][5]
    medicine = info['medicineItem']['name']
    hospital_id = hospital[0][0]
    hospital_name = hospital[0][1]
    login_user_id = doctor[0][0]
    my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    created_on = my_date.strftime("%Y/%m/%d %H:%M:%S")
    cid_id = cid[0][0]
    cid_name = cid[0][1]
    covenant = patient[0][3]
    local_id = info['local']['id']
    local_name = local[0][1]
    dose = info['dose']
    medicine_item_name = info['medicineItem']['name']
    doctor_id = doctor[0][0]
    doctor_name = doctor[0][4]
    doctor_specialty = doctor[0][3]
    doctor_cpf = doctor[0][7]
    doctor_atention_id = doctorPresciptor[0][0]
    doctor_atention_name = doctorPresciptor[0][4]
    doctor_atention_specialty = doctorPresciptor[0][3]
    doctor_atention_cpf = doctorPresciptor[0][7]
    attention_number = info['attentionNumber']



    cur.execute("""INSERT INTO cobra.appointment 
    ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone, medicine,
    hospital_id, hospital_name, login_user_id, created_on, cid_id, cid_name, covenant, local_id, local_name, dose,
    medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id, doctor_atention_name,
    doctor_atention_specialty, doctor_atention_cpf, attention_number)
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (version,patient_id,
                                                                                              patient_name, patient_medical_record,
                                                                                              patient_covenat, patient_cpf,
                                                                                              patient_phone,medicine,
                                                                                              hospital_id,hospital_name,
                                                                                              login_user_id,created_on,
                                                                                              cid_id,cid_name,covenant,
                                                                                              local_id,local_name, dose,
                                                                                              medicine_item_name, doctor_id,
                                                                                              doctor_name, doctor_specialty,
                                                                                              doctor_cpf, doctor_atention_id, doctor_atention_name,
                                                                                              doctor_atention_specialty, doctor_atention_cpf, attention_number))

    conection.conn.commit()
    cur.execute("""SELECT count(patient_id) FROM cobra.appointment_history WHERE patient_id = %s""", str(patient_id))
    appointment_history = cur.fetchall()


    if appointment_history[0][0] == 0:
        print("INSERT")
        # INSERT
        # INTO
        # cobra.appointment_history
        # ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, doctor_id,
        #  doctor_name, doctor_specialty, doctor_cpf, local_id, local_name, cid_id, cid_name, medicine_item_id,
        #  medicine_item_name, dose, nro_atendimiento, data_last_atendimineto)
        # VALUES(0, 0, '', '', '', '', 0, '', '', '', 0, '', 0, '', 0, '', '', 0, '');
        nro_atendimiento = 0
        cur.execute("""INSERT INTO cobra.appointment_history ("version", patient_id, patient_name, patient_medical_record,
                    patient_covenat, patient_cpf, doctor_id, doctor_name, doctor_specialty, doctor_cpf, local_id, 
                    local_name,hospital_id,hospital_name, cid_id, cid_name, medicine_item_id,medicine_item_name, dose, nro_atendimiento, data_last_atendimineto)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,null,%s,%s,%s,%s)""", (version, patient_id, patient_name,
                                                                                                  patient_medical_record, patient_covenat,
                                                                                                  patient_cpf, doctor_id, doctor_name,
                                                                                                  doctor_specialty, doctor_cpf, local_id, local_name,
                                                                                                  hospital_id, hospital_name, cid_id, cid_name,
                                                                                                  medicine_item_name, dose, nro_atendimiento,created_on))

        conection.conn.commit()
    else:
        cur.execute("""SELECT nro_atendimiento FROM cobra.appointment_history WHERE patient_id = %s""",
                    str(patient_id))
        appointment_history = cur.fetchall()

        nro_atendimiento = appointment_history[0][0] + 1
        cur.execute(""" UPDATE cobra.appointment_history SET
                    "version" = 0, patient_name = %s, patient_medical_record = %s, patient_covenat = %s,
                     patient_cpf = %s, doctor_id = %s, doctor_name = %s, doctor_specialty = %s, doctor_cpf = %s, 
                     local_id = %s, local_name = %s,hospital_id = %s, hospital_name = %s, cid_id = %s, cid_name = %s, 
                     medicine_item_name = %s, dose = %s, nro_atendimiento = %s, data_last_atendimineto = %s WHERE 
                     patient_id = %s""", (patient_name, patient_medical_record, patient_covenat, patient_cpf,
                                          doctor_id, doctor_name ,doctor_specialty, doctor_cpf ,local_id, local_name,hospital_id, hospital_name,
                                          cid_id, cid_name, medicine_item_name, dose, nro_atendimiento, created_on, patient_id))
        conection.conn.commit()


        print("UPDATE")
    cur.close()
    return

def appointments_update(info):
    print("UPDATE APPOINTMENT! ")
    medicines = info['medicineItem']['name'].upper()
    hospital_info = hospitals.get_hospital_by_id(info['hospital']['id'])
    hospital_id = hospital_info['id']
    hospital_name = hospital_info['name']
    vazio = False
    try:
        if len(info['cid']['id']) > 0:
            print("Soy vacio")
            print(info['cid']['id'])
        vazio = True
    except:
        print("no soy vacio")
        print(info['cid']['id'])
        vazio = False

    if vazio == False:
        info_cid = cid.get_cid_by_id(info['cid']['id'])
        cid_id = info_cid['id']
        cid_name = info_cid['name']
    else:
        cid_id = ''
        cid_name = ''

    # info_cid = cid.get_cid_by_id(info['cid']['id'])
    # cid_id = info_cid['id']
    # cid_name = info_cid['name']
    local_id = 0
    local_name = ''
    dose = str(info['dose']).upper()
    medicine_item_name = str(info['medicineItem']['name']).upper()
    info_doctor = doctors.get_doctors_by_id(info['doctor']['id'])
    doctor_id = info_doctor['id']
    doctor_name = info_doctor['name']
    covenant = info['covenant']
    specialty_info = specialty.get_specialty_by_id(info_doctor['specialty'])
    if not specialty_info:
        doctor_specialty = ''
        doctor_cpf = ''
    else:
        doctor_specialty = specialty_info['name']
        doctor_cpf = info_doctor['cpf']

    info_doctor_atention = doctors.get_doctors_by_id(info['doctorPatient'])
    doctor_atention_id = info_doctor_atention['id']
    doctor_atention_name = info_doctor_atention['name']

    specialty_info = specialty.get_specialty_by_id(info_doctor_atention['specialty'])
    if not specialty_info:
        doctor_atention_specialty = ''
        doctor_atention_cpf = ''
    else:
        doctor_atention_specialty = specialty_info['name']
        doctor_atention_cpf = info_doctor_atention['cpf']

    # doctor_atention_specialty = specialty_info['name']
    # doctor_atention_cpf = info_doctor_atention['cpf']

    attention_number = info['attentionNumber']

    aux = str(info['medicineItem']['name']).upper()
    medicine_info = medicine.get_medicine_by_name(aux)
    if not medicine_info:
        medicine.save_medicine_v2(aux)

    my_date = info['date']
    # 2021 - 11 - 06T01: 14:16.420 - 04: 00
    print(my_date)
    try:
        cr_date = datetime.datetime.strptime(my_date, '%Y-%m-%dT%H:%M:%S%z')
    except:
        cr_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
    created_on = cr_date.strftime("%Y-%m-%dT%H:%M:%S")

    cur = conection.conn.cursor()

    if cid_id == '':
        cur.execute("""
            UPDATE
            public.appointment_complete
            SET
                medicine = %s,
                hospital_id = %s, 
                hospital_name = %s, 
                created_on = %s, 
               
                cid_name = %s, 
                local_id = %s, 
                local_name = %s, 
                dose = %s,
                medicine_item_name = %s, 
                doctor_id = %s, 
                doctor_name = %s, 
                doctor_specialty = %s, 
                doctor_cpf = %s, 
                doctor_atention_id = %s, 
                doctor_atention_name = %s,
                doctor_atention_specialty = %s, 
                doctor_atention_cpf = %s, 
                attention_number = %s,
                covenant = %s
            WHERE id = %s""", (medicines,
                               hospital_id,
                               hospital_name,
                               created_on,
                               cid_name,
                               local_id,
                               local_name,
                               dose,
                               medicine_item_name,
                               doctor_atention_id,
                               doctor_atention_name,
                               doctor_atention_specialty,
                               doctor_atention_cpf,
                               doctor_id,
                               doctor_name,
                               doctor_specialty,
                               doctor_cpf,

                               attention_number,covenant, info['id']))
        conection.conn.commit()
        cur.close()
    else:
        cur.execute("""
                UPDATE
                public.appointment_complete
                SET
                    medicine = %s,
                    hospital_id = %s, 
                    hospital_name = %s, 
                    created_on = %s, 
                    cid_id = %s, 
                    cid_name = %s, 
                    local_id = %s, 
                    local_name = %s, 
                    dose = %s,
                    medicine_item_name = %s, 
                    doctor_id = %s, 
                    doctor_name = %s, 
                    doctor_specialty = %s, 
                    doctor_cpf = %s, 
                    doctor_atention_id = %s, 
                    doctor_atention_name = %s,
                    doctor_atention_specialty = %s, 
                    doctor_atention_cpf = %s, 
                    attention_number = %s,
                    covenant = %s
                WHERE id = %s""",
                    (medicines,
                     hospital_id,
                     hospital_name,
                     created_on,
                     cid_id,
                     cid_name,
                     local_id,
                     local_name,
                     dose,
                     medicine_item_name,
                     doctor_atention_id,
                     doctor_atention_name,
                     doctor_atention_specialty,
                     doctor_atention_cpf,
                     doctor_id,
                     doctor_name,
                     doctor_specialty,
                     doctor_cpf,

                     attention_number, covenant, info['id']))
        conection.conn.commit()
        cur.close()


def appointments_update_v2(info):

    # {'cid': {'id': 1}, 'medicineItem': {'id': 3}, 'hospital': {'id': 2},
    #  'doctorPatient': 26, 'doctorAppointment': 57, 'attentionNumber': '123123123',
    #  'dose': '2 AL DIA', 'id': '29', 'date': '2021-11-26T23:52:24Z', 'covenant': 'SULAMERICA'}
    id_ = info['id']
    info_hospital = hospitals.get_hospital_by_id(info['hospital']['id'])
    hospital_id = info_hospital['id']
    hospital_name = info_hospital['name']
    created_on = info['date']
    attention_number = info['attentionNumber']
    covenant = info['covenant']
    patient_covenat = covenant
    cid_id = ''
    cid_name = ''

    vazio = False
    try:
        if len(info['cid']['id']) > 0:
            print("Soy vacio")
            print(info['cid']['id'])
        vazio = True
    except:
        print("no soy vacio")
        print(info['cid']['id'])
        vazio = False

    if vazio == False:
        info_cid = cid.get_cid_by_id(info['cid']['id'])
        cid_id = info_cid['id']
        cid_name = info_cid['name']
    else:
        cid_id = ''
        cid_name = ''


    # info_cid = cid.get_cid_by_id(info['cid']['id'])
    # cid_id = info_cid['id'],
    # cid_name = info_cid['name']
    dose = info['dose']
    medicine_item_name = ''
    medicine_item_id = 0
    aux = str(info['medicineItem']['name']).upper()
    medicine_info = medicine.get_medicine_by_name(aux)
    if not medicine_info:
        medicine.save_medicine_v2(aux)
        aux_medicine = medicine.get_medicine_by_name(aux)
        medicine_item_name = aux_medicine['name']
        medicine_item_id = aux_medicine['id']

        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.appointment_complete SET
                        hospital_id = %s,
                        hospital_name = %s,
                        created_on = %s,
                        attention_number = %s,
                        covenant = %s,
                        patient_covenat = %s,
                        cid_id = %s,
                        cid_name = %s,
                        medicine_item_name = %s,
                        dose = %s
                        WHERE id = %s""", (hospital_id,
                                           hospital_name,
                                           created_on,
                                           attention_number,
                                           covenant,
                                           patient_covenat,
                                           cid_id,
                                           cid_name,
                                           medicine_item_name,
                                           dose, id_))
        conection.conn.commit()

        cur.execute("""SELECT patient_id FROM appointment_complete WHERE id = """ + id_)
        patient_id = cur.fetchone()[0]

        cur.execute("""UPDATE public.appointment_history SET
                            hospital_id = %s,
                            hospital_name = %s,
                            data_last_atendimineto = %s,

                            patient_covenat = %s,
                            cid_id = %s,
                            cid_name = %s,
                            medicine_item_id = %s,
                            medicine_item_name = %s,
                            dose = %s
                            WHERE patient_id = %s""", (hospital_id,
                                                       hospital_name,
                                                       created_on,

                                                       patient_covenat,
                                                       cid_id,
                                                       cid_name,
                                                       medicine_item_id,
                                                       medicine_item_name,
                                                       dose, patient_id))
        conection.conn.commit()
        cur.close()

    else:
        try:
            medicine_item_name = medicine_info['name']
            medicine_item_id = medicine_info['id']
            cur = conection.conn.cursor()
            if cid_id == '':
                cur.execute("""UPDATE public.appointment_complete SET
                                                hospital_id = %s,
                                                hospital_name = %s,
                                                created_on = %s,
                                                attention_number = %s,
                                                covenant = %s,
                                                patient_covenat = %s,
                                                cid_id = NULL,
                                                cid_name = %s,
                                                medicine_item_name = %s,
                                                dose = %s
                                                WHERE id = %s""", (hospital_id,
                                                                   hospital_name,
                                                                   created_on,
                                                                   attention_number,
                                                                   covenant,
                                                                   patient_covenat,
                                                                   cid_name,
                                                                   medicine_item_name,
                                                                   dose, id_))
                conection.conn.commit()

                cur.execute("""SELECT patient_id FROM appointment_complete WHERE id = """ + id_)
                patient_id = cur.fetchone()[0]

                cur.execute("""UPDATE public.appointment_history SET
                                                        hospital_id = %s,
                                                        hospital_name = %s,
                                                        data_last_atendimineto = %s,

                                                        patient_covenat = %s,
                                                        cid_id = NULL,
                                                        cid_name = %s,
                                                        medicine_item_id = %s,
                                                        medicine_item_name = %s,
                                                        dose = %s
                                                        WHERE patient_id = %s""", (hospital_id,
                                                                                   hospital_name,
                                                                                   created_on,

                                                                                   patient_covenat,

                                                                                   cid_name,
                                                                                   medicine_item_id,
                                                                                   medicine_item_name,
                                                                                   dose, patient_id))
                conection.conn.commit()
                cur.close()
            else:
                cur.execute("""UPDATE public.appointment_complete SET
                                                           hospital_id = %s,
                                                           hospital_name = %s,
                                                           created_on = %s,
                                                           attention_number = %s,
                                                           covenant = %s,
                                                           patient_covenat = %s,
                                                           cid_id = %s,
                                                           cid_name = %s,
                                                           medicine_item_name = %s,
                                                           dose = %s
                                                           WHERE id = %s""", (hospital_id,
                                                                              hospital_name,
                                                                              created_on,
                                                                              attention_number,
                                                                              covenant,
                                                                              patient_covenat,
                                                                              cid_id,
                                                                              cid_name,
                                                                              medicine_item_name,
                                                                              dose, id_))
                conection.conn.commit()

                cur.execute("""SELECT patient_id FROM appointment_complete WHERE id = """ + id_)
                patient_id = cur.fetchone()[0]

                cur.execute("""UPDATE public.appointment_history SET
                                                                   hospital_id = %s,
                                                                   hospital_name = %s,
                                                                   data_last_atendimineto = %s,

                                                                   patient_covenat = %s,
                                                                   cid_id = %s,
                                                                   cid_name = %s,
                                                                   medicine_item_id = %s,
                                                                   medicine_item_name = %s,
                                                                   dose = %s
                                                                   WHERE patient_id = %s""", (hospital_id,
                                                                                              hospital_name,
                                                                                              created_on,

                                                                                              patient_covenat,
                                                                                              cid_id,
                                                                                              cid_name,
                                                                                              medicine_item_id,
                                                                                              medicine_item_name,
                                                                                              dose, patient_id))
                conection.conn.commit()
                cur.close()
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return







    # cur.execute("""UPDATE public.appointment_complete SET
    #                 attention_number = %s, cid_id = %s, cid_name = %s, covenant = %s, created_on = %s, medicine_item_name = %s,
    #                 dose = %s, hospital_id = %s, hospital_name = %s, doctor_atention_id = %s, doctor_atention_name = %s,
    #                 doctor_atention_specialty = %s, doctor_atention_cpf = %s WHERE id = %s""", (attention_number, cid_id, cid_name, covenant,
    #                                                                       created_on, medicine_item_name, dose,
    #                                                                       hospital_id, hospital_name,doctor_atention_id,
    #                                                                       doctor_atention_name, doctor_atention_specialty,
    #                                                                       doctor_atention_cpf, id_))
    # cid_data = cid.get_cid_by_id(info['cid']['id'])
    # doctor = doctors.get_doctors_by_id(info['doctorPatient'])
    # medicine_data = medicine.get_medicine_by_id(info['medicineItem']['id'])
    # hospital_data = hospitals.get_hospital_by_id(info['hospital']['id'])
    #
    # doctor_atention_id = doctor['id']
    # doctor_atention_name = doctor['name']
    # doctor_atention_specialty = doctor['specialty']
    # doctor_atention_cpf = doctor['cpf']
    #
    # attention_number = info['attentionNumber']
    # cid_id = cid_data['id']
    # cid_name = cid_data['name']
    # covenant = info['covenant']
    # created_on = info['date']
    # medicine_item_name = medicine_data['name']
    # dose = info['dose']
    # hospital_id = hospital_data['id']
    # hospital_name = hospital_data['name']
    # id_ = info['id']
    #
    # print('dose', dose)
    # print('id', id_)
    #
    # cur = conection.conn.cursor()
    # cur.execute("""UPDATE public.appointment_complete SET
    #    attention_number = %s, cid_id = %s, cid_name = %s, covenant = %s, created_on = %s, medicine_item_name = %s,
    #    dose = %s, hospital_id = %s, hospital_name = %s, doctor_atention_id = %s, doctor_atention_name = %s,
    #     doctor_atention_specialty = %s, doctor_atention_cpf = %s WHERE id = %s""", (attention_number, cid_id, cid_name, covenant,
    #                                                                       created_on, medicine_item_name, dose,
    #                                                                       hospital_id, hospital_name,doctor_atention_id,
    #                                                                       doctor_atention_name, doctor_atention_specialty,
    #                                                                       doctor_atention_cpf, id_))
    #
    # conection.conn.commit()
    #
    # cur.execute("""SELECT patient_id FROM public.appointment_complete WHERE id = """ + str(id_))
    # records = cur.fetchall()
    #
    #
    # cur.execute("""UPDATE public.appointment_history SET
    #                cid_id = %s, cid_name = %s, data_last_atendimineto = %s, medicine_item_name = %s,
    #                dose = %s, hospital_id = %s, hospital_name = %s,doctor_id = %s, doctor_name = %s, doctor_specialty = %s,
    #                doctor_cpf = %s WHERE patient_id = %s""",
    #             (cid_id, cid_name, created_on, medicine_item_name, dose, hospital_id,
    #              hospital_name, doctor_atention_id, doctor_atention_name, doctor_atention_specialty, doctor_atention_cpf, records[0][0]))
    # conection.conn.commit()
    # cur.close()

def appointments_by_user(token, type):
    info = auth.validate_token(token,  output=True)
    if info:

        if type['type'] == 'MY_PATIENTS':
            payload = []
            content = {}

            #PACIENTES
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            medical_type, 
                            creation_date, 
                            id, 
                            local_id,
                            "name",
                            status,
                            doctor_id,
                            medical_record
                           FROM public.patient WHERE doctor_id = """ + str(info['doctor_id']) + """ORDER BY creation_date desc""")
            records = cur.fetchall()
            cur.close()

            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
                if data[5] == 'INITIAL':
                    attentionNumber = 'Paciente Nuevo'
                else:
                    attentionNumber = data[7]

                content = {
                    'attentionNumber': attentionNumber,
                    'createdOn': data[1],
                    'doctor':  info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[2],
                    'local': data[3],
                    'patient': data[4],
                    'patientDoctor': '',
                    'patientDoctorStatus': {
                        'enumType': '',
                        'name': ''
                    }
                }
                payload.append(content)
                content = {}
            #ATENCIONES
            # cur = conection.conn.cursor()
            # cur.execute("""SELECT attention_number, created_on, doctor_name, id,
            #                 hospital_name, patient_name,  doctor_id , doctor_atention_id
            #                 FROM public.appointment_complete WHERE doctor_id = """ + str(info['doctor_id']) + """ORDER BY created_on desc""")
            # records = cur.fetchall()
            # cur.close()
            #
            # for data in records:
            #     info_doctor_prescriptor = doctors.get_doctors_by_id(data[6])
            #     info_doctor_platonista = doctors.get_doctors_by_id(data[7])
            #     content = {
            #         'attentionNumber': data[0],
            #         'createdOn': data[1],
            #         'doctor':  info_doctor_prescriptor['name'],
            #         'doctorStatus': {
            #             'enumType': "cobra.api.emuns.common.GenericStatus",
            #             'name': info_doctor_prescriptor['status']
            #         },
            #         'id': data[3],
            #         'local': data[4],
            #         'patient': data[5],
            #         'patientDoctor': info_doctor_platonista['name'],
            #         'patientDoctorStatus': {
            #             'enumType': "cobra.api.emuns.common.GenericStatus",
            #             'name': info_doctor_platonista['status']
            #         }
            #     }
            #     payload.append(content)
            #     content = {}
            return payload

        if type['type'] == 'MY_ATTENTIONS':
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_atention_id = """ + str(info['doctor_id'])+ """ ORDER BY created_on desc""")
            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
                info_doctor_platonista = doctors.get_doctors_by_id_v2(data[7])
                content = {
                    'attentionNumber': data[0],
                    'createdOn': data[1],
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload

def appointments_by_data(token, type):
    info = auth.validate_token(token,  output=True)
    if info:

        if type['type'] == 'MY_PATIENTS':
            from_date = datetime.strptime(type['from'], '%Y/%m/%d')
            to_date = datetime.strptime(type['to'], '%Y/%m/%d')
            cur = conection.conn.cursor()
            cur.execute("""SELECT attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_id = %s
                            AND created_on::DATE BETWEEN %s  AND %s""", (str(info['doctor_id']),  str(from_date),
                                                                   str(to_date)))




            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id(data[6])
                info_doctor_platonista = doctors.get_doctors_by_id(data[7])
                content = {
                    'attentionNumber': data[0],
                    'createdOn': data[1],
                    'doctor':  info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_platonista['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_platonista['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload

        if type['type'] == 'MY_ATTENTIONS':
            from_date = datetime.datetime.strptime(type['from'], '%d/%m/%Y')
            to_date = datetime.datetime.strptime(type['to'], '%d/%m/%Y')

            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_atention_id = %s
                            AND created_on::DATE BETWEEN %s AND %s """, (str(info['doctor_id']), str(from_date), str(to_date)))


            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id(data[6])
                info_doctor_platonista = doctors.get_doctors_by_id(data[7])
                content = {
                    'attentionNumber': data[0],
                    'createdOn': data[1],
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload

def get_data():
    cids = cid.get_cid()
    doctor = doctors.get_doctors()
    hospital = hospitals.get_hospitals()
    locals = local.get_locals()
    medicines = medicine.get_medicine()
    content = {
        'cids': cids,
        'doctors': doctor,
        'hospitals': hospital,
        'locals': locals,
        'medicines': medicines,
    }

    return content

def get_data_appointments_by_id(id):
    print(id, 'ID')
    cur = conection.conn.cursor()
    cur.execute("""SELECT attention_number, cid_id, cid_name, covenant, patient_cpf,
                          created_on, doctor_name, doctor_id, doctor_atention_name, doctor_atention_id,
                          dose, hospital_id, id, medicine_item_name, patient_name
                           FROM public.appointment_complete WHERE id = """ + str(id))
    records = cur.fetchall()
    print(records)
    cur.close()
    content = {}

    cur = conection.conn.cursor()
    cur.execute("""select p.url from public.appointment_photo pp 
                join public.photo p on pp.photo_id = p.id where pp.appointment_other_photos_id = """ + str(id))
    photos = cur.fetchall()
    list_photos = []
    if len(photos) > 0:
        for i in photos:
            list_photos.append({'url': i[0]})

    if len(records) != 0:
        cids = {}
        print(records[0][1])
        if records[0][1] is None:
            content = {
                'id': [''],
                'name': [''],
                'status': ['']
            }
            cids = content
        else:
            print("dentro", records[0][1])
            cids = cid.get_cid_by_id(records[0][1])


        doctor_presciptor = doctors.get_doctors_by_id_v2(records[0][7])
        doctor = doctors.get_doctors_by_id_v2(records[0][9])

        myPatient = False
        if doctor['id'] == doctor_presciptor['id']:
            myPatient = True

        medicines = medicine.get_medicine_by_name(records[0][13])
        print(medicines)

        createdOn = records[0][5].strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        date = records[0][5].strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        dateIOS = records[0][5].strftime("%Y-%m-%dT%H:%M:%SZ")
        dateStr = str(records[0][5].strftime("%Y-%m-%d %H:%M:%S"))
        for i in records:
            cid_id = cids['id'],
            cid_name = cids['name'],
            cid_status = cids['status']

            try:
                medicines_name = medicines['name']
                medicines_status = medicines['status']
                medicines_id = medicines['id']
            except:
                medicines_name = ''
                medicines_status = ''
                medicines_id = ''

            try:
                doctor_presciptor_name = doctor_presciptor['name'],
                doctor_presciptor_status = doctor_presciptor['status'],
                doctor_presciptor_id = doctor_presciptor['id']
            except:
                doctor_presciptor_name = ''
                doctor_presciptor_status = ''
                doctor_presciptor_id = ''

            try:
                doctor_name = doctor['name'],
                doctor_status = doctor['status'],
                doctor_id = doctor['id']
            except:
                doctor_name = ''
                doctor_status = ''
                doctor_id = ''

            # if cids['status'] == "DELETED":
            #     cid_id = ''
            #     cid_name = ''
            #     cid_status = ''
            # else:
            #     cid_id = cids['id'],
            #     cid_name = cids['name'],
            #     cid_status = cids['status']
            #
            # if medicines['status'] == "DELETED":
            #     medicines_name = ''
            #     medicines_status = ''
            #     medicines_id = ''
            # else:
            #     medicines_name = medicines['name']
            #     medicines_status = medicines['status']
            #     medicines_id = medicines['id']
            #
            # if doctor_presciptor['status'] == "DELETED":
            #     doctor_presciptor_name = ''
            #     doctor_presciptor_status = ''
            #     doctor_presciptor_id = ''
            # else:
            #     doctor_presciptor_name = doctor_presciptor['name'],
            #     doctor_presciptor_status = doctor_presciptor['status'],
            #     doctor_presciptor_id = doctor_presciptor['id']
            #
            # if doctor['status'] == "DELETED":
            #     doctor_name = ''
            #     doctor_status = ''
            #     doctor_id = ''
            # else:
            #     doctor_name = doctor['name'],
            #     doctor_status = doctor['status'],
            #     doctor_id = doctor['id']


            content = {
                'attentionNumber': i[0],
                'cid': {
                    'id': cid_id[0],
                    'name': cid_name[0],
                    'status': cid_status[0]
                },
                'covenant': i[3],
                'cpf': i[4],
                'createdOn': createdOn,
                'date': date,
                'dateIOS': dateIOS,
                'dateStr': dateStr,
                'doctorAppointment': doctor['id'],
                'doctorPatient': doctor_presciptor['id'],
                'dose': i[10],
                'hospital': {'id': i[11]},
                'hospitalId': i[11],
                'id': id,
                'medicineItem': {
                    'name': medicines_name,
                    'status': medicines_status,
                    'id': medicines_id
                },
                'myPatient': myPatient,
                'newPatient': False,
                'patient': i[14],
                'presciptor': {
                    'name': doctor_presciptor_name,
                    'status': doctor_presciptor_status,
                    'id': doctor_presciptor_id
                },
                'doctor': {
                    'name': doctor_name,
                    'status': doctor_status,
                    'id': doctor_id
                },
                'otherPhotos': list_photos
        }

    print(content)
    return content


def appointments_search(info):
    payload = []
    # if info is None:
    if len(info) == 1:
        try:
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            app.id, 
                            app.attention_number, 
                            app.patient_name, 
                            app.doctor_name, 
                            app.doctor_atention_name, 
                            app.hospital_name,
                            app.created_on, 
                            d.status as status_doctor, 
                            p.status as status_atention_doctor, 
                            h.status as status_hospital
                           FROM public.appointment_complete app
                           join public.doctor d on app.doctor_id = d.id 
                           join public.doctor p on app.doctor_atention_id = p.id 
                           join public.hospital h on app.hospital_id = h.id 
                           ORDER BY created_on desc""")
            records = cur.fetchall()
            cur.close()
            content = {}
            for i in records:
                # info_doctor = doctors.get_doctors_by_id(i[7])
                # info_doctorPatient = doctors.get_doctors_by_id(i[8])
                # info_hospital = hospitals.get_hospital_by_id(i[9])
                content = {
                    'newPatient': False,
                    'attentionNumber': i[1],
                    'patient': i[2],
                    'doctor': i[3],
                    'doctorStatus': i[7],
                    'doctorPatient': i[4],
                    'patientDoctorStatus': i[8],
                    'hospital': i[5],
                    'hospitalStatus': i[9],
                    'createdOn': i[6].strftime("%d/%m/%Y %H:%M"),
                    'id': i[0],
                }
                payload.append(content)
                content = {}
            return payload
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return payload

    else:

        condition_hospital = ""
        coma_hopsital = ""

        condition_doctor = ""
        coma_doctor = ""

        condition_prescriptor = ""
        coma_prescriptor = ""

        condition_patient = ""
        coma_patient = ""

        condition_cpf = ""
        coma_cpf = ""
        where = ""
        # {'hospital': {'id': 3}, 'doctor': {'id': 3}, 'prescriptor': {'id': 1}, 'cpf': '123.123.123-12',
        #  'from': '23/11/2021', 'to': '23/11/2021'
        try:
            if (info['hospital']):
                print("Estoy buscando por hospital")
                condition_hospital = " hospital_id = " + str(info['hospital']['id'])
                if condition_hospital != "":
                    coma_hopsital = ' AND '
                where = " where "
        except:
            print("Hospital not working")

        try:
            if (info['doctor']):
                print("Estoy buscando por doctor")
                condition_doctor = " doctor_id = " + str(info['doctor']['id'])
                if condition_doctor != "":
                    coma_doctor = ' AND '
                where = " where "
        except:
            print("Hospital not working")

        try:
            if (info['prescriptor']):
                print("Estoy buscando por doctor")
                condition_prescriptor = " doctor_atention_id = " + str(info['prescriptor']['id'])
                if condition_prescriptor != "":
                    coma_prescriptor = ' AND '
                where = " where "
        except:
            print("Hospital not working")

        try:
            if (info['patient']):
                print("Estoy buscando por patient")
                condition_patient = " patient_id = " + str(info['patient']['id'])
                if condition_patient != "":
                    coma_patient = ' AND '
                where = " where "
        except:
            print("Hospital not working")

        try:
            if (info['cpf']):
                print("Estoy buscando por doctor")
                condition_cpf = " patient_cpf = '" + str(info['cpf'] + "'")
                if condition_cpf != "":
                    coma_cpf = ' AND '
                where = " where "
        except:
            print("Hospital not working")

        create_date = ""
        condition_dateFrom = ""
        coma_dateFrom  = ""
        condition_dateTo = ""
        coma_dateTo = ""


        try:
            date_time_obj = datetime.datetime.strptime(info['from'], '%d/%m/%Y')
            date_time_to = datetime.datetime.now()
            where = " where "
            create_date = " created_on BETWEEN "
            condition_dateFrom = " '" + str(date_time_obj) + "' "
            coma_dateFrom = " AND "
            condition_dateTo = " '" + str(date_time_to) + "' "
        except:
            print("date not workiing")

        try:
            where = " where "
            date_time_obj = datetime.datetime.strptime(info['to'],'%d/%m/%Y')
            create_date = " created_on::DATE BETWEEN "
            if condition_dateFrom == "":
                condition_dateFrom = " '" + str(date_time_obj) +  "' "

            coma_dateFrom = " AND "
            condition_dateTo = " '" + str(date_time_obj) +  "' "
        except:
            print("date not workiing")




        # select *
        # from cobra.appointment where
        # created_on
        # BETWEEN
        # '2021-11-23' and '2021-11-23'

        # cur = conection.conn.cursor()
        # cur.execute("""SELECT id, attention_number, patient_name, doctor_name, doctor_atention_name, hospital_name ,created_on
        #                            FROM public.appointment_complete """ + where + condition_hospital + coma_hopsital + condition_doctor + coma_doctor +
        #             condition_prescriptor + coma_prescriptor + condition_patient + coma_patient + condition_cpf + create_date +
        #             str(condition_dateFrom) + coma_dateFrom + str(condition_dateTo) + "ORDER BY created_on desc")
        # records = cur.fetchall()
        # cur.close()
        # content = {}
        # for i in records:
        #     print('date', i[6].strftime("%Y-%m-%d %H:%M:%S"))
        #     content = {
        #         'newPatient': False,
        #         'attentionNumber': i[1],
        #         'patient': i[2],
        #         'doctor': i[3],
        #         'doctorPatient': i[4],
        #         'hospital': i[5],
        #         'createdOn': str(i[6].strftime("%d/%m/%Y %H:%M")),
        #         'id': i[0],
        #     }
        #     payload.append(content)
        #     content = {}
        # return payload

        try:
            cur = conection.conn.cursor()
            print("""SELECT id, attention_number, patient_name, doctor_name, doctor_atention_name, hospital_name ,created_on
                           FROM public.appointment_complete """ + where + condition_hospital + coma_hopsital + condition_doctor + coma_doctor +
                        condition_prescriptor + coma_prescriptor + condition_patient + coma_patient + condition_cpf + create_date +
                        str(condition_dateFrom) + coma_dateFrom + str(condition_dateTo) + "ORDER BY created_on desc")


            cur.execute("""SELECT id, attention_number, patient_name, doctor_name, doctor_atention_name, hospital_name ,created_on
                           FROM public.appointment_complete """ + where + condition_hospital + coma_hopsital + condition_doctor + coma_doctor +
                        condition_prescriptor + coma_prescriptor + condition_patient + coma_patient + condition_cpf + coma_cpf +  create_date +
                        str(condition_dateFrom) + coma_dateFrom + str(condition_dateTo) + "ORDER BY created_on desc")
            records = cur.fetchall()
            cur.close()
            content = {}
            for i in records:
                print('date',i[6].strftime("%Y-%m-%d %H:%M:%S"))
                content = {
                    'newPatient': False,
                    'attentionNumber': i[1],
                    'patient': i[2],
                    'doctor': i[3],
                    'doctorPatient': i[4],
                    'hospital': i[5],
                    'createdOn': str(i[6].strftime("%d/%m/%Y %H:%M")),
                    'id': i[0],
                }
                payload.append(content)
                content = {}
            return payload
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return payload


    return

def appointments_delete(info):

    cur = conection.conn.cursor()
    cur.execute("""DELETE FROM public.appointment_complete WHERE id = """ + str(info))
    conection.conn.commit()
    cur.close()
    return

def suporte():
    cur = conection.conn.cursor()
    cur.execute("""SELECT patient_name, doctor_name, hospital_name, cid_name, medicine_item_name, dose, nro_atendimiento,
                    id, cid_id, medicine_item_id, hospital_id, data_last_atendimineto, doctor_id 
                    FROM public.appointment_history  ORDER BY patient_name asc""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        # print(i)
        if i[6] > 0:

            doctor = ''
            doctorid = ''
            cidName = ''
            cid_id = ''
            medicineName = ''
            medicineId = ''
            hospitalName = ''
            hospitalId = ''

            if i[12] is not None:
                vDoctor = doctors.get_doctors_by_id(i[12])
                if vDoctor['status'] == 'DELETED':
                    doctor = ''
                    doctorid = ''
                else:
                    doctor = i[1]
                    doctorid = i[12]
            if i[8] is not None:
                vCid = cid.get_cid_by_id(i[8])
                if vCid['status'] == 'DELETED':
                    cidName = ''
                    cid_id = ''
                else:
                    cidName = i[3]
                    cid_id = i[8]
            if i[9] is not None:
                vMedicine = medicine.get_medicine_by_id(i[9])
                if vMedicine['status'] == 'DELETED':
                    medicineName = ''
                    medicineId = ''
                else:
                    medicineName = i[4]
                    medicineId = i[9]
            if i[10] is not None:
                vHospital = hospitals.get_hospital_by_id(i[10])
                if vHospital['status'] == 'DELETED':
                    hospitalName = ''
                    hospitalId = ''
                else:
                    hospitalName = i[2]
                    hospitalId = i[10]

            content = {
                "patientName": i[0],
                "doctorName": doctor,
                "hospitalName": hospitalName,
                "cidName": cidName,
                "medicineName": medicineName,
                "dose": i[5],
                "nroAtendimiento": i[6],
                "id": i[7],
                'cidId': cid_id,
                'medicineId': medicineId,
                'hospitalId': hospitalId,
                'lastAtention': i[11],
                'doctorId': doctorid
            }

        else:

            content = {
                "patientName": i[0],
                "doctorName": i[1],
                "hospitalName": i[2],
                "cidName": i[3],
                "medicineName": i[4],
                "dose": i[5],
                "nroAtendimiento": i[6],
                "id": i[7],
                'cidId': i[8],
                'medicineId': i[9],
                'hospitalId': i[10],
                'lastAtention': i[11],
                'doctorId': i[12]
            }

        payload.append(content)
        content = {}

    return payload

def suporte_update(info):
    # cidId: 1
    # doctorId: 26
    # dose: "1 AL DIA"
    # hospitalId: 2
    # id: 26
    # lastAtention: "Mon, 29 Nov 2021 19:01:40 GMT"
    # medicineId: 5
    # nroAtention: ""
    # patientName: "ANA SUELI PEREIRA GARCIA"
    cid_data = cid.get_cid_by_id(info['cidId'])
    doctor_data = doctors.get_doctors_by_id(info['doctorId'])
    dose = info['dose']
    hospital_data = hospitals.get_hospital_by_id(info['hospitalId'])
    medicine_data = medicine.get_medicine_by_id(info['medicineId'])

    print(cid_data)
    print(doctor_data)
    print(dose)
    print(hospital_data)
    print(medicine_data)

    # {'id': 1, 'name': 'M0512312', 'status': 'DELETE'}
    # {'id': 26, 'cpf': None, 'specialty': {'name': None}, 'status': 'ACTIVE', 'name': 'Jayme Fogagnolo Cobra'}
    # 1 AL DIA
    # {'id': 2, 'version': 0, 'name': 'IFOR-2', 'status': None}
    # {'id': 2, 'name': 'ACTEMRA EV', 'status': 'ACTIVE'}
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.appointment_history SET 
                        cid_id= %s, 
                        cid_name= %s,
                        doctor_id= %s, 
                        doctor_name= %s, 
                        doctor_specialty= %s, 
                        doctor_cpf= %s, 
                        hospital_id= %s, 
                        hospital_name= %s, 
                        medicine_item_id= %s, 
                        medicine_item_name= %s, 
                        dose= %s
                        WHERE id = %s""", (
                        cid_data['id'],
                        cid_data['name'],
                        doctor_data['id'],
                        doctor_data['name'],
                        doctor_data['specialty']['name'],
                        doctor_data['cpf'],
                        hospital_data['id'],
                        hospital_data['name'],
                        medicine_data['id'],
                        medicine_data['name'],
                        dose, info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return False

def suporte_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT patient_name, doctor_name, hospital_name, cid_name, medicine_item_name, dose, nro_atendimiento,
                    id, cid_id, medicine_item_id, hospital_id, data_last_atendimineto, doctor_id 
                    FROM public.appointment_history  ORDER BY patient_name asc""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        print(i)
        content = {
            "patientName": i[0],
            "doctorName": i[1],
            "hospitalName": i[2],
            "cidName": i[3],
            "medicineName": i[4],
            "dose": i[5],
            "nroAtendimiento": i[6],
        }
        payload.append(content)
        content = {}

    return payload

def appointments_search_download(info):

    payload = []
    if len(info) == 0:
        cur = conection.conn.cursor()
        cur.execute("""SELECT 
            attention_number,
            patient_name, 
            patient_medical_record, 
            patient_covenat, 
            patient_cpf, 
            patient_phone, 
            medicine, 
            hospital_name, 
            created_on, 
            cid_id, 
            cid_name, 
            covenant, 
            local_name, 
            medicine_item_name, 
            dose, 
            doctor_name, 
            doctor_specialty, 
            doctor_cpf, 
            doctor_atention_name, 
            doctor_atention_specialty, 
            doctor_atention_cpf
            FROM public.appointment_complete ORDER BY ORDER BY created_on desc""")
        records = cur.fetchall()
        cur.close()
        content = {}
        for i in records:

            content = {
                'attention_number': i[0],
                'patient_name': i[1],
                'patient_medical_record': i[2],
                'patient_covenat': i[3],
                'patient_cpf': i[4],
                'patient_phone': i[5],
                'medicine': i[6],
                'hospital_name': i[7],
                'created_on': i[8].strftime("%Y/%m/%d %H:%M:%S"),
                'cid_name': i[10],
                'covenant': i[11],
                'local_name': i[12],
                'medicine_item_name': i[13],
                'dose': i[14],
                'doctor_name': i[15],
                'doctor_specialty': i[16],
                'doctor_cpf': i[17],
                'doctor_atention_name': i[18],
                'doctor_atention_specialty': i[19],
                'doctor_atention_cpf': i[20],
            }
            payload.append(content)
            content = {}
        return payload

    else:

        condition_hospital = ""
        coma_hopsital = ""

        condition_doctor = ""
        coma_doctor = ""

        condition_prescriptor = ""
        coma_prescriptor = ""

        condition_patient = ""
        coma_patient = ""

        condition_cpf = ""
        where = ""
        # {'hospital': {'id': 3}, 'doctor': {'id': 3}, 'prescriptor': {'id': 1}, 'cpf': '123.123.123-12',
        #  'from': '23/11/2021', 'to': '23/11/2021'
        try:
            if (info['hospital']):
                print("Estoy buscando por hospital")
                condition_hospital = " hospital_id = " + str(info['hospital']['id'])
                where = " where "
        except:
            print("Hospital not working")
            where = ""

        try:
            if (info['doctor']):
                print("Estoy buscando por doctor")
                condition_doctor = " doctor_id = " + str(info['doctor']['id'])
                if condition_hospital != "":
                    coma_hopsital = ' AND '
                where = " where "
        except:
            print("DOCTOR not working")
            where = ""

        try:
            if (info['prescriptor']):
                print("Estoy buscando por doctor")
                condition_prescriptor = " doctor_atention_id = " + str(info['prescriptor']['id'])
                if condition_doctor != "":
                    coma_doctor = ' AND '
                where = " where "
        except:
            print("PRESCRIPTOR not working")
            where = ""

        try:
            if (info['patient']):
                print("Estoy buscando por patient")
                condition_patient = " patient_id = " + str(info['patient']['id'])
                if condition_prescriptor != "":
                    coma_prescriptor = ' AND '
                where = " where "
        except:
            print("PATIENT not working")
            where = ""

        try:
            if (info['cpf']):
                print("Estoy buscando por doctor")
                condition_cpf = " patient_cpf = '" + str(info['cpf'] + "'")
                if condition_patient != "":
                    coma_patient = ' AND '
                where = " where "
        except:
            print("CPF not working")
            where = ""

        create_date = ""
        condition_dateFrom = ""
        coma_dateFrom  = ""
        condition_dateTo = ""
        coma_dateTo = ""


        try:
            date_time_obj = datetime.strptime(info['from'], '%d/%m/%Y')
            where = " where "
            create_date = " created_on BETWEEN "
            condition_dateFrom = "'" + str(date_time_obj) +  "'"
            coma_dateFrom = " AND "
            condition_dateTo = "'" + str(date_time_obj) +  "'"
        except:
            print("date not workiing")
            where = ""

        try:
            where = " where "
            date_time_obj = datetime.strptime(info['to'],'%d/%m/%Y')
            create_date = " created_on BETWEEN "
            if condition_dateFrom == "":
                condition_dateFrom = "'" + str(date_time_obj) +  "'"

            coma_dateFrom = " AND "
            condition_dateTo = "'" + str(date_time_obj) +  "'"
        except:
            print("date not workiing")
            where = ""



        # select *
        # from cobra.appointment where
        # created_on
        # BETWEEN
        # '2021-11-23' and '2021-11-23'

        try:
            cur = conection.conn.cursor()
            cur.execute("""SELECT attention_number,
                            patient_name, 
                            patient_medical_record, 
                            patient_covenat, 
                            patient_cpf, 
                            patient_phone, 
                            medicine, 
                            hospital_name, 
                            created_on, 
                            cid_id, 
                            cid_name, 
                            covenant, 
                            local_name, 
                            medicine_item_name, 
                            dose, 
                            doctor_name, 
                            doctor_specialty, 
                            doctor_cpf, 
                            doctor_atention_name, 
                            doctor_atention_specialty, 
                            doctor_atention_cpf
                           FROM public.appointment_complete """ + where + condition_hospital + coma_hopsital + condition_doctor + coma_doctor +
                        condition_prescriptor + coma_prescriptor + condition_patient + coma_patient + condition_cpf + create_date +
                        str(condition_dateFrom) + coma_dateFrom + str(condition_dateTo) + "ORDER BY created_on desc")
            records = cur.fetchall()
            cur.close()
            content = {}
            for i in records:
                content = {
                    'attention_number': i[0],
                    'patient_name': i[1],
                    'patient_medical_record': i[2],
                    'patient_covenat': i[3],
                    'patient_cpf': i[4],
                    'patient_phone': i[5],
                    'medicine': i[6],
                    'hospital_name': i[7],
                    'created_on': i[8].strftime("%Y/%m/%d %H:%M:%S"),
                    'cid_name': i[10],
                    'covenant': i[11],
                    'local_name': i[12],
                    'medicine_item_name': i[13],
                    'dose': i[14],
                    'doctor_name': i[15],
                    'doctor_specialty': i[16],
                    'doctor_cpf': i[17],
                    'doctor_atention_name': i[18],
                    'doctor_atention_specialty': i[19],
                    'doctor_atention_cpf': i[20],
                }
                payload.append(content)
                content = {}
            return payload
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return payload
    return

def appointments_download_by_id(id):
    payload = []
    cur = conection.conn.cursor()
    cur.execute("""SELECT 
               attention_number,
               patient_name, 
               patient_medical_record, 
               patient_covenat, 
               patient_cpf, 
               patient_phone, 
               medicine, 
               hospital_name, 
               created_on, 
               cid_id, 
               cid_name, 
               covenant, 
               local_name, 
               medicine_item_name, 
               dose, 
               doctor_name, 
               doctor_specialty, 
               doctor_cpf, 
               doctor_atention_name, 
               doctor_atention_specialty, 
               doctor_atention_cpf
               FROM public.appointment_complete WHERE id =""" + str(id))
    records = cur.fetchall()
    cur.close()
    for i in records:

        content = {
            'attention_number': i[0],
            'patient_name': i[1],
            'patient_medical_record': i[2],
            'patient_covenat': i[3],
            'patient_cpf': i[4],
            'patient_phone': i[5],
            'medicine': i[6],
            'hospital_name': i[7],
            'created_on': i[8].strftime("%Y/%m/%d %H:%M:%S"),
            'cid_name': i[10],
            'covenant': i[11],
            'local_name': i[12],
            'medicine_item_name': i[13],
            'dose': i[14],
            'doctor_name': i[15],
            'doctor_specialty': i[16],
            'doctor_cpf': i[17],
            'doctor_atention_name': i[18],
            'doctor_atention_specialty': i[19],
            'doctor_atention_cpf': i[20],
        }
        payload.append(content)
        content = {}
    return payload


#Mobile
def insert_appointments_mobile(info, token):
    # {'patient': {'id': 129},
    # 'cid': {'id': ''},
    # 'medicineItem': {'name': 'ACTEMRA EV'},
    # 'attentionNumber': '090909090',
    # 'date': '2021-12-15T05:23:38.527Z',
    # 'dose': '1 al dia',
    # 'local': {'id': ''},
    # 'covenant': '',
    # 'doctorPatient': 12,
    # 'hospital': {'id': 7},
    # 'otherPhotos': []}

    print("INSERTANDO APPOINTMENT! ")
    print(info, 'INFO')
    patient_info = patients.get_info_patients(info['patient']['id'])
    version = 0
    patient_id = patient_info['id']



    if patient_info['name'] is not None:
        patient_name = patient_info['name'].upper()
    else:
        patient_name = ''


    if patient_info['attentionNumber'] is not None:
        patient_medical_record = patient_info['attentionNumber'].upper()
    else:
        patient_medical_record = ''

    if patient_info['covenant'] is not None:
        patient_covenat = patient_info['covenant'].upper()
    else:
        patient_covenat = ''
    patient_cpf = patient_info['cpf']
    patient_phone = patient_info['phone']
    medicines = info['medicineItem']['name'].upper()
    hospital_info = hospitals.get_hospital_by_id(info['hospital']['id'])
    hospital_id = hospital_info['id']
    hospital_name = hospital_info['name']

    info_user = validate_token(token, True)
    login_user_id = info_user['id']
    cid_id = ''
    cid_name = ''

    if info['cid']['id'] != "":
        cid_id = ''
        cid_name = ''

    if info['cid']['id'] is None:
        cid_id = ''
        cid_name = ''

    if info['cid']['id'] != "" and info['cid']['id'] is not None:
        info_cid = cid.get_cid_by_id(info['cid']['id'])
        cid_id = info_cid['id']
        cid_name = info_cid['name']


    if patient_info['covenant'] is not None:
        covenant = patient_info['covenant'].upper()
    else:
        covenant = ''


    local_id = 0
    local_name = ''

    dose = str(info['dose']).upper()
    medicine_item_name = str(info['medicineItem']['name']).upper()

    info_doctor = doctors.get_doctors_by_id(patient_info['doctor_id'])
    doctor_id = patient_info['doctor_id']
    doctor_name = info_doctor['name']

    try:
        specialty_info = specialty.get_specialty_by_id(info_doctor['specialty'])
        doctor_specialty = specialty_info['name']
    except:
        doctor_specialty = ''
    doctor_cpf = info_doctor['cpf']

    info_doctor_atention = doctors.get_doctors_by_id(info_user['doctor_id'])
    doctor_atention_id = info_doctor_atention['id']
    doctor_atention_name = info_doctor_atention['name']
    try:
        specialty_info = specialty.get_specialty_by_id(info_doctor_atention['specialty'])
        doctor_atention_specialty = specialty_info['name']
    except:
        doctor_atention_specialty = ''

    doctor_atention_cpf = info_doctor_atention['cpf']

    attention_number = info['attentionNumber']

    aux = str(info['medicineItem']['name']).upper()
    medicine_info = medicine.get_medicine_by_name(aux)
    if not medicine_info:
        medicine.save_medicine_v2(aux)
    # my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    my_date = info['date']
    # 2021 - 11 - 06T01: 14:16.420 - 04: 00
    cr_date = datetime.datetime.strptime(my_date, '%Y-%m-%dT%H:%M:%S.%f%z')
    print(cr_date)
    date = cr_date.astimezone(pytz.timezone('America/Sao_Paulo'))

    cr_date = cr_date.strftime("%Y-%m-%dT%H:%M:%S")
    created_on = date.strftime("%Y-%m-%dT%H:%M:%S")
    print(created_on)

    if cid_id == '':
        try:
            cur = conection.conn.cursor()
            cur.execute("""
                        INSERT
                        INTO
                        public.appointment_complete
                        ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone, medicine,
                         hospital_id, hospital_name, login_user_id, created_on, covenant, local_id, local_name, dose,
                         medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id, doctor_atention_name,
                         doctor_atention_specialty, doctor_atention_cpf, attention_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """, (
                version, patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone,
                medicines,
                hospital_id, hospital_name, login_user_id, created_on, covenant, local_id, local_name,
                dose,
                medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id,
                doctor_atention_name,
                doctor_atention_specialty, doctor_atention_cpf, attention_number))
            conection.conn.commit()
            cur.close()
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return False
    else:
        try:
            cur = conection.conn.cursor()
            cur.execute("""
                   INSERT
                   INTO
                   public.appointment_complete
                   ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone, medicine,
                    hospital_id, hospital_name, login_user_id, created_on, cid_id, cid_name, covenant, local_id, local_name, dose,
                    medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id, doctor_atention_name,
                    doctor_atention_specialty, doctor_atention_cpf, attention_number)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                   """, (
            version, patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, patient_phone,
            medicines,
            hospital_id, hospital_name, login_user_id, created_on, cid_id, cid_name, covenant, local_id, local_name, dose,
            medicine_item_name, doctor_id, doctor_name, doctor_specialty, doctor_cpf, doctor_atention_id,
            doctor_atention_name,
            doctor_atention_specialty, doctor_atention_cpf, attention_number))
            conection.conn.commit()
            cur.close()
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            return False



    content = {
        'version': version,
        'patient_id': patient_id,
        'patient_name': patient_name,
        'patient_medical_record': patient_medical_record,
        'patient_covenat': patient_covenat,
        'patient_cpf': patient_cpf,
        'patient_phone': patient_phone,
        'medicines': medicines,
        'hospital_id': hospital_id,
        'hospital_name': hospital_name,
        'login_user_id': login_user_id,
        'created_on': created_on,
        'cid_id': cid_id,
        'cid_name': cid_name,
        'covenant': covenant,
        'local_id': local_id,
        'local_name': local_name,
        'dose': dose,
        'medicine_item_name': medicine_item_name,
        'doctor_id': doctor_id,
        'doctor_name': doctor_name,
        'doctor_specialty': doctor_specialty,
        'doctor_cpf': doctor_cpf,
        'doctor_atention_id': doctor_atention_id,
        'doctor_atention_name': doctor_atention_name,
        'doctor_atention_specialty': doctor_atention_specialty,
        'doctor_atention_cpf': doctor_atention_cpf,
        'attention_number': attention_number
    }

    insert_history(content)

    # otherPhotos
    cur = conection.conn.cursor()
    cur.execute(""" SELECT MAX(id) FROM public.appointment_complete """)
    data = cur.fetchone()
    id_patient_app = data[0]
    try:
        if len(info['otherPhotos']) > 0:
            for i in info['otherPhotos']:
                cur.execute("SELECT MAX(id) from public.photo")
                aux = cur.fetchone()
                id_photo = aux[0] + 1
                # insert photo
                cur.execute(""" INSERT INTO public.photo (id, "version", url, format) VALUES(%s, 0, %s, %s); """,
                            (id_photo, i, i.split('/')[1]))
                conection.conn.commit()
                # link Photo to Appointment
                cur.execute(""" INSERT INTO public.appointment_photo (appointment_other_photos_id, photo_id) VALUES(%s, %s); """,
                            (id_patient_app, id_photo))
                conection.conn.commit()
            cur.close()
    except:
        return

    return

def appointments_by_user_mobile(token, type):
    info = auth.validate_token(token,  output=True)
    # print(info, 'info')
    if info:
        if type['type'] == 'MY_PATIENTS':
            # payload = []
            # content = {}
            #
            # #PACIENTES
            # cur = conection.conn.cursor()
            # cur.execute("""SELECT
            #                 medical_type,
            #                 creation_date,
            #                 id,
            #                 local_id,
            #                 "name",
            #                 status,
            #                 doctor_id,
            #                 medical_record
            #                FROM public.patient WHERE doctor_id = """ + str(info['doctor_id']) + """ORDER BY creation_date desc""")
            # records = cur.fetchall()
            # cur.close()
            #
            # for data in records:
            #     info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
            #     if data[5] == 'INITIAL':
            #         attentionNumber = 'Paciente Nuevo'
            #     else:
            #         attentionNumber = data[7]
            #
            #     content = {
            #         'attentionNumber': attentionNumber,
            #         'createdOn': data[1],
            #         'doctor':  info_doctor_prescriptor['name'],
            #         'doctorStatus': {
            #             'enumType': "cobra.api.emuns.common.GenericStatus",
            #             'name': info_doctor_prescriptor['status']
            #         },
            #         'id': data[2],
            #         'local': data[3],
            #         'patient': data[4],
            #         'patientDoctor': '',
            #         'patientDoctorStatus': {
            #             'enumType': '',
            #             'name': ''
            #         }
            #     }
            #     payload.append(content)
            #     content = {}
            #
            # return payload            try:
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                                        attention_number, created_on, doctor_name, id, 
                                        hospital_name, patient_name,  doctor_id , doctor_atention_id
                                        FROM public.appointment_complete WHERE doctor_id = """ + str(
                info['doctor_id']) + """ ORDER BY created_on desc""")
            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
                info_doctor_platonista = doctors.get_doctors_by_id_v2(data[7])
                cr_date = data[1].strftime("%d/%m/%Y")
                created_on = cr_date
                content = {
                    'attentionNumber': data[0],
                    'createdOn': created_on,
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload
        if type['type'] == 'MY_ATTENTIONS':
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_atention_id = """ + str(info['doctor_id']) +
                            """ ORDER BY created_on desc""")
            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
                info_doctor_platonista = doctors.get_doctors_by_id_v2(data[7])
                # cr_date = datetime.datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f')
                cr_date = data[1].strftime("%d/%m/%Y")
                created_on = cr_date
                content = {
                    'attentionNumber': data[0],
                    'createdOn': created_on,
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload

def appointments_by_data_mobile(token, type):
    info = auth.validate_token(token,  output=True)
    if info:

        if type['type'] == 'MY_PATIENTS':
            # print(type)
            # try:
            #     from_date = datetime.datetime.strptime(type['from'], '%d/%m/%Y')
            # except:
            #     date = datetime.datetime.strptime('01/01/2020','%d/%m/%Y')
            #     from_date = date
            # try:
            #     to_date = datetime.datetime.strptime(type['to'], '%d/%m/%Y')
            # except:
            #     now = datetime.datetime.now()
            #     to_date = now.strftime("%d/%m/%Y")
            # cur = conection.conn.cursor()
            # cur.execute("""SELECT
            #                 medical_type,
            #                 creation_date,
            #                 id,
            #                 local_id,
            #                 "name",
            #                 status,
            #                 doctor_id,
            #                 medical_record
            #                 FROM public.patient WHERE doctor_id = %s
            #                 AND creation_date::DATE BETWEEN %s  AND %s""", (str(info['doctor_id']),  str(from_date),
            #                                                        str(to_date)))
            # records = cur.fetchall()
            # cur.close()
            # payload = []
            # content = {}
            # print(records)
            # for data in records:
            #     info_doctor_prescriptor = doctors.get_doctors_by_id_v2(data[6])
            #     if data[5] == 'INITIAL':
            #         attentionNumber = 'Paciente Nuevo'
            #     else:
            #         attentionNumber = data[7]
            #
            #     content = {
            #         'attentionNumber': attentionNumber,
            #         'createdOn': data[1],
            #         'doctor': info_doctor_prescriptor['name'],
            #         'doctorStatus': {
            #             'enumType': "cobra.api.emuns.common.GenericStatus",
            #             'name': info_doctor_prescriptor['status']
            #         },
            #         'id': data[2],
            #         'local': data[3],
            #         'patient': data[4],
            #         'patientDoctor': '',
            #         'patientDoctorStatus': {
            #             'enumType': '',
            #             'name': ''
            #         }
            #     }
            #     payload.append(content)
            #     content = {}
            # return payload

            try:
                from_date = datetime.datetime.strptime(type['from'], '%d/%m/%Y')
            except:
                date = datetime.datetime.strptime('01/01/2020', '%d/%m/%Y')
                from_date = date
            try:
                to_date = datetime.datetime.strptime(type['to'], '%d/%m/%Y')
            except:
                now = datetime.datetime.now()
                to_date = now.strftime("%d/%m/%Y")

            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_id = %s
                            AND created_on::DATE BETWEEN %s AND %s """, (str(info['doctor_id']), str(from_date), str(to_date)))


            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id(data[6])
                print(info_doctor_prescriptor)
                content = {
                    'attentionNumber': data[0],
                    'createdOn': data[1],
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload

        if type['type'] == 'MY_ATTENTIONS':

            try:
                from_date = datetime.datetime.strptime(type['from'], '%d/%m/%Y')
            except:
                date = datetime.datetime.strptime('01/01/2020', '%d/%m/%Y')
                from_date = date
            try:
                to_date = datetime.datetime.strptime(type['to'], '%d/%m/%Y')
            except:
                now = datetime.datetime.now()
                to_date = now.strftime("%d/%m/%Y")

            cur = conection.conn.cursor()

            cur.execute("""SELECT 
                            attention_number, created_on, doctor_name, id, 
                            hospital_name, patient_name,  doctor_id , doctor_atention_id
                            FROM public.appointment_complete WHERE doctor_atention_id = %s AND doctor_id != %s
                            AND created_on::DATE BETWEEN %s AND %s """, (str(info['doctor_id']),str(info['doctor_id']),
                                                                         str(from_date), str(to_date)))


            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for data in records:
                info_doctor_prescriptor = doctors.get_doctors_by_id(data[6])
                print(info_doctor_prescriptor)
                content = {
                    'attentionNumber': data[0],
                    'createdOn': datetime.datetime.strptime(data[1], '%d/%m/%Y'),
                    'doctor': info_doctor_prescriptor['name'],
                    'doctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    },
                    'id': data[3],
                    'local': data[4],
                    'patient': data[5],
                    'patientDoctor': info_doctor_prescriptor['name'],
                    'patientDoctorStatus': {
                        'enumType': "cobra.api.emuns.common.GenericStatus",
                        'name': info_doctor_prescriptor['status']
                    }
                }
                payload.append(content)
                content = {}
            return payload




