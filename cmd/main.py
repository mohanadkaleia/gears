# import os
# import sys
# import inspect

from app.database import db
from app.models import shops, services, vehicles
from app.models.shops import Shop, ShopRepo
from app.models.services import Service, ServiceRepo
from app.models.vehicles import Vehicle, VehicleRepo

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

# from app.models import services, shops  # noqa


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


def create_shop(name=""):
    repo = ShopRepo(db)

    if not name:
        raise ErrInvalidParameters("name is required")

    try:
        shop = repo.get_by_name(name)
        shop_id = shop.id
    except shops.ErrNotFound:
        new_shop = Shop(name=name,
                        description="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent purus ipsum, bibendum et metus quis, cursus hendrerit libero. Etiam aliquam, metus eu cursus dictum, risus ante volutpat augue""")
        shop_id = repo.insert(**new_shop.__dict__)
    print(f"Created shop with id {shop_id}")
    return shop_id


def create_services(shop_id=None):
    repo = ServiceRepo(db)
    seeds = [
        {
            "name": "Detail",
            "description": "Get the absolute best look for your paintwork and surfaces. A clean or a valet is about making sure all surfaces are, well, clean.",
            "price": 40,
            "images": ["/static/images/detail_service.jpeg"],
        },
        {
            "name": "Lube, Oil, and Filters",
            "images": ["/static/images/detail_service.jpeg"],
            "price": 40,
            "description": """An oil change and filter replacement is one of many preventative maintenance services that help promote maximum vehicle performance while extending the life of your vehicle.
            Oil is responsible for lubricating the working components inside your vehicle's engine while reducing the amount of friction between them.""",
        },
        {
            "name": "Inspection",
            "images": ["/static/images/detail_service.jpeg"],
            "price": 40,
            "description": """Vehicle inspection is a procedure mandated by national or subnational governments in many countries,
            in which a vehicle is inspected to ensure that it conforms to regulations governing safety, emissions, or both. Inspection can be required at various times,
            e.g., periodically or on the transfer of title to a vehicle.""",
        },
        {
            "name": "Tire Installation",
            "price": 40,
            "images": ["/static/images/tire_installation.jpeg"],
            "description": "Comming soon",
        },
    ]

    for service in seeds:
        try:
            repo.get_by_name(service["name"])
        except services.ErrNotFound:
            new_service = Service(shop_id=shop_id, **service)
            repo.insert(**new_service.__dict__)
            print(f"Service {new_service.name} has been added")


def create_vehicles(shop_id):
    repo = VehicleRepo(db)
    if not shop_id:
        raise ErrInvalidParameters("shop_id is required")

    vehicles_number = 3

    # We only need to add 3 vehicles
    try:
        result = repo.all()
    except vehicles.ErrVehicleNotFound:
        result = []

    if len(result) >= vehicles_number:
        return

    makes = ["mazda", "toyota", "honda"]
    models = ["mx5", "corolla", "civic"]

    for x in range(vehicles_number - len(result)):
        new_vehicle = Vehicle(shop_id=shop_id,
                              make=makes[x],
                              model=models[x],
                              year="2015",
                              price="10000",
                              title="clean",
                              condition="good",
                              description="nice car")
        vehicle_id = repo.insert(**new_vehicle.__dict__)
        print(f"a vehicle with id {vehicle_id} has been created")


def main():
    shop_id = create_shop("DKLube & Detail")
    create_services(shop_id)
    create_vehicles(shop_id)


if __name__ == "__main__":
    main()
