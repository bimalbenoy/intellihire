from dotenv import load_dotenv
import os
import cloudinary

load_dotenv()  # loads variables from .env into environment

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)
