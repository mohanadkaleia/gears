import json
from datetime import datetime

from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required

from app.models import appointments as appt_model
from app.models import services as service_model
from app.models import shops as shop_model


bp = Blueprint("appointments", __name__)


@bp.route("/admin/appointments")
@login_required
def admin_appointments_management():
    data = appt_model.all()
    events = []
    for appt in data:
        event = {
            "id": appt["id"],
            "title": appt["name"],
            "start": str(appt["timeslot"]),
            "allDay": True,
        }
        if appt["timeslot"] < datetime.now():
            event["backgroundColor"] = "#989898"
            event["borderColor"] = "#989898"
        events.append(event)
    return render_template(
        "admin/appointments/index.html",
        active_nav="appointments",
        appointments=json.dumps(events),
    )


@bp.route("/admin/appointments/view/upsert", methods=["POST"])
def admin_render_upsert_form():
    shops = shop_model.all()
    services = service_model.all()
    try:
        appt = appt_model.get(request.form.get("id"))
        appt.timeslot = str(appt["timeslot"].date())
    except appt_model.ErrNotFound:
        appt = None
    return render_template(
        "admin/appointments/upsert_form.html", appt=appt, shops=shops, services=services
    )


@bp.route("/admin/appointments/save", methods=["POST"])
@login_required
def admin_save_appointment():
    try:
        appt_model.get(request.form.get("id"))
        appt_model.update(
            id=request.form["id"],
            shop_id=request.form.get("shop"),
            service_id=request.form.get("service"),
            timeslot=datetime.strptime(request.form.get("timeslot"), "%Y-%m-%d"),
            vehicle=request.form.get("vehicle"),
            name=request.form.get("name"),
            email=request.form.get("email"),
            description=request.form.get("description"),
        )
        flash("Appointment has been updated")
    except appt_model.ErrNotFound:
        appt_model.insert(
            shop_id=request.form.get("shop"),
            service_id=request.form.get("service"),
            timeslot=datetime.strptime(request.form.get("timeslot"), "%Y-%m-%d"),
            vehicle=request.form.get("vehicle"),
            name=request.form.get("name"),
            email=request.form.get("email"),
            description=request.form.get("description"),
        )
        flash("New appointment has been added")
    except Exception as e:
        raise e
    finally:
        return redirect(url_for("appointments.admin_appointments_management"))


@bp.route("/admin/appointments/<id>/delete", methods=["POST"])
@login_required
def admin_delete_appointment(id):
    appt_model.delete(id)
    flash(f"Appointment {id} deleted", "info")
    return redirect(url_for("appointments.admin_appointments_management"))
