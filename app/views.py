from app.config import get_config
from flask import render_template, request, jsonify, abort, flash
from app import app, util
import app.models.vehicles as vehicles_model
import app.models.promos as promos_model
import app.models.services as services_model
import app.models.appointments as appintments_model

from app.third_parties import sendemail

config = get_config()


@app.route("/")
def index():
    vehicles = vehicles_model.all() or []
    promos = promos_model.all() or []
    services = services_model.all() or []

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


@app.route("/admin/services")
def admin_services_management():
    services = services_model.all()
    return render_template("admin/services/index.html", services=services)


@app.route("/admin/services/adding", methods=["GET", "POST"])
def admin_services_adding():
    if request.method == "POST":
        images = None
        if request.files.getlist("images"):
            images = util.upload_files(
                request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
            )

        price = [price.split(",") for price in request.form.getlist("price")]
        services_model.insert(
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=images,
        )
        flash('Service has been created')
        return jsonify(data="OK")
    return render_template("admin/services/upsert.html", mode="add")


@app.route("/admin/services/<id>/editing", methods=["GET", "POST"])
def admin_services_editing(id: str):
    service = {}
    try:
        service = services_model.get(id=id)
    except services_model.ErrNotFound:
        abort(404)

    if request.method == "POST":
        # Convert to set to be able to - with rm images
        images = set(service["images"])
        rm_images = set(request.form.getlist('rmImages'))
        images -= rm_images

        # remove images from disk
        util.remove_files(list(rm_images), app.config["IMAGES_DIR_PATH"])

        if request.files.getlist("images"):
            uploaded_images = util.upload_files(
                request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
            )
            images |= set(uploaded_images)

        price = [price.split(",") for price in request.form.getlist("price")]
        services_model.update(
            id=service["id"],
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=list(images),
        )
        flash('Service has been updated')
        return jsonify(data="OK")
    else:
        return render_template("admin/services/upsert.html", service=service, mode="edit")


@app.route("/admin/services/<id>/deleting", methods=["POST"])
def admin_services_deleting(id):
    service = services_model.get(id)
    # Remove image of this service
    util.remove_files(service["images"], app.config['IMAGES_DIR_PATH'])
    services_model.delete(id)
    flash("Service has been deleted")
    return jsonify(message="OK")


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


@app.route("/appointment")
def appointment():
    booked_appointments = appintments_model.get_booked_slots()
    timeslots = [a["timeslot"].date() for a in booked_appointments]
    print(timeslots)
    data = {"appointments": timeslots}
    return render_template("appointment.html", config=config, data=data)


@app.errorhandler(404)
def page_not_found(error):
    return "oops.. page not found 😝"
