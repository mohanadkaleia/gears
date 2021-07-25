import datetime
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.models import services, shops, vehicles, promos, appointments  # noqa


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


def create_shop(name=""):
    if not name:
        raise ErrInvalidParameters("name is required")

    try:
        shop_id = shops.get_by_name(name)["id"]
    except shops.ErrNotFound:
        shop_id = shops.insert(
            name=name,
            description="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent purus ipsum, bibendum et metus quis, cursus hendrerit libero. Etiam aliquam, metus eu cursus dictum, risus ante volutpat augue,
            non placerat ante massa vel mauris. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut ut scelerisque. """,
        )

    print(f"Created shop with id {shop_id}")
    return shop_id


def create_services(shop_id=None):
    seeds = [
        {
            "name": "Detail",
            "description": "Get the absolute best look for your paintwork and surfaces. A clean or a valet is about making sure all surfaces are, well, clean.",
            "images": ["/static/images/detail_service.jpeg"],
        },
        {
            "name": "Lube, Oil, and Filters",
            "images": ["/static/images/detail_service.jpeg"],
            "description": """An oil change and filter replacement is one of many preventative maintenance services that help promote maximum vehicle performance while extending the life of your vehicle.
            Oil is responsible for lubricating the working components inside your vehicle's engine while reducing the amount of friction between them.""",
        },
        {
            "name": "Inspection",
            "images": ["/static/images/detail_service.jpeg"],
            "description": """Vehicle inspection is a procedure mandated by national or subnational governments in many countries,
            in which a vehicle is inspected to ensure that it conforms to regulations governing safety, emissions, or both. Inspection can be required at various times,
            e.g., periodically or on the transfer of title to a vehicle.""",
        },
        {
            "name": "Tire Installation",
            "images": ["/static/images/tire_installation.jpeg"],
            "description": "Comming soon",
        },
    ]
    services_ids = []
    for service in seeds:
        try:
            service = services.get_by_name(service["name"])
            services_ids.append(service["id"])
        except services.ErrNotFound:
            id = services.insert(
                shop_id=shop_id,
                name=service["name"],
                description=service["description"],
            )
            services_ids.append(id)
            print(f"Service {service['name']} has been added")

    return services_ids


def create_vehicles(shop_id):
    if not shop_id:
        raise ErrInvalidParameters("shop_id is required")

    vehicles_number = 3

    # We only need to add 3 vehicles
    result = vehicles.all()

    if len(result) >= vehicles_number:
        return

    makes = ["mazda", "toyota", "honda"]
    models = ["mx5", "corolla", "civic"]

    for x in range(vehicles_number - len(result)):
        vehicle_id = vehicles.insert(
            shop_id=shop_id,
            make=makes[x],
            model=models[x],
            year="2015",
            price="10000",
            title="clean",
            condition="good",
            description="nice car",
        )

        print(f"a vehicle with id {vehicle_id} has been created")


def create_promo(shop_id):
    code = "5DOLLARS_DISCOUNT"
    try:
        promo_id = promos.get_by_code(code)["id"]
    except promos.ErrNotFound:
        promo_id = promos.insert(
            shop_id,
            code=code,
            description="Claim your discount when using any service at dklube",
        )

    print(f"a promo with id {promo_id} has been created")


def create_appointments(shop_id, service_id):
    # insert two appointments
    appointments.insert(
        shop_id,
        service_id,
        datetime.datetime.today(),
        "mohanad",
        "mohanad.kaleia@gmail.com",
        "mazda",
        "need some detailing work",
    )
    appointments.insert(
        shop_id,
        service_id,
        datetime.datetime.today() + datetime.timedelta(1),
        "mohanad",
        "mohanad.kaleia@gmail.com",
        "toyota",
        "need some oid change work",
    )


def main():
    shop_id = create_shop("DKLube & Detail")
    s_ids = create_services(shop_id=shop_id)
    create_vehicles(shop_id)
    create_promo(shop_id)
    create_appointments(shop_id, s_ids[0])


if __name__ == "__main__":
    pass
