from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    national_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20))

    birth_date = db.Column(db.Date)
    pregnant = db.Column(db.Boolean, default=False)
    breastfeeding = db.Column(db.Boolean, default=False)

    image_url = db.Column(db.String(300))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))

    def age(self):
        if not self.birth_date:
            return None

        today = date.today()

        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)

    doctor_name = db.Column(db.String(100), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)

    pdf_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default="open")

    patient = db.relationship("Patient", backref="visits")