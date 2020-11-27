import tinydb
import json


db = tinydb.TinyDB('db.json')
shops = db.table('shops')

def insert(name="", description="", logo="", phone="", email="", hours=""):
    return shops.insert({
        'name': name,
        'description': description, 
        'logo': logo, 
        'phone': phone, 
        'email': email, 
        'hours': hours
        } 
    )
