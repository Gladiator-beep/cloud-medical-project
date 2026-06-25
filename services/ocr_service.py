import os
import requests
from werkzeug.utils import secure_filename
from config import Config

UPLOAD_FOLDER = "uploaded_prescriptions"

HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/PaddlePaddle/PaddleOCR-VL"


def save_prescription_image(file):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    return file_path


def extract_text_from_prescription(file_path):
    """
    OCR service using Hugging Face PaddleOCR-VL.
    If the cloud model is unavailable, the system falls back to Demo Mode.
    """

    if not Config.HUGGINGFACE_API_TOKEN:
        return """
Hugging Face token missing.

Demo OCR Result:
Medication: Acamol
Dosage: 500mg
Instructions: Take one tablet up to three times a day after meals.
"""

    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"
    }

    try:
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = requests.post(
            HF_MODEL_URL,
            headers=headers,
            data=image_bytes,
            timeout=60
        )

        if response.status_code != 200:
            return f"""
Hugging Face OCR request failed.
Status code: {response.status_code}
Response: {response.text}

Demo OCR Result:
Medication: Acamol
Dosage: 500mg
Instructions: Take one tablet up to three times a day after meals.
"""

        result = response.json()

        return f"""
Hugging Face PaddleOCR-VL Result:

{result}
"""

    except Exception as e:
        return f"""
OCR Error: {e}

Demo OCR Result:
Medication: Acamol
Dosage: 500mg
Instructions: Take one tablet up to three times a day after meals.
"""