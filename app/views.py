from flask import render_template, request
from app import app
from app.models import vehicle
from app.third_parties import sendemail


config = {"SITEURL": "http://localhost:5000"}


@app.route("/")
def index():

    # shop_id = shops.insert(
    #     name="DKLube",
    #     description="Auto services",
    #     logo="logo",
    #     phone="",
    #     email="mohahad@kaleia.io",
    #     hours={
    #         "monday": "9 - 6",
    #         "Friday": "9 - 3"
    #     }
    # )

    # TODO: this should be taken from db not hardcoded :)
    services = [
        {
            "slug": "detail",
            "cover": "/static/images/detail_service.jpeg",
            "title": "Detail",
            "summary": "Get the absolute best look for your paintwork and surfaces. A clean or a valet is about making sure all surfaces are, well, clean.",
        },
        {
            "slug": "lube_oil_and_filters",
            "cover": "http://dklube.com/assets/images/samples/390x260/image_02.jpg",
            "title": "Lube, Oil, and Filters",
            "summary": """An oil change and filter replacement is one of many preventative maintenance services that help promote maximum vehicle performance while extending the life of your vehicle.
            Oil is responsible for lubricating the working components inside your vehicle's engine while reducing the amount of friction between them.""",
        },
        {
            "slug": "inspection",
            "cover": "http://dklube.com/assets/images/samples/390x260/image_03.jpg",
            "title": "Inspection",
            "summary": """Vehicle inspection is a procedure mandated by national or subnational governments in many countries, in which a vehicle is inspected to ensure that it conforms to regulations governing safety, emissions, or both.
            Inspection can be required at various times, e.g., periodically or on the transfer of title to a vehicle.""",
        },
        {
            "slug": "tire_installation",
            "cover": "/static/images/tire_installation.jpeg",
            "title": "Tire Installation",
            "summary": "Comming soon",
        },
    ]

    vehicles = vehicle.all()
    return render_template(
        "index.html", config=config, services=services, vehicles=vehicles[:3]
    )


@app.route("/inventory")
def inventory():
    vehicles = vehicle.all()
    return render_template("inventory.html", config=config, vehicles=vehicles)


@app.route("/inventory/<id>")
def get_vehicle(id):
    try:
        # Search for the vehicle and render it
        data = vehicle.get(id)
        return render_template("vehicle_details.html", config=config, vehicle=data)
    except vehicle.ErrVehicleNotFound:
        # TODO: return a 404 page
        return "oops not vehicle found"


@app.route("/vehicle/add")
def vehicle_add():
    return render_template("vehicle_add.html")


@app.route("/vehicle/save", methods=["POST"])
def vehicle_save():
    make = request.form["make"]
    model = request.form["model"]
    year = request.form["year"]
    condition = request.form["condition"]
    title = request.form["title"]
    price = request.form["price"]

    vehicle_id = vehicle.insert(
        make=make, model=model, year=year, price=price, title=title, condition=condition
    )
    return "Success " + vehicle_id


@app.route("/vehicle/delete", methods=["POST"])
def vehicle_delete():
    vehicle_id = request.form["vehicle_id"]
    vehicle.delete(vehicle_id)
    return "vehicle deleted"


@app.route("/contact")
def contact():
    return render_template("contact.html", config=config)


@app.route("/admin")
def admin():
    vehicles = vehicle.all()
    services = []
    return render_template("admin.html", vehicles=vehicles, services=services)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    from_email = request.form["from_email"]
    subject = request.form["subject"]
    content = request.form["content"]

    try:
        sendemail.send(subject, from_email=from_email, content=content)
    except sendemail.ErrNoContentFound:
        return "error"

    return "email sent"
