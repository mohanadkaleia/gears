from flask import render_template, request, Blueprint, flash, redirect, abort, url_for
from flask_login import login_required

from app import app, util
import app.models.services as services_model


bp = Blueprint("service", __name__)


@bp.route("/admin/services")
@login_required
def admin_services_management():
    services = services_model.all()
    return render_template("admin/services/index.html", services=services)


@bp.route("/admin/services/save", methods=["POST"])
@login_required
def admin_services_save():
    uploaded_images = None
    if request.files.getlist("images"):
        uploaded_images = util.upload_files(
            request.files.getlist("images"), app.config["IMAGES_DIR_PATH"]
        )
    # price info are separated into names and values (prices)
    # e.g [Wash & Vacuum, Carpet Shampoo], [40, 50]
    # since this is list so the order are name - value will be matched
    # to update the price, I combine those list in to a dict with key = name, value = value
    # zip(names[], values[]) will resolve the above into [(Wash & Vacuum, 40), (Carpet Shampoo, 50)]
    # finally convert prices into dict => final = {Wash & Vacuum: 40, Carpet Shampoo: 50}
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
        images |= set(uploaded_images)

        services_model.update(
            id=service["id"],
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=list(images),
        )
        flash("Service has been updated")
        return redirect(url_for("service.admin_services_edit", id=service["id"]))
    except services_model.ErrNotFound:
        images = uploaded_images or None
        services_model.insert(
            name=request.form["name"],
            price=price,
            description=request.form["description"],
            images=images,
        )
        flash("Service has been created")
        return redirect(url_for("service.admin_services_add"))


@bp.route("/admin/services/add")
@login_required
def admin_services_add():
    return render_template("admin/services/upsert.html", mode="add")


@bp.route("/admin/services/<id>/images/remove", methods=["POST"])
@login_required
def admin_services_images_remove(id):
    try:
        # remove images from disk if any
        rm_image = request.form.get("image")
        util.remove_files([rm_image], app.config["IMAGES_DIR_PATH"])

        service = services_model.get(id=id)
        # get current set of images and update it
        service["images"].remove(rm_image)

        services_model.update(id=service["id"], images=service["images"])
        flash("Removed image")
        return redirect(url_for("service.admin_services_edit", id=service["id"]))
    except services_model.ErrNotFound:
        abort(404)


@bp.route("/admin/services/<id>/edit")
@login_required
def admin_services_edit(id: str):
    try:
        service = services_model.get(id=id)
        return render_template(
            "admin/services/upsert.html", service=service, mode="edit"
        )
    except services_model.ErrNotFound:
        abort(404)


@bp.route("/admin/services/<id>/delete", methods=["POST"])
@login_required
def admin_services_delete(id):
    service = services_model.get(id)
    # Remove image of this service on disk
    util.remove_files(service["images"], app.config["IMAGES_DIR_PATH"])
    services_model.delete(id)
    flash("Service has been deleted")
    return redirect(url_for("service.admin_services_management"))
