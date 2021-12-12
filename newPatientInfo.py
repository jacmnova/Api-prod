import psycopg2
import conection
from flask import jsonify
import hospitals
import cid
import local
import doctors


def get_data_mobile():
    hospitals_ = hospitals.get_hospitals()
    cids_ = cid.get_cid()
    locals_ = local.get_locals()
    doctors_ = doctors.get_doctors()
    payload = []
    content = {}
    content = {'hospitals': hospitals_,
               'cids': cids_,
               'locals': locals_,
               'doctors': doctors_}

    payload.append(content)
    content = {}
    print(payload)
    return payload[0]


def get_data():
    hospitals_ = hospitals.get_hospitals()
    cids_ = cid.get_cid()
    locals_ = local.get_locals()
    doctors_ = doctors.get_doctors()
    print(doctors_)
    payload = []
    content = {}
    content = {'hospitals': hospitals_,
               'cids': cids_,
               'locals': locals_,
               'doctors': doctors_}

    payload.append(content)
    content = {}
    print(payload)
    return payload[0]