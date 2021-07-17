from flask import render_template, request, redirect, url_for, abort, jsonify

from app import forms, util
from app.config import get_config
from app import app
import app.models.promos as promos_model

from app.third_parties import sendemail
from app.models import services as services_model, vehicles as vehicles_model


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
    if request.method == "GET":
        return render_template("login.html")
    else:
        return redirect(url_for("services_management"))


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


@app.route("/admin/services")
def services_management():
    services = services_model.all()
    return render_template("admin/services/service_list.html", services=services)


@app.route("/admin/services/adding", methods=["GET", "POST"])
def services_adding():
    form = forms.FormNewServices()

    if form.validate_on_submit():
        # When the form is valid take it data and save to database
        # Upload images to disk and get files name if any
        images = util.upload_files(form.images.data, app.config["IMAGES_DIR_PATH"])
        services_model.insert(
            shop_id="FAKE SHOP ID",
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            images=images,
        )
        return redirect(url_for("services_management"))

    return render_template("admin/services/service_add.html", form=form)


@app.route("/admin/services/<id>/editing", methods=["GET", "POST"])
def services_editing(id: str):
    service = {}
    try:
        service = services_model.get(id=id)
    except services_model.ErrNotFound:
        abort(404)

    if request.method == "POST":
        images = service["images"]
        if request.files.getlist("images"):
            images = util.upload_files(
                request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
            )
            images = [f"/static/images/{filename}" for filename in images]

        price = [price.split(",") for price in request.form.getlist("price")]
        services_model.update(
            id=service["id"],
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=images,
        )
        return jsonify(data="OK")
    else:
        return render_template("admin/services/service_edit.html", service=service)
