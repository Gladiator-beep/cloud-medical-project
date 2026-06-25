from flask import Blueprint, render_template, request, redirect, url_for
from models.models import db, Patient, Visit
from services.ocr_service import save_prescription_image, extract_text_from_prescription
from services.clinical_trials_service import search_clinical_trials
from services.side_effects_service import search_side_effects
pharmacist_bp = Blueprint("pharmacist", __name__, url_prefix="/pharmacist")

@pharmacist_bp.route("/", methods=["GET", "POST"])
def pharmacist_home():
    patient = None
    visits = []
    message = None
    ocr_text = None
    uploaded_file_path = None
    clinical_trials = None
    side_effects = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "search_patient":
            national_id = request.form["national_id"]
            patient = Patient.query.filter_by(national_id=national_id).first()

            if patient:
                visits = Visit.query.filter_by(patient_id=patient.id).all()
            else:
                message = "Patient not found"

        elif action == "dispense":
            visit_id = request.form["visit_id"]
            visit = Visit.query.get(visit_id)

            if visit:
                visit.status = "dispensed"
                db.session.commit()
                message = "Prescription was dispensed successfully"
                patient = visit.patient
                visits = Visit.query.filter_by(patient_id=patient.id).all()

        elif action == "ocr":
            file = request.files.get("prescription_image")

            if file and file.filename:
                uploaded_file_path = save_prescription_image(file)
                ocr_text = extract_text_from_prescription(uploaded_file_path)
                message = "Prescription image was uploaded and processed successfully"

            else:
                message = "No image file was uploaded"
        elif action == "clinical_trials":
            drug_name = request.form["drug_name"]
            clinical_trials = search_clinical_trials(drug_name)
            message = f"Clinical trials search completed for {drug_name}"
        elif action == "side_effects":
            drug_name = request.form["side_effect_drug"]
            side_effects = search_side_effects(drug_name)
            message = f"Side effects search completed for {drug_name}"

    return render_template(
        "pharmacist.html",
        patient=patient,
        visits=visits,
        message=message,
        ocr_text=ocr_text,
        uploaded_file_path=uploaded_file_path,
        clinical_trials=clinical_trials,
        side_effects=side_effects
    )