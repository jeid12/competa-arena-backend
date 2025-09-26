import cloudinary.uploader

def upload_profile_photo(file, public_id=None):
    result = cloudinary.uploader.upload(
        file,
        folder="competa_arena/profiles",
        public_id=public_id,  # e.g. f"user_{user_id}"
        overwrite=True,
        resource_type="image",
        transformation=[{"width": 300, "height": 300, "crop": "fill"}]  # optional: resize
    )
    return result["secure_url"]