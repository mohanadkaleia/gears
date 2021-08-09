from flask import render_template, request, Blueprint, flash, redirect, abort, url_for
from flask_login import login_required

from app import app, util
import app.models.vehicles as vehicle_model


bp = Blueprint("vehicles", __name__)


@bp.route("/admin/vehicles")
@login_required
def admin_vehicles_management():
    vehicles = vehicle_model.all()
    return render_template(
        "admin/vehicles/index.html", vehicles=vehicles, active_nav="vehicle"
    )


@bp.route("/admin/vehicles/save", methods=["POST"])
@login_required
def admin_vehicles_save():
    uploaded_images = None
    if request.files.getlist("images"):
        uploaded_images = util.upload_files(
            request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
        )

    try:
        vehicle = vehicle_model.get(id=request.form.get("vehicle_id"))
        # get current set of images
        images = set(vehicle["images"])
        # add updated images if any
        images |= set(uploaded_images)

        vehicle_model.update(
            id=vehicle["id"],
            make=request.form["make"],
            model=request.form["model"],
            year=request.form["year"],
            trim=request.form["trim"],
            engine=request.form["engine"],
            title=request.form["title"],
            condition=request.form["condition"],
            drive=request.form["drive"],
            fuel=request.form["fuel"],
            transmission=request.form["transmission"],
            exterior=request.form["exterior"],
            interior=request.form["interior"],
            description=request.form["description"],
            images=list(images),
        )
        flash("Vehicle has been updated")
        return redirect(url_for("vehicles.admin_vehicles_edit", id=vehicle["id"]))
    except vehicle_model.ErrNotFound:
        images = uploaded_images or None
        vehicle_model.insert(
            make=request.form["make"],
            model=request.form["model"],
            year=request.form["year"],
            trim=request.form["trim"],
            engine=request.form["engine"],
            title=request.form["title"],
            condition=request.form["condition"],
            drive=request.form["drive"],
            fuel=request.form["fuel"],
            transmission=request.form["transmission"],
            exterior=request.form["exterior"],
            interior=request.form["interior"],
            description=request.form["description"],
            images=images,
        )
        flash("Vehicle has been created")
        return redirect(url_for("vehicles.admin_vehicles_add"))


@bp.route("/admin/vehicles/add")
@login_required
def admin_vehicles_add():
    return render_template(
        "admin/vehicles/upsert.html", mode="add", active_nav="vehicle"
    )


@bp.route("/admin/vehicles/<id>/images/remove", methods=["POST"])
@login_required
def admin_vehicles_images_remove(id):
    try:
        # remove images from disk if any
        rm_image = request.form.get("image")
        util.remove_files([rm_image], app.config["IMAGES_DIR_PATH"])

        vehicle = vehicle_model.get(id=id)
        # get current set of images and update it
        vehicle["images"].remove(rm_image)

        vehicle_model.update(id=vehicle["id"], images=vehicle["images"])
        flash("Removed image")
        return redirect(url_for("vehicle.admin_vehicles_edit", id=vehicle["id"]))
    except vehicle_model.ErrNotFound:
        abort(404)


@bp.route("/admin/vehicles/<id>/edit")
@login_required
def admin_vehicles_edit(id: str):
    try:
        vehicle = vehicle_model.get(id=id)
        return render_template(
            "admin/vehicles/upsert.html",
            vehicle=vehicle,
            mode="edit",
            active_nav="vehicle",
        )
    except vehicle_model.ErrNotFound:
        abort(404)


@bp.route("/admin/vehicles/<id>/delete", methods=["POST"])
@login_required
def admin_vehicles_delete(id):
    vehicle = vehicle_model.get(id)
    # Remove image of this vehicle on disk
    util.remove_files(vehicle["images"], app.config["IMAGES_DIR_PATH"])
    vehicle_model.delete(id)
    flash("Vehicle has been deleted")
    return redirect(url_for("vehicles.admin_vehicles_management"))
