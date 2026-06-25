import cloudinary
import cloudinary.uploader

from config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True
)


def upload_pdf(local_path):
    try:
        result = cloudinary.uploader.upload(
            local_path,
            resource_type="raw",
            folder="medical_prescriptions"
        )

        return result["secure_url"]

    except Exception as e:
        print(e)
        return None