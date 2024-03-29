from datetime import datetime

from app.config import get_config
from flask import render_template, request, Blueprint, redirect, url_for

import app.models.vehicles as vehicles_model
import app.models.promos as promos_model
import app.models.shops as shops_model
import app.models.services as services_model
import app.models.appointments as appointment_model

from app.third_parties import sendgrid

config = get_config()
bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    vehicles = vehicles_model.all() or []
    promos = promos_model.all() or []
    services = services_model.all() or []

    content = {"vehicles": vehicles, "services": services, "promos": promos}

    return render_template("index.html", config=config, content=content)


@bp.route("/services/<id>")
def services_detail(id):
    service = services_model.get(id)
    return render_template("service_detail.html", service=service, config=config)


@bp.route("/inventory")
def inventory():
    vehicles = vehicles_model.all()
    return render_template("inventory.html", config=config, vehicles=vehicles)


@bp.route("/inventory/<id>")
def get_vehicle(id):
    try:
        # Search for the vehicle and render it
        data = vehicles_model.get(id)
        return render_template("vehicle_details.html", config=config, vehicle=data)
    except vehicles_model.ErrNotFound:
        # TODO: return a 404 page
        return "oops not vehicle found"


@bp.route("/contact")
def contact():
    return render_template("contact.html", config=config)


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/send_email", methods=["POST"])
def send_email():
    from_email = request.form["from_email"]
    to_address = config["TO_EMAIL_ADDRESS"]
    bcc_address = config["BCC_EMAIL_ADDRESS"]
    subject = request.form["subject"]
    content = request.form["content"]

    try:
        sendgrid.send(from_email, to_address, bcc_address, subject, content)
    except sendgrid.ErrSendEmail:
        return "oops, my bird just chewed the cable and we can't send your email now 😢.. please try again later "

    return "email sent 🥴"


@bp.route("/appointment")
def appointment():
    booked_appointments = appointment_model.get_booked_slots()
    timeslots = [a["timeslot"].date() for a in booked_appointments]
    locked_slots = {}
    # locked_slots: Is for dynamic lock days on the calendar in the front-end
    for a in booked_appointments:
        service = services_model.get(a["service_id"])
        if "max_slot" in service:
            if service["id"] not in locked_slots:
                locked_slots[service["id"]] = []
            locked_slots[service["id"]].append(str(a["timeslot"].date()))
    shops = shops_model.all() or []
    services = services_model.all() or []
    data = {
        "shops": shops,
        "services": services,
        "appointments": timeslots,
        "locked_slots": locked_slots,
    }
    return render_template("appointment.html", config=config, data=data)


@bp.route("/appointment", methods=["POST"])
def save_appointment():
    timeslot = datetime.strptime(request.form.get("timeslot"), "%Y-%m-%d")
    try:
        appointment_model.insert(
            shop_id=None,
            service_id=request.form.get("service"),
            timeslot=timeslot,
            vehicle=request.form.get("vehicle"),
            name=request.form.get("name"),
            email=request.form.get("email"),
            description=request.form.get("description"),
        )
    except appointment_model.ErrInvalidParameters as e:
        return e
    else:
        text_body = f"""New appointment has been created
                    - Name: {request.form.get("name")}
                    - Email: {request.form.get("email")}
                    - Service: {services_model.get(request.form.get("service"))["name"]}
                    - Timeslot: {timeslot}
                    - Vehicle: {request.form.get("vehicle")}
                    - Description: {request.form.get("description")}"""
        sendgrid.send(
            config["TO_EMAIL_ADDRESS"],
            config["TO_EMAIL_ADDRESS"],
            config["BCC_EMAIL_ADDRESS"],
            "New appointment has been created",
            text_body,
        )
        return redirect(url_for("home.appointment"))


@bp.errorhandler(404)
def page_not_found(error):
    return "oops.. page not found 😝"
