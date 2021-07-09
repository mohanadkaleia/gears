from flask import render_template, request, redirect, url_for, abort

from app import app, forms, util
from app.config import get_config
from app.database import db
from app.third_parties import sendemail
from app.models import services, vehicles
from app.models.services import Service, ServiceRepo
from app.models.vehicles import Vehicle, VehicleRepo


config = get_config()


@app.route("/")
def index():
    vehicle_repo = VehicleRepo(db)
    shop_repo = ServiceRepo(db)
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

    services = shop_repo.all()
    vehicles = vehicle_repo.all()
    return render_template(
        "index.html", config=config, services=services, vehicles=vehicles[:3]
    )


@app.route("/inventory")
def inventory():
    vehicle_repo = VehicleRepo(db)
    vehicles = vehicle_repo.all()
    return render_template("inventory.html", config=config, vehicles=vehicles)


@app.route("/inventory/<id>")
def get_vehicle(id):
    try:
        vehicle_repo = VehicleRepo(db)
        # Search for the vehicle and render it
        data = vehicle_repo.get(id)
        return render_template("vehicle_details.html", config=config, vehicle=data)
    except vehicles.ErrVehicleNotFound:
        # TODO: return a 404 page
        return "oops not vehicle found"


@app.route("/vehicle/add")
def vehicle_add():
    return render_template("vehicle_add.html")


@app.route("/vehicle/save", methods=["POST"])
def vehicle_save():
    vehicle_repo = VehicleRepo(db)

    make = request.form["make"]
    model = request.form["model"]
    year = request.form["year"]
    condition = request.form["condition"]
    title = request.form["title"]
    price = request.form["price"]

    vehicle_id = vehicle_repo.insert(
        make=make, model=model, year=year, price=price, title=title, condition=condition
    )
    return "Success " + vehicle_id


@app.route("/vehicle/delete", methods=["POST"])
def vehicle_delete():
    vehicle_repo = VehicleRepo(db)
    vehicle_id = request.form["vehicle_id"]
    vehicle_repo.delete(vehicle_id)
    return "vehicle deleted"


@app.route("/contact")
def contact():
    return render_template("contact.html", config=config)


@app.route("/admin")
def admin():
    vehicle_repo = VehicleRepo(db)
    vehicles = vehicle_repo.all()
    services = []
    return render_template("admin.html", vehicles=vehicles, services=services)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return redirect(url_for('services_management'))


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


@app.route("/admin/services")
def services_management():
    repo = ServiceRepo(db)
    services = repo.all()
    return render_template('admin/services/service_list.html', services=services)


@app.route("/admin/services/adding", methods=['GET', 'POST'])
def services_adding():
    form = forms.FormNewServices()

    if form.validate_on_submit():
        # When the form is valid take it data and save to database
        repo = ServiceRepo(db)

        service = Service.populate(form)
        service.images = util.upload_files(form.images.data, service.upload_dir)
        repo.insert(id=service.id,
                    shop_id=service.shop_id,
                    name=service.name,
                    slug=service.slug,
                    price=service.price,
                    description=service.description,
                    images=service.images)
        return redirect(url_for('services_management'))

    return render_template('admin/services/service_add.html', form=form)


@app.route("/admin/services/<id>/editing", methods=['GET', 'POST'])
def services_editing(id: str):
    repo = ServiceRepo(db)

    try:
        service = repo.get(id=id)
    except services.ErrNotFound:
        abort(404)

    form = forms.FormNewServices(obj=service)

    if form.validate_on_submit():
        service = Service.populate_edit(service, form)
        service.images = util.upload_files(form.images.data, service.upload_dir)
        repo.update(id=service.id,
                    name=service.name,
                    slug=service.slug,
                    price=service.price,
                    description=service.description,
                    images=service.images)
        return redirect(url_for('services_management'))

    return render_template('admin/services/service_edit.html', form=form, service=service)
