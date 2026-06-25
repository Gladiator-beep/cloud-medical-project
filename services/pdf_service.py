from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

def create_prescription_pdf(patient, doctor_name, diagnosis, medication, dosage, instructions):
    os.makedirs("generated_pdfs", exist_ok=True)

    filename = f"prescription_{patient.national_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join("generated_pdfs", filename)

    c = canvas.Canvas(file_path, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "Medical Prescription")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Patient Name: {patient.full_name}")
    c.drawString(50, 740, f"National ID: {patient.national_id}")
    c.drawString(50, 720, f"Age: {patient.age()}")
    c.drawString(50, 700, f"Gender: {patient.gender}")

    c.drawString(50, 660, f"Doctor Name: {doctor_name}")
    c.drawString(50, 640, f"Diagnosis: {diagnosis}")
    c.drawString(50, 620, f"Medication: {medication}")
    c.drawString(50, 600, f"Dosage: {dosage}")
    c.drawString(50, 580, f"Instructions: {instructions}")

    c.drawString(50, 540, f"Created At: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 500, "Doctor Signature: __________________")

    c.save()

    return file_path