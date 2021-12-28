import psycopg2
import conection
from flask import jsonify


def save_medicine_v2(name_medicine):
    version = 0
    name = name_medicine
    status = 'ACTIVE'
    cur = conection.conn.cursor()
    cur.execute("""SELECT 1 FROM public.medicine WHERE "name" = '""" + name + "'")
    records = cur.fetchall()
    if len(records) > 0 :
        cur.execute("""UPDATE public.medicine SET status = 'ACTIVE' where "name" = '""" + name + "'")
        conection.conn.commit()
        cur.close()
        return True
    else:
        cur.execute("SELECT MAX(id) FROM public.medicine;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1
        cur.execute("""INSERT INTO public.medicine
                    (id, "version", "name", status)
                    VALUES(%s, %s, %s, %s);""", (max, version, name, status))
        conection.conn.commit()
        cur.close()
        return False

def save_medicine(auth):
    version = 0
    name = auth['name'].upper()
    print(name)
    status = 'ACTIVE'
    cur = conection.conn.cursor()
    cur.execute("""SELECT 1 FROM public.medicine WHERE "name" = '""" + name + "'")
    records = cur.fetchall()

    if len(records) > 0 :
        cur.execute("""UPDATE public.medicine SET status = 'ACTIVE' where "name" = '""" + name + "'")
        conection.conn.commit()
        cur.close()
        return True
    else:
        cur.execute("SELECT MAX(id) FROM public.medicine;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1
        cur.execute("""INSERT INTO public.medicine
                    (id, "version", "name", status)
                    VALUES(%s, %s, %s, %s);""", (max, version, name, status))
        conection.conn.commit()
        cur.close()
        return False

def get_medicine():
    payload = []
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT "id", "name" FROM public.medicine  WHERE status = 'ACTIVE' ORDER BY "name" ASC """)
        records = cur.fetchall()
        cur.close()

        content = {}
        for result in records:
            content = {'id': result[0], 'name': result[1]}
            payload.append(content)
            content = {}
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
    return payload

def get_medicine_by_name(name):
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT id, name, status FROM public.medicine WHERE name = '""" + name + """'""")
        records = cur.fetchall()
        content = {}
        for i in records:
            content = {
                'id': i[0],
                'name': i[1],
                'status': i[2],
            }
        return content
    except:
        content = {}
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return content

def get_medicine_by_id(id):
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT id, name, status FROM public.medicine WHERE id = """ + str(id))
        records = cur.fetchall()
        content = {}
        for i in records:
            content = {
                'id': i[0],
                'name': i[1],
                'status': i[2],
            }
        return content
    except:
        content = {}
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return content

def put_medicine(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.medicine SET "name" = %s WHERE id = %s;""", (info['name'].upper(), info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def delete_medicine(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.medicine SET status = %s WHERE id = %s;""", ('DELETED', info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def medicines_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "name" FROM public.medicine WHERE status = 'ACTIVE' ORDER BY "name" asc """)
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

