from flask import Blueprint, render_template
from models.models import Patient, Visit

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    total_patients = Patient.query.count()
    total_visits = Visit.query.count()
    open_prescriptions = Visit.query.filter_by(status="open").count()
    dispensed_prescriptions = Visit.query.filter_by(status="dispensed").count()

    return render_template(
        "index.html",
        total_patients=total_patients,
        total_visits=total_visits,
        open_prescriptions=open_prescriptions,
        dispensed_prescriptions=dispensed_prescriptions
    )