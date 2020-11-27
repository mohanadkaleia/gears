import tinydb
import json

from slugify import slugify
from app import util


class ErrNotFound(Exception):
    pass

class ErrInvalidParameters(Exception):
    pass


# DB initializtion
db = tinydb.TinyDB('db.json')
services = db.table('services')

def insert(shop_id="", name="", description="", images=None):
    if not images: 
        images = []
    
    # Initialize id with randomly generated string
    service_id = util.random_id()

    services.insert({
        'service_id': service_id,
        'shop_id': shop_id, 
        'name': name, 
        'slug': slugify(name),
        'description': description, 
        'images': images,
    })

    # TODO: upload images into disk
    pass 

    return service_id


def delete(service_id):  
    query = tinydb.Query()         
    services.remove(query.vehicle_id == service_id)        


def all():    
    results = services.all()
    
    if not results:
        raise ErrNotFound(f'oops.. no service found in the db')
        
    return results
 

def get(service_id):    
    service = tinydb.Query()
    result = services.search(service.service_id == service_id)
    
    if not result:
        raise ErrNotFound(f'no service found for the provided id: {service_id}')
        
    return result[0]

def get_by_name(name=""):
    if not name:
        raise ErrInvalidParameters("service name must be provided")

    service = tinydb.Query()
    result = services.search(service.name == name)
    
    if not result:
        raise ErrNotFound(f'no service found for the provided name: {name}')
        
    return result[0]
    

    