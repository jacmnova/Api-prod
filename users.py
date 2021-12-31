import bcrypt
import string
import random
import conection
from datetime import datetime
import doctors
import emails
from function_jwt import write_token, validate_token
import psycopg2

## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def validate_sesion(token):
    info_user = validate_token(token, True)
    cur = conection.conn.cursor()
    cur.execute("SELECT account_locked from public.login_user WHERE id = " + str(info_user['id']))
    record = cur.fetchone()
    print(record)
    print(info_user)
    return record[0]

def save_user(data):
    print(data)
    exist = get_data_user(data['username'])
    aux = len(exist)
    if aux > 0:
        print("USER YA EXISTE")
        if data['roleType'] == 'ADMIN':

            updated_on = datetime.now()
            account_locked = data['accountLocked']
            name = data['name']
            if data['accountLocked'] == False:
                status = 'ACTIVE'
                enabled = True
            else:
                status = 'DEACTIVATED'
                enabled = True
            app_type = ''
            role_user = data['roleType']

            cur = conection.conn.cursor()
            cur.execute("""UPDATE public.login_user SET
                            "version" = "version" + 1, 
                            updated_on = %s, 
                            account_locked = %s,
                            "name" = %s, 
                            status = %s, 
                            doctor_id = null, 
                            enabled = %s, 
                            app_type = %s, 
                            role_user = %s 
                          WHERE id = %s""", (updated_on, account_locked, name.upper(), status, enabled, app_type, role_user,
                                             exist['id']))
            # conection.conn.commit()
            cur.close()

        if data['roleType'] == 'DOCTOR_USER':
            exist_doctor = doctors.get_doctors_by_name(data['doctor']['name'])
            if len(exist_doctor) > 0:
                doctor_id = exist_doctor['id']
            else:
                cur = conection.conn.cursor()
                cur.execute("SELECT MAX(id) FROM public.doctor;")
                max = cur.fetchall()
                max = max[0][0]
                max = max + 1
                cur.execute("""INSERT INTO public.doctor
                                    (id, "version", crm, specialty_id, "name", status, cpf)
                                    VALUES(%s, 0, null , null , %s, 'ACTIVE', null );""",
                            (max, data['doctor']['name']))
                conection.conn.commit()
                cur.close()
                exist_doctor = doctors.get_doctors_by_name(data['doctor']['name'])
                doctor_id = exist_doctor['id']

            updated_on = datetime.now()
            account_locked = data['accountLocked']
            name = data['name']
            if data['accountLocked'] == False:
                status = 'ACTIVE'
                enabled = True
            else:
                status = 'DEACTIVATED'
                enabled = True
            app_type = data['appType']
            role_user = data['roleType']

            cur = conection.conn.cursor()
            cur.execute("""UPDATE public.login_user SET
                                       "version" = "version" + 1, 
                                       updated_on = %s, 
                                       account_locked = %s,
                                       "name" = %s, 
                                       status = %s, 
                                       doctor_id = %s, 
                                       enabled = %s, 
                                       app_type = %s, 
                                       role_user = %s
                                     WHERE id = %s""",
                        (updated_on, account_locked, name, status, doctor_id,enabled, app_type, role_user, exist['id']))
            conection.conn.commit()
            cur.close()

    else:

        temporal_password = generate_random_password()
        pass_temp = temporal_password
        temporal_password = encrypt_pass(temporal_password)

        if data['roleType'] == 'ADMIN':
            version = 0
            password_expired = False
            account_expired = False
            created_on = datetime.now()
            username = data['username']
            updated_on = ''
            account_locked = data['accountLocked']
            name = data['name']
            password = temporal_password
            status = 'ACTIVE'
            temp_password = True
            doctor_id = ''
            enabled = True
            gid = ''
            app_type = data['appType']
            roleType = data['roleType']

            password = '{bcrypt}' + str(password).split("'")[1]
            cur = conection.conn.cursor()
            cur.execute("SELECT MAX(id) FROM public.login_user;")
            max = cur.fetchall()
            max = max[0][0]
            max_id = max + 1
            cur.execute("""INSERT INTO public.login_user
                            (id, "version", password_expired, account_expired, created_on, username, updated_on, account_locked,
                            "name", "password", status, temp_password, doctor_id, enabled, gid, app_type, role_user)
                             VALUES(%s, %s,%s,%s,%s,%s,null,%s,%s,%s,%s,%s,null ,%s,%s,%s,%s);""",
                        (max_id, version, password_expired, account_expired, created_on, username, account_locked, name, password,
                         status, temp_password, enabled, gid, app_type, roleType))
            conection.conn.commit()
            cur.close()
            link = ''
            emails.send_mail(pass_temp, username, name, link)
        else:

            result = doctors.get_doctors_by_name(data['doctor']['name'])
            print(result)
            print(temporal_password)
            version = 0
            password_expired = False
            account_expired = False
            created_on = datetime.now()
            username = data['username']
            updated_on = ''
            account_locked = data['accountLocked']
            name = data['name'].upper()
            password = temporal_password
            status = 'ACTIVE'
            temp_password = True
            doctor_id = result['id']
            enabled = True
            gid = ''
            app_type = data['appType']
            roleType = data['roleType']

            password = '{bcrypt}' + str(password).split("'")[1]

            cur = conection.conn.cursor()
            cur.execute("SELECT MAX(id) FROM public.login_user;")
            max = cur.fetchall()
            max = max[0][0]
            max_id = max + 1
            cur.execute("""INSERT INTO public.login_user
                            (id, "version", password_expired, account_expired, created_on, username, updated_on, account_locked,
                            "name", "password", status, temp_password, doctor_id, enabled, gid, app_type, role_user)
                            VALUES(%s,%s,%s,%s,%s,%s,null,%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s);""",
                        (max_id,version, password_expired, account_expired, created_on, username, account_locked, name, password,
                         status, temp_password, doctor_id, enabled, gid, app_type, roleType))


            conection.conn.commit()
            cur.close()
            ios_code = {}
            link = ''
            if app_type == 'IOS':
                cur = conection.conn.cursor()
                cur.execute("""SELECT id, link FROM public.ios_codes WHERE email is null   limit 1;""")
                values = cur.fetchall()
                cur.close()
                ios_code = {
                    'id': values[0][0],
                    'code': values[0][1]
                }
                link = ios_code['code']
                cur = conection.conn.cursor()
                cur.execute("""UPDATE public.ios_codes SET email = %s WHERE id = %s;""", (username, ios_code['id']))
                conection.conn.commit()
                cur.close()

            if app_type == 'ANDROID':
                link= 'https://www.google.com/url?q=https://play.google.com/store/apps/details?id%3Dcom.ievo.cobra&amp;source=gmail&amp;ust=1637826436805000&amp;usg=AOvVaw145bs0TizDfnYTxLDRXXQu'

            emails.send_mail(pass_temp, username, name, link)

    return

