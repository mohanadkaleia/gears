import tinydb
import json

from app import util


class ErrVehicleNotFound(Exception):
    pass

class ErrVehicleAlreadyExisit(Exception):
    pass


# DB initializtion
db = tinydb.TinyDB('db.json')
vehicles = db.table('vehicles')


# CRUD functions 
def insert(make="", model="", year="", price="", title="", condition="", description="", images=None):
    # Initialize id with randomly generated string
    vehicle_id = util.random_id()

    if not images:
        images = []

    # TODO: add shop id as a FK
    vehicles.insert({
        'vehicle_id': vehicle_id,
        'make': make,
        'model': model, 
        'year': year, 
        'price': price, 
        'title': title, 
        'condition': condition, 
        'description': description, 
        'images': images,
    })

    # TODO: Upload images into disk
    pass

    return vehicle_id


def delete(vehicle_id):  
    query = tinydb.Query()         
    vehicles.remove(query.vehicle_id == vehicle_id)        


def all():    
    results = vehicles.all()
    
    if not results:
        raise ErrVehicleNotFound(f'oops.. no vehicles found in the db')
        
    return results
 


def get(vehicle_id):    
    vehicle = tinydb.Query()
    result = vehicles.search(vehicle.vehicle_id == vehicle_id)
    
    if not result:
        raise ErrVehicleNotFound(f'no vehicle found for the provided id: {vehicle_id}')
        
    return result[0]


def find(make="", model="", year=""):
    pass