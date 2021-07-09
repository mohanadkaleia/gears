import tinydb

from app import util


class ErrVehicleNotFound(Exception):
    pass


class ErrVehicleAlreadyExisit(Exception):
    pass


class VehicleRepo:

    # DB initializtion
    def __init__(self, db: tinydb.TinyDB):
        self.db = db
        self.vehicles = db.table('vehicles')


    # CRUD functions
    def insert(self, id="",
               shop_id=None,
               make="",
               model="",
               year="",
               price="",
               title="",
               condition="",
               description="",
               images=None,
               ):

        if not images:
            images = []

        # TODO: add shop id as a FK
        self.vehicles.insert({"id": id,
                              "shop_id": shop_id,
                              "make": make,
                              "model": model,
                              "year": year,
                              "price": price,
                              "title": title,
                              "condition": condition,
                              "description": description,
                              "images": images})

        # TODO: Upload images into disk
        pass

        return id


    def delete(self, vehicle_id):
        query = tinydb.Query()
        self.vehicles.remove(query.vehicle_id == vehicle_id)


    def all(self, ):
        results = self.vehicles.all()

        if not results:
            raise ErrVehicleNotFound("oops.. no vehicles found in the db")

        return results


    def get(self, vehicle_id):
        vehicle = tinydb.Query()
        result = self.vehicles.search(vehicle.vehicle_id == vehicle_id)

        if not result:
            raise ErrVehicleNotFound(f"no vehicle found for the provided id: {vehicle_id}")

        return result.pop()


    def find(self, make="", model="", year=""):
        pass


class Vehicle:
    def __init__(self, id: str = None,
                 shop_id: str = None,
                 make: str = None,
                 model: str = None,
                 year: int = None,
                 price: float = None,
                 title: str = None,
                 condition: str = None,
                 description: str = None,
                 images: list = None):
        self.id = id or util.random_id(initial="v")
        self.shop_id = shop_id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.title = title
        self.condition = condition
        self.description = description
        self.images = images
