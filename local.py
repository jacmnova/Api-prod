import psycopg2
import conection
from flask import jsonify

def save_locals_by_name(name):
    cur = conection.conn.cursor()
    cur.execute("SELECT MAX(id) FROM public.local;")
    max = cur.fetchall()
    max = max[0][0]
    max = max + 1
    version = 0
    status = "ACTIVE"
    cur.execute("""INSERT INTO public.local
                        (id, "version", "name", status)
                        VALUES(%s, %s, %s, %s);""", (max, version, name, status))
    conection.conn.commit()
    cur.close()
    return


def save_locals(auth):
    version = 0
    name = auth['name'].upper()
    status = 'ACTIVE'
    cur = conection.conn.cursor()
    cur.execute("""SELECT 1 FROM public.local WHERE "name" = '""" + name + "'")
    records = cur.fetchall()
    print(name)
    print(records)
    if len(records) > 0 :
        cur.execute("""UPDATE public.local
                                SET status='ACTIVE'
                                WHERE name='""" + name + "'")
        conection.conn.commit()
        cur.close()
    else:
        cur.execute("SELECT MAX(id) FROM public.local;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1
        cur.execute("""INSERT INTO public.local
                    (id, "version", "name", status)
                    VALUES(%s, %s, %s, %s);""", (max, version, name, status))
        conection.conn.commit()
        cur.close()
        return False

def get_local_by_name(name):
    cur = conection.conn.cursor()
    cur.execute("SELECT id, name, status from public.local where name = '" + name + "'")
    records = cur.fetchall()
    content = {}
    for i in records:
        content = {
            'id': i[0],
            'name': i[1],
            'status': i[2]
        }
    return content

def get_locals():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.local  WHERE status = 'ACTIVE' ORDER BY "name" ASC """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        content = {'id': result[0], 'name': result[1]}
        payload.append(content)
        content = {}
    return payload

def get_locals_by_id(id_local):
    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.local  WHERE status = 'ACTIVE' AND id = """ + str(id_local))
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        content = {'id': result[0], 'name': result[1]}
        payload.append(content)
        content = {}
    return payload

def put_locals(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.local SET "name" = %s WHERE id = %s;""", (info['name'].upper(), info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def delete_locals(info):
    try:
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.local SET status = %s WHERE id = %s;""", ('DELETED', info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def local_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "name" FROM public.local WHERE status = 'ACTIVE' ORDER BY "name" ASC;""")
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
