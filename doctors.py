import psycopg2
import conection
from flask import jsonify
from datetime import datetime
import specialty

def save_doctors(data):
    print(data)
    cur = conection.conn.cursor()
    cur.execute("""SELECT 1 FROM public.doctor WHERE cpf = '""" + str(data['cpf']) + "'")
    records = cur.fetchall()
    if len(records) > 0 :
        if data['specialty']['id'] is None:
            cur = conection.conn.cursor()
            cur.execute("SELECT 1, id FROM public.specialty WHERE name =  '" + str(data['specialty']['name']) + "'")
            info_ver = cur.fetchone()
            print(info_ver)
            if info_ver is not None:
                aux = specialty.get_specialty_by_id(info_ver[1])
            else:
                print(info_ver)
                aux = specialty.save_speciality(data['specialty']['name'].upper())
                aux = specialty.get_specialty_by_id(aux)
            print(aux)
        else:
            aux = specialty.get_specialty_by_id(data['specialty']['id'])
            print(aux)

        cur.execute("""UPDATE public.doctor SET status = 'ACTIVE', specialty_id = %s, "name" = %s where cpf = %s """,
                    (aux['id'], data['name'].upper(), data['cpf']))
        conection.conn.commit()
        cur.close()

        return True
    else:
        # 'specialty': {'name': 'carme', 'id': None}}
        print(data)
        if data['specialty']['id'] is None:
            cur = conection.conn.cursor()
            cur.execute("SELECT 1, id FROM public.specialty WHERE name =  '" + str(data['specialty']['name']) + "'")
            info_ver = cur.fetchone()
            print(info_ver)
            if info_ver is not None:
                aux = specialty.get_specialty_by_id(info_ver[1])
            else:
                print(info_ver)
                aux = specialty.save_speciality(data['specialty']['name'].upper())
                aux = specialty.get_specialty_by_id(aux)
            print(aux)
        else:
            aux = specialty.get_specialty_by_id(data['specialty']['id'])
            print(aux)
        cur.execute("SELECT MAX(id) FROM public.doctor;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1

        cur.execute("""INSERT INTO public.doctor
                    (id, "version", crm, specialty_id, "name", status, cpf)
                    VALUES(%s, 0, null , %s, %s, %s, %s);""",
                    (max, aux['id'], data['name'].upper(), 'ACTIVE', data['cpf']))
        conection.conn.commit()
        cur.close()
    return False

def get_doctors():
    cur = conection.conn.cursor()
    cur.execute(""" SELECT "id", "name", specialty_id, cpf FROM public.doctor  WHERE status = 'ACTIVE' ORDER BY "id" ASC """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        if result[2] is None:
            specialty_name = ''
        else:
            specialty_name = specialty.get_specialty_by_id(result[2])['name']
        content = {
            'id': result[0],
            'name': result[1],
            'cpf': result[3],
            "specialty": {
                'name': specialty_name,
            }
        }
        payload.append(content)
        content = {}
    return payload

def get_doctors_by_id(id):
    if id is not None:
        try:
            cur = conection.conn.cursor()
            cur.execute("""SELECT id, "version", crm, specialty, "name", audit_id, status, cpf FROM public.doctor WHERE id = """ + str(id))
            records = cur.fetchall()
            cur.close()
            contentd = {}
            # id,
            # "version",
            # crm,
            # specialty,
            # "name",
            # audit_id,
            # status,
            # cpf
            for result in records:
                # contentd = {
                #     "id": result[0],
                #     "version": result[1],
                #     "crm": result[2],
                #     "specialty": result[3],
                #     "name": result[4],
                #     "audit_id": result[5],
                #     "status": result[6],
                #     "cpf": result[7],
                # }
                contentd = {
                    "id": result[0],
                    "cpf": result[7],
                    "specialty": {
                        'name': result[3],
                    },
                    "status": result[6],
                    "name": result[4],

                }
            return contentd
        except:
            curs = conection.conn.cursor()
            curs.execute("ROLLBACK")
            conection.conn.commit()
            curs.close()
            contentd = {
                "id": '',
                "cpf": '',
                "specialty": {
                    'name': '',
                },
                "status": '',
                "name": '',

            }
            return contentd

def get_doctors_by_id_v2(id):
    cur = conection.conn.cursor()
    cur.execute("""SELECT * FROM public.doctor WHERE id = """ + str(id))
    records = cur.fetchall()
    cur.close()
    contentd = {}
    # id,
    # "version",
    # crm,
    # specialty,
    # "name",
    # audit_id,
    # status,
    # cpf
    for result in records:
        contentd = {
            "id": result[0],
            "version": result[1],
            "crm": result[2],
            "specialty": result[3],
            "name": result[4],
            "audit_id": result[5],
            "status": result[6],
            "cpf": result[7],
        }
        # contentd = {
        #     "id": result[0],
        #     "cpf": result[7],
        #     "specialty": {
        #         'name': result[3],
        #     },
        #     "name": result[4],
        #
        # }
    return contentd

def get_doctors_by_name(name):
    cur = conection.conn.cursor()
    cur.execute("""SELECT * FROM public.doctor WHERE name = '""" + str(name) + """'""")
    records = cur.fetchall()
    cur.close()
    contentd = {}
    # id,
    # "version",
    # crm,
    # specialty,
    # "name",
    # audit_id,
    # status,
    # cpf
    print(len(records))
    for result in records:
        contentd = {
            "id": result[0],
            "version": result[1],
            "crm": result[2],
            "specialty": result[3],
            "name": result[4],
            "audit_id": result[5],
            "status": result[6],
            "cpf": result[7],
        }




    return contentd

def doctors_download():
    cur = conection.conn.cursor()
    cur.execute("""
                SELECT 
                    s."name", 
                    doc."name", 
                    doc.cpf 
                FROM public.doctor doc 
                LEFT JOIN 
                    public.specialty s 
                    on doc.specialty_id = s.id 
                WHERE  doc.status = 'ACTIVE'
                """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        content = {
            'specialty': i[0],
            'name': i[1],
            'cpf': i[2],
        }
        payload.append(content)
        content = {}
    return payload

def set_doctor(data):
    print(data)
    cur = conection.conn.cursor()
    cur.execute("SELECT 1, id FROM public.specialty WHERE name =  '" + str(data['specialty']['name']) + "'")
    info_ver = cur.fetchone()
    print(info_ver, "VERIFICACION DE SPECIALIDAD")
    if info_ver is None:
        print("No exite la especialidad")
        aux = specialty.save_speciality(data['specialty']['name'])
        aux = specialty.get_specialty_by_id(aux)
        print(aux, 'especialidad guadada')
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.doctor
                        SET "version"= "version"::int + 1, crm='', specialty_id=%s, name=%s, cpf=%s
                        WHERE id=%s;""", (aux['id'], data['name'], data['cpf'], data['id']))
        conection.conn.commit()
        cur.close()
    else:
        print("existe la especialidad")
        cur.execute("""UPDATE public.doctor
                                SET "version"= "version"::int + 1, crm='', specialty_id= %s, name= %s, cpf= %s
                                WHERE id= %s """, (info_ver[1], data['name'].upper(), data['cpf'], data['id']))
        conection.conn.commit()
        cur.close()

    return

def delete_doctor(data):
    print(data)
    cur = conection.conn.cursor()
    cur.execute("""UPDATE public.doctor set status = 'DELETED' WHERE id = """ + str(data['id']))
    conection.conn.commit()
    cur.close()

    return

def check_cpf_doctor(cpf):
    status = "ACTIVE"
    cur = conection.conn.cursor()
    cur.execute("""SELECT name FROM public.doctor WHERE cpf = %s AND status = %s""", (cpf, status))
    records = cur.fetchall()
    cur.close()
    if len(records) > 0:
        content = {}
        for i in records:
            content = {
                'name': i[0],
                'exists': True
            }
        return content
    else:
        return {
            'name': '',
            'exists': False
        }


