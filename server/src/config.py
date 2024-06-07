import os

from dotenv.main import load_dotenv, dotenv_values

# Get the directory of the current file (config.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(base_dir, ".env")
# Load environment variables from the .env file
load_dotenv(env_path)

config = {
    **dotenv_values(env_path),
    **os.environ,  # override loaded values with environment variables
}

try:
    GOOGLE_CSE_ID = "e74ae2f61bea249ef"
    GOOGLE_API_KEY = "AIzaSyDYgOOODO_MHGrV28sIRPdrQ9GIaZlX4dU"
    TESSERACT_EXECUTABLE_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    LOG_LEVEL = "INFO"
    LOG_PATH = os.path.join(base_dir, "logs")
    TEMP_FOLDER_PATH = r"D:\Coding\internship\image_scrapper\temp"
    SQLALCHEMY_DATABASE_URL = r"sqlite:///D:\Coding\internship\image_scrapper\server\src\tasks.db"
    CELERY_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER = 'redis://localhost:6379/0'
except Exception as e:
    print("Exception in loading variables", e)
    raise
