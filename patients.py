import psycopg2
import pytz
import datetime

import conection
from datetime import datetime
import function_jwt
import local
import doctors
import medicine
import cid

def new_patient(info):
    if info['id'] != '':
        cur = conection.conn.cursor()
        cur.execute("""SELECT count(id) FROM public.patient WHERE id = """ + str(info['id']))
        records = cur.fetchall()
        cur.close()
        aux = 0
        for i in records:
            aux = i[0]

        if aux > 0:

            name = str(info['name'].upper())
            phone = str(info['phone'])
            medical_record = str(info['medicalRecord'].upper())
            covenant = str(info['covenant'].upper())
            cpf = str(info['cpf'])
            birth_date = str(info['birthDateStr'])
            doctor_id = str(info['doctor']['id'])
            id_ = str(info['id'])

            print("paciente existe")
            print(cpf)
            if cpf == 'None':
                print(cpf)
                cur = conection.conn.cursor()
                cur.execute("""
                                    UPDATE public.patient
                                    SET
                                        "name" = %s,
                                        phone = %s,
                                        medical_record = %s,
                                        covenant = %s,
                                        cpf = NULL ,
                                        birth_date = %s,
                                        doctor_id = %s

                                    WHERE
                                        id = %s;""",
                            (name, phone, medical_record, covenant, birth_date, doctor_id, id_))
                conection.conn.commit()
                cur.close()

                return True

            else:
                cur = conection.conn.cursor()
                cur.execute("""
                    UPDATE public.patient
                    SET
                        "name" = %s,
                        phone = %s,
                        medical_record = %s,
                        covenant = %s,
                        cpf = %s,
                        birth_date = %s,
                        doctor_id = %s
                    
                    WHERE
                        id = %s;""", (name, phone, medical_record, covenant, cpf, birth_date, doctor_id, id_))
                conection.conn.commit()
                cur.close()

                return True

    else:
        print("Nuevo paciente")
        cur = conection.conn.cursor()
        cur.execute("""SELECT id FROM public.local WHERE name = '""" + str(info['local']['name']) + "'")
        records = cur.fetchall()
        cur.close()
        id_local = records[0][0]
        name = info['name'].upper()
        phone = info['phone']
        medicalRecord = info['medicalRecord'].upper()
        covenant = info['covenant'].upper()
        # cid = info['cid']['id']
        doctor = info['doctor']['id']
        local = id_local
        cpf = info['cpf']
        if cpf == '':
            cpf = None
        birthDateStr = info['birthDateStr']
        medical_type = 'REUMATOLOGIA'
        status = 'INITIAL'
        my_date = datetime.now(pytz.timezone('America/Sao_Paulo'))
        creation_date = my_date.strftime("%Y/%m/%d %H:%M:%S")

        data_user = function_jwt.get_token_data()
        login_user_id = data_user['id']

            # otherPhotos
        cur = conection.conn.cursor()
        cur.execute("SELECT max(id) FROM public.patient")
        max = cur.fetchone()[0] + 1

        cur.execute("""INSERT INTO public.patient
                        (id, "version", phone, hospital_id, login_user_id, cid_id, covenant, local_id, "name",
                        audit_id, creation_date, status, medical_record, cpf, birth_date, medical_type, doctor_id)
                        VALUES(%s ,0, %s, %s, %s, NULL, %s, %s, %s, NULL, %s, %s,%s, %s, %s, %s, %s);""",
                        (max, phone, id_local, login_user_id, covenant, local, name, creation_date, status, medicalRecord,
                         cpf, birthDateStr, medical_type, doctor))
        conection.conn.commit()
        cur.close()

        return


    def update_patient(info):
        print(info['birthDateStr'])
        print(info['covenant'])
        print(info['cpf'])
        print(info['doctor']['id'])
        print(info['id'])
        print(info['medicalRecord'])
        print(info['name'])
        print(info['phone'])

        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.patient
                        SET phone=%s,
                            covenant=%s, 
                            name=%s, 
                            medical_record=%s, 
                            cpf=%s, 
                            birth_date=%s,  
                            doctor_id=%s
                        WHERE id = %s""", (info['phone'], info['covenant'],info['name'],info['medicalRecord'],info['cpf'],
                                           info['birthDateStr'],info['doctor']['id'],info['id']))
        conection.conn.commit()
        cur.close()

    return


def get_patients():
    cur = conection.conn.cursor()
    cur = conection.conn.cursor()
    cur.execute(""" SELECT q1.id, q1."name", q1.medical_record, q1.cpf, q1.covenant, q1.doctor_id, doctor."name" AS doctor_name
                    FROM public.doctor as doctor, (SELECT id, "name", medical_record, cpf, covenant, doctor_id FROM public.patient) AS q1 
                    WHERE doctor.id = q1.doctor_id""")
    records = cur.fetchall()
    print(records)
    cur.close()
    payload = []
    content = {}
    print(records)
    for result in records:
        if result[3]:
            cpf = result[3]
        else:
            cpf = ''
        content = {
            'covenant': result[4],
            'doctor': {
                'id': result[5],
                'name': result[6],
            },
            'id': result[0],
            'medicalRecord': result[2],
            'name': result[1],
            'nameCpf': "CPF: " + cpf + " - " + result[1]}
        payload.append(content)
        # covenant: "AMIL"
        # doctor: {id: 19, name: 'Gabriela Munhoz'}
        # id: 2047
        # medicalRecord: "8792684"
        # name: "ABRAO HA"
        # nameCpf: "CPF: 135.550.748-06 - ABRAO HA"
        # content = {'id': result[0], 'name': result[1]}
        # payload.append(content)
        content = {}
    return payload

def get_info_patients(id):
    cur = conection.conn.cursor()
    cur.execute("""SELECT 
    id,
    "version",
    phone,
    hospital_id,
    login_user_id,
    cid_id,
    covenant,
    local_id,
    "name",
    audit_id,
    creation_date,
    status,
    medical_record,
    cpf,
    birth_date,
    medical_type,
    doctor_id
     FROM public.patient WHERE id = """ + str(id))
    records = cur.fetchall()

    cur.close()
    print(records)
    # id,
    # "version"
    # phone
    # hospital_id
    # login_user_id
    # cid_id
    # covenant
    # local_id
    # "name"
    # audit_id
    # creation_date
    # status
    # medical_record
    # cpf
    # birth_date
    # medical_type
    # doctor_id
    payload = []
    content = {}
    for result in records:
        content = {
            'id': result[0],
            'version': result[1],
            'phone': result[2],
            'hospital_id': result[3],
            'login_user_id': result[4],
            'cid_id': result[5],
            'covenant': result[6],
            'local_id': result[7],
            'name': result[8],
            'audit_id': result[9],
            'creation_date': result[10],
            'status': result[11],
            'attentionNumber': result[12],
            'cpf': result[13],
            'birth_date': result[14],
            'medical_type': result[15],
            'doctor_id': result[16],
            }
        print(content)
        payload.append(content)
    return content

def get_v2():
    cur = conection.conn.cursor()
    cur.execute("""SELECT id, name, cpf, birth_date, covenant, phone, creation_date 
                    FROM public.patient WHERE status != 'DELETED' order by name asc""")
    records = cur.fetchall()
    payload = []
    content = {}
    for i in records:
        if (i[3]):
            birthDate = i[3].strftime("%d/%m/%Y")
        else:
            birthDate = ''

        if (i[6]):
            creationDate = i[6].strftime("%d/%m/%Y")
        else:
            creationDate = ''

        content = {
            'id': i[0],
            'name': i[1],
            'cpf': i[2],
            'birthDate': birthDate,
            'covenant': i[4],
            'phone': i[5],
            'creationDate': creationDate
        }
        payload.append(content)
        content = {}

    return payload

def get_info_patient(id):
    print(id)
    content = {}
    try:
        cur = conection.conn.cursor()
        cur.execute("""
        SELECT 
        p.id, 
        p.name, 
        p.phone,
        p.medical_record, 
        p.covenant, 
        p.cpf, 
        p.birth_date, 
        p.creation_date, 
        p.doctor_id, 
        d."name", 
        d.status,
        p.local_id, p.iskid FROM public.patient p  join doctor d ON doctor_id = d.id WHERE p.id = """ + str(id))
        records = cur.fetchall()


        cur.execute("""SELECT medicine_item_name, dose, cid_id FROM public.appointment_history WHERE patient_id = """ + str(id))
        data = cur.fetchone()
        cur.close()

        medicine_item_name = ''
        dose = ''
        cid_id = ''
        if data is None:
            medicine_item_name = ''
            dose = ''
            cid_id = ''
        else:
            medicine_item_name = data[0]
            dose = data[1]
            cid_id = data[2]

        cur.close()
        content = {}
        # 16 / 11 / 2021
        menor = False
        if len(records) == 0:
            cur = conection.conn.cursor()
            cur.execute("""SELECT 
                            p.id, 
                            p.name, 
                            p.phone,
                            p.medical_record, 
                            p.covenant, 
                            p.cpf, 
                            p.birth_date, 
                            p.creation_date, 
                            p.doctor_id, 
                            p.local_id, p.iskid FROM public.patient p WHERE p.id =  """ + str(id))
            records = cur.fetchall()
            cur.close()
            local_name = ''
            for i in records:
                if i[9] is not None:
                    aux_local = local.get_locals_by_id(i[11])
                    print(aux_local)
                    if len(aux_local) > 0:
                        local_name = aux_local[0]['name']

                if i[5] is None:
                    menor = True

                if i[6]:
                    birthDate = i[6].strftime("%d/%m/%Y")
                else:
                    birthDate = ''

                if i[7]:
                    creationDate = i[7].strftime("%d/%m/%Y")
                else:
                    creationDate = ''

                doctor_id = ''
                doctor_status = ''
                doctor_doctorName = ''

                if i[8] is not None:
                    doctor = doctors.get_doctors_by_id(i[8])
                    doctor_id = doctor['id']
                    doctor_status = doctor['status']
                    doctor_doctorName = doctor['name']
                    # "id": result[0],
                    # "cpf": result[7],
                    # "specialty": {
                    #     'name': result[3],
                    # },
                    # "status": result[6],
                    # "name": result[4],

                content = {
                    'id': i[0],
                    'name': i[1],
                    'phone': i[2],
                    'attentionNumber': i[3],
                    'covenant': i[4],
                    'cpf': i[5],
                    'birthDateStr': birthDate,
                    'createdOn': creationDate,
                    'doctor': {
                        'id': doctor_id,
                        'status': doctor_status,
                        'doctorName': doctor_doctorName
                    },
                    'menor': menor,
                    'cid': {
                        'id': cid_id
                    },
                    'lastInfo': {
                        'dose': dose,
                        'medicineItem': {
                            'name': medicine_item_name
                        }
                    },
                    'local': {
                        'name': local_name
                    },
                    'isKid': i[10]

                }
        else:
            local_name = ''
            for i in records:
                if i[11] is not None:
                    aux_local = local.get_locals_by_id(i[11])
                    print(aux_local)
                    if len(aux_local) > 0:
                        local_name = aux_local[0]['name']

                if i[5] is None:
                    menor = True

                if (i[6]):
                    birthDate = i[6].strftime("%d/%m/%Y")
                else:
                    birthDate = ''

                if (i[7]):
                    creationDate = i[7].strftime("%d/%m/%Y")
                else:
                    creationDate = ''

                content = {
                    'id': i[0],
                    'name': i[1],
                    'phone': i[2],
                    'attentionNumber': i[3],
                    'covenant': i[4],
                    'cpf': i[5],
                    'birthDateStr': birthDate,
                    'createdOn': creationDate,
                    'doctor': {
                        'id': i[8],
                        'status': i[10],
                        'doctorName': i[9]
                    },
                    'menor': menor,
                    'cid': {
                        'id': cid_id
                    },
                    'lastInfo': {
                        'dose': dose,
                        'medicineItem': {
                            'name': medicine_item_name
                        }
                    },
                    'local': {
                        'name': local_name
                    },
                    'isKid': i[12]

                }
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return False

    return content

def delete(id):
    cur = conection.conn.cursor()
    # cur.execute("""DELETE FROM public.patient WHERE id= """ + str(id))
    cur.execute("""UPDATE public.patient SET status='DELETED' WHERE id = """ + str(id))
    conection.conn.commit()
    cur.close()
    return True
    # try:
    #     cur = conection.conn.cursor()
    #     cur.execute("""DELETE FROM public.patient WHERE id= """ + str(id))
    #     conection.conn.commit()
    #     cur.close()
    #     return True
    # except:
    #     curs = conection.conn.cursor()
    #     curs.execute("ROLLBACK")
    #     conection.conn.commit()
    #     curs.close()
    #     return False

def patients_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "name", cpf, birth_date, medical_type, phone, creation_date, isKid FROM public.patient;""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        if i[2] is not None:
            birth_date = i[2].strftime("%d/%m/%Y")
        else:
            birth_date = ''

        if i[5] is not None:
            creation_date = i[5].strftime("%d/%m/%Y")
        else:
            creation_date = ''

        if i[0] is not None:
            name = i[0]
        else:
            name = ''
        print(i[6])
        content = {
            'name': name,
            'cpf': i[1],
            'birth_date': birth_date,
            'medical_type': i[3],
            'phone': i[4],
            'creation_date': creation_date,
            'isKid': i[6]
        }
        payload.append(content)
        content = {}
    return payload


#MOBILE
def get_info_patient_mobile(id):
    cur = conection.conn.cursor()
    cur.execute("""
    SELECT 
    p.id, 
    p.name, 
    p.phone,
    p.medical_record, 
    p.covenant, 
    p.cpf, 
    p.birth_date, 
    p.creation_date, 
    p.doctor_id, 
    d."name", 
    d.status,
    p.local_id, 
    p.isKid FROM public.patient p  join doctor d ON doctor_id = d.id WHERE p.id = """ + str(id))
    records = cur.fetchall()
    print(records)

    cur.execute("""SELECT medicine_item_name, dose, cid_id FROM public.appointment_history WHERE patient_id = """ + str(id))
    data = cur.fetchone()
    cur.close()

    medicine_item_name = ''
    dose = ''
    cid_id = ''
    if data is None:
        medicine_item_name = ''
        dose = ''
        cid_id = ''
    else:
        if data[0] is not None:
            medicine_info = medicine.get_medicine_by_name(data[0])
            print("Verificando medicina")
            if medicine_info['status'] == 'DELETED':
                medicine_item_name = ''
            else:
                medicine_item_name = data[0]
        else:
            medicine_item_name = data[0]


        if data[2] is not None:
            cid_info = cid.get_cid_by_id(data[2])

            print("Verificando CID")
            if cid_info['status'] == 'DELETED':
                cid_id = ''
            else:
                cid_id = data[2]
        else:
            cid_id = data[2]
        dose = data[1]

    cur.close()
    content = {}
    # 16 / 11 / 2021
    menor = False
    if len(records) == 0:
        print("FAKA")
        cur = conection.conn.cursor()
        cur.execute("""SELECT 
                                p.id, 
                                p.name, 
                                p.phone,
                                p.medical_record, 
                                p.covenant, 
                                p.cpf, 
                                p.birth_date, 
                                p.creation_date, 
                                p.doctor_id, 
                                p.local_id, p.iskid FROM public.patient p WHERE p.id =  """ + str(id))
        records = cur.fetchall()

        cur.execute("""select p.url from public.patient_photo pp 
        join public.photo p on pp.photo_id = p.id where pp.patient_other_photos_id = """ + str(records[0][0]))
        photos = cur.fetchall()
        list_photos = []
        if len(photos) > 0:
            for i in photos:
                list_photos.append({'url': i[0]})

        cur.close()
        local_name = ''



        for i in records:
            if i[9] is not None:
                aux_local = local.get_locals_by_id(i[11])
                print(aux_local)
                if len(aux_local) > 0:
                    local_name = aux_local[0]['name']


            if i[6]:
                birthDate = i[6].strftime("%d/%m/%Y")
            else:
                birthDate = ''

            if i[7]:
                creationDate = i[7].strftime("%d/%m/%Y")
            else:
                creationDate = ''

            doctor_id = ''
            doctor_status = ''
            doctor_doctorName = ''

            if i[8] is not None:
                doctor = doctors.get_doctors_by_id(i[8])
                doctor_id = doctor['id']
                doctor_status = doctor['status']
                doctor_doctorName = doctor['name']

            content = {
                'id': i[0],
                'name': i[1],
                'phone': i[2],
                'attentionNumber': i[3],
                'covenant': i[4],
                'cpf': i[5],
                'birthDateStr': birthDate,
                'createdOn': creationDate,
                'doctor': {
                    'id': doctor_id,
                    'status': doctor_status,
                    'doctorName': doctor_doctorName
                },
                'menor': i[10],
                'cid': {
                    'id': cid_id
                },
                'lastInfo': {
                    'dose': dose,
                    'medicineItem': {
                        'name': medicine_item_name
                    }
                },
                'local': {
                    'name': local_name
                },
                'isKid': i[10],
                'otherPhotos': list_photos

            }
        verificar_content(content)
        return content
    else:
        cur = conection.conn.cursor()
        cur.execute("""select p.url from public.patient_photo pp 
             join public.photo p on pp.photo_id = p.id where pp.patient_other_photos_id = """ + str(records[0][0]))
        photos = cur.fetchall()
        list_photos = []
        if len(photos) > 0:
            for i in photos:
                list_photos.append({'url': i[0]})

        cur.close()
        local_name = ''

        for i in records:
            if i[11] is not None:
                aux_local = local.get_locals_by_id(i[11])
                print(aux_local)
                if len(aux_local) > 0:
                    local_name = aux_local[0]['name']

            if (i[6]):
                birthDate = i[6].strftime("%d/%m/%Y")
            else:
                birthDate = ''

            if (i[7]):
                creationDate = i[7].strftime("%d/%m/%Y")
            else:
                creationDate = ''

            content = {
                'id': i[0],
                'name': i[1],
                'phone': i[2],
                'attentionNumber': i[3],
                'covenant': i[4],
                'cpf': i[5],
                'birthDateStr': birthDate,
                'createdOn': creationDate,
                'doctor': {
                    'id': i[8],
                    'status': i[10],
                    'doctorName': i[9]
                },
                'menor': i[12],
                'cid': {
                    'id': cid_id
                },
                'lastInfo': {
                    'dose': dose,
                    'medicineItem': {
                        'name': medicine_item_name
                    }
                },
                'local': {
                    'name': local_name
                },
                'isKid': i[12],
                'otherPhotos': list_photos

            }

    return verificar_content(content)


def verificar_content(info):
    print("VERFICANDO CONTENT")
    print(info)
    if info == {}:
        return
    else:
        #Verificacion de Doctor
        try:
            if info['doctor']['id'] != '':
                if info['doctor']['status'] == "DELETED":
                    info['doctor']['id'] = ''
                    info['doctor']['status'] = ''
                    info['doctor']['doctorName'] = ''
        except:
            print(None)
        try:
            #Verificacion de medicina
            if info['lastInfo']['medicineItem']['name'] != '' and info['medicineItem']['name'] is not None:
                info_medicine = medicine.get_medicine_by_name(info['lastInfo']['medicineItem']['name'])
                print(info_medicine)
                if info_medicine != {}:
                    if info_medicine['status'] == "DELETED":
                        info['lastInfo']['medicineItem']['name'] = ''
        except:
            print(None)

        try:
            #Verificando Local
            if info['local']['name'] != '' and info['local']['name'] is not None:
                info_local = local.get_local_by_name(info['local']['name'])
                print(info_local)
                if info_local != {}:
                    if info_local['status'] == "DELETED":
                        info['local']['name'] = ''
        except:
            print(None)
        try:
            #Verificando CID
            if info['cid']['id'] != '' and info['cid']['id'] is not None:
                info_cid = cid.get_cid_by_id(info['cid']['id'])
                if info_cid != {}:
                    if info_cid['status'] == "DELETED":
                        info['cid']['id'] = ''
        except:
            print(None)

        return info

def new_patient_mobile(info):
    if info['id'] != '':
        try:
            cur = conection.conn.cursor()
            cur.execute("""SELECT count(id) FROM public.patient WHERE id = """ + str(info['id']))
            records = cur.fetchall()
            cur.close()
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
        aux = 0
        for i in records:
            aux = i[0]

        print("ENTRE")
        if aux > 0:
            print("paciente existe")
            name = str(info['name'].upper())
            phone = str(info['phone'])
            medical_record = str(info['medicalRecord'].upper())
            covenant = str(info['covenant'].upper())
            cpf = str(info['cpf'])
            birth_date = datetime.strptime(info['birthDateStr'], '%d/%m/%Y')
            doctor_id = str(info['doctor']['id'])
            id_ = str(info['id'])
            print(name)
            print(phone)
            print(medical_record)
            print(covenant)
            print(birth_date)
            print(doctor_id)
            print(info['menor'])
            print(id_)
            if info['cpf'] is None or info['cpf'] == '':
                print('ENTRE')
                cur = conection.conn.cursor()
                cur.execute("""UPDATE public.patient
                                                SET
                                                    "name" = %s,
                                                    phone = %s,
                                                    medical_record = %s,
                                                    covenant = %s,
                                                    cpf = null,
                                                    birth_date = %s,
                                                    doctor_id = %s,
                                                    isKid = %s
                                                WHERE
                                                    id = %s;""",
                            (name, phone, medical_record, covenant, birth_date, doctor_id, info['menor'], id_))
                conection.conn.commit()
                cur.close()
                return True
            else:
                print('ENTRE 2')

                cur = conection.conn.cursor()
                cur.execute("""UPDATE public.patient
                                SET
                                    "name" = %s,
                                    phone = %s,
                                    medical_record = %s,
                                    covenant = %s,
                                    cpf = %s,
                                    birth_date = %s,
                                    doctor_id = %s,
                                    isKid = %s
                                WHERE
                                    id = %s;""",
                            (name, phone, medical_record, covenant, cpf, birth_date, doctor_id, info['menor'], id_))
                conection.conn.commit()
                cur.close()
                return True


            # try:
            #     cur = conection.conn.cursor()
            #     cur.execute("""UPDATE public.patient
            #                     SET
            #                         "name" = %s,
            #                         phone = %s,
            #                         medical_record = %s,
            #                         covenant = %s,
            #                         cpf = %s,
            #                         birth_date = %s,
            #                         doctor_id = %s,
            #                         isKid = %s
            #                     WHERE
            #                         id = %s;""",
            #                 (name, phone, medical_record, covenant, cpf, birth_date, doctor_id, info['menor'], id_))
            #     conection.conn.commit()
            #     cur.close()
            #     return True
            # except:
            #     curs = conection.conn.cursor()
            #     curs.execute("ROLLBACK")
            #     conection.conn.commit()
            #     curs.close()
            #     return False
            # if info['menor'] == True:
            #     # print("entry")
            #     # cur = conection.conn.cursor()
            #     # cur.execute("""UPDATE public.patient
            #     #                                     SET
            #     #                                     "name" = %s,
            #     #                                     phone = %s,
            #     #                                     medical_record = %s,
            #     #                                     covenant = %s,
            #     #                                     cpf = NULL,
            #     #                                     birth_date = %s,
            #     #                                     doctor_id = %s,
            #     #                                     isKid = %s
            #     #                                     WHERE
            #     #                                     id = %s;""",
            #     #             (name, phone, medical_record, covenant, birth_date, doctor_id, info['menor'], id_))
            #     # conection.conn.commit()
            #     # cur.close()
            #     # return True
            #     print(cpf, 'UPDATE')
            #     cur = conection.conn.cursor()
            #     cur.execute("""UPDATE public.patient
            #                                                                            SET
            #                                                                            "name" = %s,
            #                                                                            phone = %s,
            #                                                                            medical_record = %s,
            #                                                                            covenant = %s,
            #                                                                            cpf = cpf,
            #                                                                            birth_date = %s,
            #                                                                            doctor_id = %s,
            #                                                                            isKid = %s
            #                                                                            WHERE
            #                                                                            id = %s;""",
            #                 (name, phone, medical_record, covenant, birth_date, doctor_id, info['menor'], id_))
            #     conection.conn.commit()
            #     cur.close()
            #     # try:
            #     #     cur = conection.conn.cursor()
            #     #     cur.execute("""UPDATE public.patient
            #     #                                                         SET
            #     #                                                         "name" = %s,
            #     #                                                         phone = %s,
            #     #                                                         medical_record = %s,
            #     #                                                         covenant = %s,
            #     #                                                         cpf = cpf,
            #     #                                                         birth_date = %s,
            #     #                                                         doctor_id = %s,
            #     #                                                         isKid = %s
            #     #                                                         WHERE
            #     #                                                         id = %s;""",
            #     #                 (name, phone, medical_record, covenant, birth_date, doctor_id, info['menor'], id_))
            #     #     conection.conn.commit()
            #     #     cur.close()
            #     #     return True
            #     # except:
            #     #     curs = conection.conn.cursor()
            #     #     curs.execute("ROLLBACK")
            #     #     conection.conn.commit()
            #     #     curs.close()
            #     #     return False

            #
            # else:

    else:
        print("Nuevo paciente")
        cur = conection.conn.cursor()
        cur.execute("""SELECT id FROM public.local WHERE name = '""" + str(info['local']['name']) + "'")
        records = cur.fetchall()
        cur.close()
        if len(records) > 0:
            id_local = records[0][0]
        else:
            local.save_locals_by_name(str(info['local']['name']))
            cur = conection.conn.cursor()
            cur.execute("""SELECT id FROM public.local WHERE name = '""" + str(info['local']['name']) + "'")
            records = cur.fetchall()
            cur.close()
            id_local = records[0][0]

        name = info['name'].upper()
        phone = info['phone']
        medicalRecord = info['medicalRecord'].upper()
        covenant = info['covenant'].upper()
        # cid = info['cid']['id']
        doctor_id = info['doctor']['id']
        # local = id_local
        cpf = info['cpf']
        if cpf == '':
            cpf = None
        birthDateStr = datetime.strptime(info['birthDateStr'], '%d/%m/%Y')
        medical_type = 'REUMATOLOGIA'
        status = 'INITIAL'
        my_date = datetime.now(pytz.timezone('America/Sao_Paulo'))
        creation_date = my_date.strftime("%Y/%m/%d %H:%M:%S")

        data_user = function_jwt.get_token_data()
        login_user_id = data_user['id']


        cur = conection.conn.cursor()
        cur.execute("SELECT max(id) FROM public.patient")
        max = cur.fetchone()[0] + 1
        if info['cpf'] is None or info['cpf'] == '':
            cur.execute("""INSERT INTO public.patient
                            (id, "version", phone, hospital_id, login_user_id, cid_id, covenant, local_id, "name", audit_id,
                             creation_date, status, medical_record, cpf, birth_date, medical_type, doctor_id, iskid)
                            VALUES(%s, 0, %s, NULL, %s, NULL, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s);""",
                        (max, phone, login_user_id, covenant, id_local, name, creation_date, status, medicalRecord,
                         cpf, birthDateStr, medical_type, doctor_id, info['menor']))

            conection.conn.commit()
            cur.close()
        else:
            cur.execute("""INSERT INTO public.patient
                                        (id, "version", phone, hospital_id, login_user_id, cid_id, covenant, local_id, "name", audit_id,
                                         creation_date, status, medical_record, cpf, birth_date, medical_type, doctor_id, iskid)
                                        VALUES(%s, 0, %s, NULL, %s, NULL, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s);""",
                        (max, phone, login_user_id, covenant, id_local, name, creation_date, status, medicalRecord,
                         cpf, birthDateStr, medical_type, doctor_id, info['menor']))

            conection.conn.commit()
            cur.close()

        # otherPhotos
        cur = conection.conn.cursor()
        cur.execute(""" SELECT MAX(id) FROM public.patient """)
        data = cur.fetchone()
        id_patient_new = data[0]

        if len(info['otherPhotos']) > 0:
            for i in info['otherPhotos']:
                cur.execute("SELECT MAX(id) from public.photo")
                aux = cur.fetchone()
                id_photo = aux[0] + 1
                #insert photo
                cur.execute(""" INSERT INTO public.photo (id, "version", url, format) VALUES(%s, 0, %s, %s); """,
                            (id_photo, i, i.split('/')[1]))
                conection.conn.commit()
                #link Photo to patient
                cur.execute(""" INSERT INTO public.patient_photo (patient_other_photos_id, photo_id) VALUES(%s, %s); """,
                            (id_patient_new, id_photo))
                conection.conn.commit()

        #ADD patient to history

        version = 0
        id_patient_new
        name
        medicalRecord
        covenant
        cpf
        doctor_id
        info_doctor = doctors.get_doctors_by_id(doctor_id)
        doctor_name = info_doctor['name']
        doctor_specialty = info_doctor['specialty']['name']
        doctor_cpf = info_doctor['cpf']
        info_local = local.get_locals_by_id(id_local)
        print(info_local)
        local_name = info_local[0]['name']
        nro_atendimiento = 0
        cur.execute(""" INSERT INTO public.appointment_history
                               ("version", patient_id, patient_name, patient_medical_record, patient_covenat, patient_cpf, 
                               doctor_id, doctor_name, doctor_specialty, doctor_cpf, local_id, local_name, nro_atendimiento)
                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (version, id_patient_new, name,
                                                                                    medicalRecord, covenant, cpf, doctor_id,
                                                                                    doctor_name, doctor_specialty, doctor_cpf,
                                                                                    id_local, local_name, nro_atendimiento))
        conection.conn.commit()
        cur.close()


        # print(info, 'LOCAL')
        # # local_info = local.get_locals_by_id(str(id_local))
        # cur = conection.conn.cursor()
        # cur.execute("""SELECT "id", "name" FROM public.local  WHERE status = 'ACTIVE' AND id = """ + str(id_local))
        # records = cur.fetchall()
        # cur.close()
        # local_info = {}
        # for result in records:
        #     local_info = {'id': result[0], 'name': result[1]}
        #
        # doctor_info = doctors.get_doctors_by_id(doctor_id)
        # version = 0
        # patient_id = max
        # patient_name = name
        # patient_medical_record = medicalRecord
        # patient_covenat = covenant
        # patient_cpf = cpf
        # patient_phone = phone
        # medicines =  '-'
        # hospital_id =  None
        # hospital_name =  '-'
        # login_user_id = login_user_id
        # created_on = creation_date
        # cid_id = None
        # cid_name = '-'
        # covenant = covenant
        # local_id = id_local,
        # local_name = local_info['name']
        # dose =  ''
        # medicine_item_id =  None
        # medicine_item_name =  '-'
        # doctor_id = doctor_id
        # doctor_name = doctor_info['name']
        # doctor_specialty = doctor_info['specialty']['name']
        # doctor_cpf = doctor_info['cpf']
        # doctor_atention_id =  None
        # doctor_atention_name =  '-'
        # doctor_atention_specialty =  '-'
        # doctor_atention_cpf =  '-'
        # attention_number =  '-'
        #
        #
        # cur = conection.conn.cursor()
        # cur.execute(""" INSERT INTO public.appointment_history
        #             (version,
        #             patient_id,
        #             patient_name,
        #             patient_medical_record,
        #             patient_covenat,
        #             patient_cpf,
        #             created_on,
        #             covenant,
        #             local_id,
        #             local_name,
        #             doctor_id,
        #             doctor_name,
        #             doctor_specialty,
        #             doctor_cpf,
        #             nro_atendimiento) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0)""", (version,patient_id,patient_name,
        #                                                                                           patient_medical_record,patient_covenat,
        #                                                                                           patient_cpf,created_on,covenant,local_id,
        #                                                                                           local_name,doctor_id,doctor_name,
        #                                                                                           doctor_specialty,doctor_cpf))
        # conection.conn.commit()
        # cur.close()


def update_patient(info):
    cur = conection.conn.cursor()
    cur.execute("""UPDATE public.patient
                    SET phone=%s,
                    covenant=%s, 
                    name=%s, 
                    medical_record=%s, 
                    cpf=%s, 
                    birth_date=%s,  
                    doctor_id=%s
                    WHERE id = %s""",(info['phone'], info['covenant'], info['name'], info['medicalRecord'], info['cpf'],
                     info['birthDateStr'], info['doctor']['id'], info['id']))
    conection.conn.commit()
    cur.close()
    return

def check_cpf(cpf):
    cur = conection.conn.cursor()
    cur.execute("SELECT count(id) FROM public.patient WHERE cpf = '" + str(cpf['data']) + "'")
    record = cur.fetchone()
    if record[0] > 0:
        return False
    else:
        return True



