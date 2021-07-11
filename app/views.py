from app.config import get_config
from flask import render_template, request
from app import app
import app.models.vehicles as vehicles_model
import app.models.promos as promos_model
import app.models.services as services_model

from app.third_parties import sendemail

config = get_config()


@app.route("/")
def index():
    vehicles = vehicles_model.all()
    promos = promos_model.all()
    services = services_model.all()

    content = {"vehicles": vehicles, "services": services, "promos": promos}

    return render_template("index.html", config=config, content=content)


@app.route("/inventory")
def inventory():
    vehicles = vehicles_model.all()
    return render_template("inventory.html", config=config, vehicles=vehicles)


@app.route("/inventory/<id>")
def get_vehicle(id):
    try:
        # Search for the vehicle and render it
        data = vehicles_model.get(id)
        return render_template("vehicle_details.html", config=config, vehicle=data)
    except vehicles_model.ErrVehicleNotFound:
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

    vehicle_id = vehicles_model.insert(
        make=make, model=model, year=year, price=price, title=title, condition=condition
    )
    return "Success " + vehicle_id


@app.route("/vehicle/delete", methods=["POST"])
def vehicle_delete():
    vehicle_id = request.form["vehicle_id"]
    vehicles_model.delete(vehicle_id)
    return "vehicle deleted"


@app.route("/contact")
def contact():
    return render_template("contact.html", config=config)


@app.route("/admin")
def admin():
    vehicles = vehicles_model.all()
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


@app.errorhandler(404)
def page_not_found(error):
    return "oops.. page not found 😝"
