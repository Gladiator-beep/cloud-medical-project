from flask import Blueprint, render_template, request
from models.models import db, Patient, Visit
from services.pdf_service import create_prescription_pdf
from services.storage_service import upload_pdf
from services.search_service import search_diagnosis_info

doctor_bp = Blueprint("doctor", __name__, url_prefix="/doctor")

@doctor_bp.route("/visit", methods=["GET", "POST"])
def visit():
    message = None
    patient = None
    pdf_path = None
    search_results = None

    if request.method == "POST":
        national_id = request.form["national_id"]
        patient = Patient.query.filter_by(national_id=national_id).first()

        if not patient:
            message = "Patient not found"
            return render_template(
                "doctor_visit.html",
                message=message,
                patient=None,
                pdf_path=None,
                search_results=None
            )

        doctor_name = request.form["doctor_name"]
        diagnosis = request.form["diagnosis"]
        medication = request.form["medication"]
        dosage = request.form["dosage"]
        instructions = request.form["instructions"]

        local_pdf_path = create_prescription_pdf(
            patient,
            doctor_name,
            diagnosis,
            medication,
            dosage,
            instructions
        )

        # Upload to Cloudinary for cloud storage requirement
        cloud_pdf = upload_pdf(local_pdf_path)

        # Local URL for opening the PDF in the app
        local_pdf_url = "/" + local_pdf_path.replace("\\", "/")

        visit = Visit(
            patient_id=patient.id,
            doctor_name=doctor_name,
            diagnosis=diagnosis,
            medication=medication,
            dosage=dosage,
            instructions=instructions,
            pdf_url=local_pdf_url,
            status="open"
        )

        db.session.add(visit)
        db.session.commit()

        message = "Visit, prescription and PDF were created successfully"
        search_results = search_diagnosis_info(diagnosis)

        # The button will open local PDF route, not Cloudinary raw URL
        pdf_path = local_pdf_url

    return render_template(
        "doctor_visit.html",
        message=message,
        patient=patient,
        pdf_path=pdf_path,
        search_results=search_results
    )