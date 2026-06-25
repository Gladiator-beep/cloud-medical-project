from flask import Flask, send_from_directory
from config import Config
from models.models import db

from routes.home_routes import home_bp
from routes.admin_routes import admin_bp
from routes.doctor_routes import doctor_bp
from routes.pharmacist_routes import pharmacist_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(pharmacist_bp)

@app.route("/generated_pdfs/<path:filename>")
def generated_pdf(filename):
    return send_from_directory("generated_pdfs", filename)

with app.app_context():
    db.create_all()

import os

if __name__ == "__main__":
    print("Starting Flask server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)