def generate_random_password():
    length = 4
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)

def encrypt_pass(temporal_password):
    pass_text_plano = temporal_password
    pass_text_plano = pass_text_plano.encode()
    sal = bcrypt.gensalt()
    pass_hasheada = bcrypt.hashpw(pass_text_plano, sal)
    return pass_hasheada

def verify_user(username, password):
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT password FROM public.login_user WHERE account_locked != true and status != 'DEACTIVATED' 
                        and username = '""" + username + """'""")
        result = cur.fetchall()
        cur.close()
        encrypt = result[0][0]
        encrypt = str(encrypt).split('{bcrypt}')[1]
        login = check(password, encrypt)
        return login
    except:
        conn = psycopg2.connect(host="cobra.cvc6fic9cofz.us-east-1.rds.amazonaws.com",
                                database="cobra",
                                user="postgres",
                                password="cobra2021*")
        cur = conection.conn.cursor()
        cur.execute("ROLLBACK")
        conection.conn.commit()
        cur.close()
        return False



def check(password, encrypt):
    password = password.encode()
    encrypt = encrypt.encode()

    if bcrypt.checkpw(password, encrypt):
        print("Ok, las contraseñas coinciden")
        return True
    else:
        print("Contraseña incorrecta")
        return False

def get_user():
    cur = conection.conn.cursor()
    # cur.execute("""SELECT username, "name", doctor_id, app_type, role_user FROM public.login_user""")
    cur.execute("""SELECT id, "name", username, account_locked, app_type, role_user, doctor_id FROM public.login_user 
                    WHERE status = 'ACTIVE' order by "name" asc """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in records:
        if result[6] is not None:
            aux = doctors.get_doctors_by_id(result[6])
            content = {
                'id': result[0],
                'name': result[1],
                'username': result[2],
                'accountLocked': result[3],
                'appType': result[4],
                'roleType': result[5],
                'doctor': {
                    'name': aux['name']
                }
            }
        else:
            content = {
                'id': result[0],
                'name': result[1],
                'username': result[2],
                'accountLocked': result[3],
                'appType': result[4],
                'roleType': result[5],
                'doctor': {
                    'name': ''
                }
            }
        payload.append(content)
        content = {}
        # content = {'username': result[0],
        #            'name': result[1],
        #            'doctor_id': result[2],
        #            'app_type': result[3],
        #            'role_user': result[4]}
    return payload

def get_data_user(username):
    cur = conection.conn.cursor()
    cur.execute("SELECT id, password_expired, username, status, doctor_id ,app_type, role_user, temp_password, terms_condition, name FROM public.login_user WHERE status = 'ACTIVE' and  username = '"+ username + "'")
    records = cur.fetchall()
    content = {}
    for result in records:
        if result[6] == 'DOCTOR_USER':
            isDoctor = True
        else:
            isDoctor = False
        content = {
            'id': result[0],
            'password_expired': result[1],
            'username': result[2],
            'status': result[3],
            'doctor_id': result[4],
            'app_type': result[5],
            'role_user': result[6],
            'temp_password': result[7],
            'terms_condition': result[8],
            'isDoctor': isDoctor,
            'name': result[9]
        }
    return content

    return

def update_password(info, token):
    info_user = validate_token(token, True)
    password = info['password']
    password = encrypt_pass(password)
    password = '{bcrypt}' + str(password).split("'")[1]
    cur = conection.conn.cursor()
    cur.execute("""UPDATE public.login_user
                    SET  "password"=%s, temp_password=false WHERE username=%s;""", (password, info_user['username']))
    conection.conn.commit()
    cur.close()
    return

def update_password_temp(info, token):
    info_user = validate_token(token, True)
    print(info_user)
    cur = conection.conn.cursor()
    cur.execute("""SELECT password FROM public.login_user WHERE username = '""" + info_user['username'] + """'""")
    result = cur.fetchall()
    cur.close()
    encrypt = result[0][0]
    encrypt = str(encrypt).split('{bcrypt}')[1]
    login = check(info['oldPassword'], encrypt)


    print(login)
    if login == True:
        password = '{bcrypt}' + str(encrypt_pass(info['password'])).split("'")[1]
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.login_user
                        SET  "password"=%s, temp_password=false WHERE username=%s;""", (password, info_user['username']))
        conection.conn.commit()
        cur.close()
        return True
    else:
        return False

    # # old_password = info['password']
    # # password = encrypt_pass(old_password)
    # # password = '{bcrypt}' + str(password).split("'")[1]
    # # cur = conection.conn.cursor()
    # # cur.execute("""UPDATE public.login_user
    # #                 SET  "password"=%s, temp_password=false WHERE username=%s;""", (password, info_user['username']))
    # # conection.conn.commit()
    # # cur.close()
    # return

