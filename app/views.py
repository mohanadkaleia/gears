from app.config import get_config
from flask import render_template, request, abort, flash, redirect, url_for
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


@app.route("/admin/services/save", methods=["POST"])
def admin_services_save():
    updated_images = None
    if request.files.getlist("images"):
        updated_images = util.upload_files(
            request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
        )
    price = {
        price[0]: price[1]
        for price in list(
            zip(
                request.form.getlist("price_names[]"),
                request.form.getlist("price_values[]"),
            )
        )
    }
    try:
        service = services_model.get(id=request.form.get("service_id"))
        # get current set of images
        images = set(service["images"])
        # add updated images if any
        images |= set(updated_images)

        services_model.update(
            id=service["id"],
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=list(images),
        )
        flash("Service has been updated")
        return redirect(url_for("admin_services_edit", id=service["id"]))
    except services_model.ErrNotFound:
        images = updated_images or None
        services_model.insert(
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=images,
        )
        flash("Service has been created")
        return redirect(url_for("admin_services_add"))


@app.route("/admin/services/add")
def admin_services_add():
    return render_template("admin/services/upsert.html", mode="add")


@app.route("/admin/services/<id>/images/remove", methods=["POST"])
def admin_services_images_remove(id):
    try:
        # remove images from disk if any
        rm_image = request.form.get("image")
        util.remove_files([rm_image], app.config["IMAGES_DIR_PATH"])

        service = services_model.get(id=id)
        # get current set of images and update it
        service["images"].remove(rm_image)

        services_model.update(
            id=service["id"],
            name=service["name"],
            price=service["price"],
            description=service["description"],
            images=service["images"],
        )
        flash("Removed image")
        return redirect(url_for("admin_services_edit", id=service["id"]))
    except services_model.ErrNotFound:
        abort(404)


@app.route("/admin/services/<id>/edit")
def admin_services_edit(id: str):
    try:
        service = services_model.get(id=id)
        return render_template(
            "admin/services/upsert.html", service=service, mode="edit"
        )
    except services_model.ErrNotFound:
        abort(404)


@app.route("/admin/services/<id>/delete", methods=["POST"])
def admin_services_deleting(id):
    service = services_model.get(id)
    # Remove image of this service
    util.remove_files(service["images"], app.config["IMAGES_DIR_PATH"])
    services_model.delete(id)
    flash("Service has been deleted")
    return redirect(url_for("admin_services_management"))


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
