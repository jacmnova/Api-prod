import psycopg2
import conection
from flask import jsonify
from datetime import datetime



def get_specialty():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.specialty  WHERE status = 'ACTIVE' ORDER BY "id" ASC """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        content = {'id': result[0], 'name': result[1]}
        payload.append(content)
        content = {}
    return jsonify(payload)

def get_specialty_by_id(id_spe):
    try:
        if id_spe['name'] is None:
            content = {'id': '', 'name': ''}
            return content
    except:
        if id_spe is None:
            content = {'id': '', 'name': ''}
            return content
        else:

            cur = conection.conn.cursor()
            cur.execute("""SELECT "id", "name" FROM public.specialty WHERE "id" = """+ str(id_spe) )
            records = cur.fetchall()
            cur.close()
            payload = []
            content = {}
            for result in records:
                content = {'id': result[0], 'name': result[1]}
            return content

def get_specialty_by_id_v2(id_spe):
    if id_spe is None:
        content = {'id': '', 'name': ''}
        return content
    else:
        cur = conection.conn.cursor()
        cur.execute("""SELECT "id", "name" FROM public.specialty WHERE "id" = """+ str(id_spe) )
        records = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in records:
            content = {'id': result[0], 'name': result[1]}
        return content

def save_speciality(name):

    status = 'ACTIVE'
    cur = conection.conn.cursor()
    cur.execute("SELECT MAX(id) FROM public.specialty;")
    max = cur.fetchall()
    max = max[0][0]
    max = max + 1
    cur.execute("""INSERT INTO public.specialty
                (id, "version", "name", status)
                VALUES(%s, 0, %s, %s)""", (max, name, status))
    conection.conn.cursor()
    cur.close()
    return max


