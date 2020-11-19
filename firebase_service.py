from datetime import datetime

import pyrebase
import ujson as ujson

with open("./config.json") as file_pointer:
    CONFIG = ujson.load(file_pointer)

firebase = pyrebase.initialize_app(CONFIG)
DATA = firebase.database()


class Server:

    def __init__(self):
        self.id = None
        self.name = None
        self.office = None
        self.departament = None
        self.process = None
        self.reason = None
        self.delete = None
        self.type_number = None
        self.type_process = None
        self.contact = None
        self.evaluate_date = None
        self.bi_annually_ld = None
        self.bi_annually_nd = None
        self.quarterly_ld = None
        self.quarterly_nd = None

    def set_id(self, Id):
        self.id = Id

    def get_id(self):
        return str(self.id)

    def set_evaluate_date(self, date):
        self.evaluate_date = date

    def get_evaluate_date(self):
        return self.evaluate_date

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return str(self.name)

    def set_office(self, office):
        self.office = office

    def get_office(self):
        return self.office

    def set_departament(self, departament):
        self.departament = departament

    def get_departament(self):
        return self.departament

    def set_process(self, process):
        self.process = process

    def get_process(self):
        return self.process

    def set_reason(self, reason):
        self.reason = reason

    def get_reason(self):
        return self.reason

    def set_delete(self, delete):
        self.delete = delete

    def get_delete(self):
        return self.delete

    def set_type_number(self, type_number):
        self.type_number = type_number

    def get_type_number(self):
        return int(self.type_number)

    def set_type_process(self, type_process):
        self.type_process = str(type_process)

    def get_type_process(self):
        return self.type_process

    def set_contact(self, contact):
        self.contact = contact

    def get_contact(self):
        return self.contact

    def set_delete(self, delete):
        self.delete = delete

    def get_delete(self):
        return self.delete

    def set_biannually_ld(self, biannually_ld):
        self.bi_annually_ld = biannually_ld

    def get_biannually_ld(self):
        return self.bi_annually_ld

    def set_biannually_nd(self, biannually_nd):
        self.bi_annually_nd = biannually_nd

    def get_biannually_nd(self):
        return self.bi_annually_nd

    def set_quarterly_ld(self, quarterly_ld):
        self.quarterly_ld = quarterly_ld

    def get_quarterly_ld(self):
        return self.quarterly_ld

    def set_quarterly_nd(self, quarterly_nd):
        self.quarterly_nd = quarterly_nd

    def get_quarterly_nd(self):
        return self.quarterly_nd


class Remark():
    def __init__(self):
        self.edited = False
        self.time = datetime.now().strftime('%Y/%m/%d')
        self.id_server = None
        self.about = None
        self.remark = None
        self.id = None

    def get_edit(self):
        return self.edited

    def change_edit(self):
        self.edited = not self.edited

    def get_id(self):
        return self.id

    def set_id(self, Id):
        self.id = Id

    def get_time(self):
        return self.time

    def set_time(self, date):
        self.time = date

    def set_idServer(self, id):
        self.id_server = id

    def get_idServer(self):
        return self.id_server

    def set_about(self, about):
        self.about = about

    def get_about(self):
        return str(self.about)

    def set_remark(self, note):
        self.remark = note

    def get_remark(self):
        return str(self.remark)
