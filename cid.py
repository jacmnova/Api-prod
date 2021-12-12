import psycopg2
import conection
from flask import jsonify
from datetime import datetime
import function_jwt
import datetime
import pytz

def save_cid(auth, token):

    value = function_jwt.validate_token(token, True)
    name = auth['name'].upper()
    created_by = value['id']
    my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    created_on = my_date.strftime("%Y/%m/%d %H:%M:%S")
    status = 'ACTIVE'
    cur = conection.conn.cursor()

    cur.execute("""SELECT 1 FROM public.cid WHERE "name" = '""" + name + "'")
    records = cur.fetchall()
    print(name)
    print(records)
    if len(records) > 0 :
        cur.execute("""UPDATE public.cid
                                SET status='ACTIVE'
                                WHERE name='""" + name + "'")
        conection.conn.commit()
        cur.close()
        return True
    else:
        cur.execute("SELECT MAX(id) FROM public.cid;")
        max = cur.fetchall()
        max = max[0][0]
        max = max + 1
        cur.execute("""INSERT INTO public.cid
                (id, "version", updated_on, updated_by_id, "name", created_by_id, created_on, status, audit_id)
                VALUES(%s ,0, null , null , %s, %s, %s, %s, 1);""", (max, name, created_by, created_on, status))
        conection.conn.commit()
        cur.close()
        return False

def get_cid_by_id(id):
    cur = conection.conn.cursor()
    cur.execute("""SELECT id, name, status FROM public.cid WHERE id = """ + str(id))
    records = cur.fetchall()
    content = {}
    for i in records:
        content = {
            'id': i[0],
            'name': i[1],
            'status': i[2]
        }

    return content


def get_cid():
    cur = conection.conn.cursor()
    cur.execute("""SELECT "id", "name" FROM public.cid  WHERE status = 'ACTIVE' ORDER BY "name" ASC """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        content = {'id': result[0], 'name': result[1]}
        payload.append(content)
        content = {}
    return payload

def put_cid(info, token):
    try:
        value = function_jwt.validate_token(token, True)
        name = info['name'].upper()
        created_by = value['id']
        my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        created_on = my_date.strftime("%Y/%m/%d %H:%M:%S")
        status = 'ACTIVE'
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.cid SET "name" = %s, updated_on = %s, updated_by_id = %s WHERE id = %s;""",
                    (name, created_on, created_by, info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False


def delete_cid(info, token):

    try:
        value = function_jwt.validate_token(token, True)
        updated_by_id = value['id']
        my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        updated_on = my_date.strftime("%Y/%m/%d %H:%M:%S")
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.cid SET  updated_on = %s, updated_by_id = %s, status = %s WHERE id = %s;""",
                    (updated_on, updated_by_id, 'DELETED', info['id']))
        conection.conn.commit()
        cur.close()
        return True
    except:
        return False

def cid_download():
    cur = conection.conn.cursor()
    cur.execute("""SELECT 
                    cid."name",
                    cid.created_on,
                    lu."name" 
                FROM public.cid cid 
                LEFT JOIN 
                    public.login_user lu 
                    ON cid.created_by_id = lu.id 
                WHERE cid.status = 'ACTIVE';""")
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        content = {
            'cidName': i[0],
            'create': i[1].strftime("%Y/%m/%d %H:%M:%S"),
            'createName': i[2],
        }
        payload.append(content)
        content = {}
    return payload

