from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from models.models import db, Patient

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/patients", methods=["GET", "POST"])
def patients():
    if request.method == "POST":
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()

        patient = Patient(
            national_id=request.form["national_id"],
            full_name=request.form["full_name"],
            gender=request.form["gender"],
            birth_date=birth_date,
            pregnant=True if request.form.get("pregnant") == "on" else False,
            breastfeeding=True if request.form.get("breastfeeding") == "on" else False,
            image_url=request.form["image_url"],
            email=request.form["email"],
            phone=request.form["phone"]
        )

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("admin.patients"))

    patients_list = Patient.query.all()
    return render_template("admin_patients.html", patients=patients_list)