def terms(info, token):
    info_user = validate_token(token, True)
    cur = conection.conn.cursor()
    cur.execute("""UPDATE public.login_user SET  terms_condition=true WHERE username= '""" + str(info_user['username']) + """'""")
    conection.conn.commit()
    cur.close()
    return

def get_user_info(info):
    print(info)
    return

def resend_pass(user):
    try:
        temporal_password = generate_random_password()
        pass_temp = temporal_password
        temporal_password = encrypt_pass(temporal_password)
        password = temporal_password
        password = '{bcrypt}' + str(password).split("'")[1]
        cur = conection.conn.cursor()
        cur.execute("""SELECT username, "name", app_type FROM public.login_user WHERE username = '""" + user + """'""")
        records = cur.fetchall()
        cur.close()
        content = {}
        for i in records:
            content = {
                'username': i[0],
                'name': i[1],
                'pass_temp': pass_temp,
                'password': password,
                'app_type': i[2],
            }

        # ios_code = {}
        # if content['app_type'] == 'IOS':
        #     cur = conection.conn.cursor()
        #     cur.execute("""SELECT id, link FROM public.ios_codes WHERE email is null   limit 1;""")
        #     values = cur.fetchall()
        #     cur.close()
        #     ios_code = {
        #         'id': values[0][0],
        #         'code': values[0][1]
        #     }

        # print(content)
        # print(ios_code)
        print(content)
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.login_user SET "password"=%s, temp_password=true WHERE username=%s;""", (content['password'], content['username']))
        conection.conn.commit()
        # cur.execute("""UPDATE public.ios_codes SET email = %s WHERE id = %s;""", (content['username'], ios_code['id']))
        # conection.conn.commit()
        cur.close()

        emails.send_mail_recovery(content['pass_temp'], content['username'], content['name'])

        return
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return False

def forgot(user):
    try:
        temporal_password = generate_random_password()
        pass_temp = temporal_password
        temporal_password = encrypt_pass(temporal_password)
        password = temporal_password
        password = '{bcrypt}' + str(password).split("'")[1]
        cur = conection.conn.cursor()
        cur.execute("""SELECT username, "name", app_type FROM public.login_user WHERE status = 'ACTIVE' and username = '""" + user + """'""")
        records = cur.fetchall()
        cur.close()
        print(records)
        if len(records) == 0:
            return False
        else:
            content = {}
            for i in records:
                content = {
                    'username': i[0],
                    'name': i[1],
                    'pass_temp': pass_temp,
                    'password': password,
                    'app_type': i[2],
                }

            print(content)
            cur = conection.conn.cursor()
            cur.execute("""UPDATE public.login_user SET "password"=%s, temp_password=true WHERE username=%s;""", (content['password'], content['username']))
            conection.conn.commit()
            # cur.execute("""UPDATE public.ios_codes SET email = %s WHERE id = %s;""", (content['username'], ios_code['id']))
            # conection.conn.commit()
            cur.close()

            emails.send_mail_recovery(content['pass_temp'], content['username'], content['name'])

            return True
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return False

def sendIos_code(user):
    try:
        cur = conection.conn.cursor()
        cur.execute("""SELECT username, "name", app_type FROM public.login_user WHERE username = '""" + user + """'""")
        records = cur.fetchall()
        cur.close()
        content = {}
        for i in records:
            content = {
                'username': i[0],
                'name': i[1],
                'app_type': i[2],
            }

        cur = conection.conn.cursor()
        cur.execute("""SELECT id, link FROM public.ios_codes WHERE email is null   limit 1;""")
        values = cur.fetchall()
        cur.close()
        ios_code = {
            'id': values[0][0],
            'code': values[0][1]
        }

        emails.send_mail_ios(content['username'], content['name'], ios_code['code'])
        cur = conection.conn.cursor()
        cur.execute("""UPDATE public.ios_codes SET email = %s WHERE id = %s;""", (content['username'], ios_code['id']))
        conection.conn.commit()
        cur.close()
        return
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return

def delete_user(id):
    try:
        cur = conection.conn.cursor()
        cur.execute("UPDATE public.login_user SET enabled = false, status = 'DEACTIVATED' WHERE id =" + str(id))
        conection.conn.commit()
        cur.close()
        return
    except:
        curs = conection.conn.cursor()
        curs.execute("ROLLBACK")
        conection.conn.commit()
        curs.close()
        return


def user_download():
    cur = conection.conn.cursor()
    cur.execute("""
        select 
            lu.username, 
            lu."name", 
            lu.role_user,
            d."name" 
        from public.login_user lu
        LEFT join 
            public.doctor d 
            on lu.doctor_id = d.id 
        WHERE  lu.status = 'ACTIVE' ORDER BY d."name"  
    """)
    records = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for i in records:
        content = {
            'username': i[0],
            'name': i[1],
            'role_user': i[2],
            'doctor_name': i[3],
        }
        payload.append(content)
        content = {}
    return payload
