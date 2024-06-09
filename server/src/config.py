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
    DB_FILE_PATH = os.path.join(base_dir, "sqlite.db")
    LOG_PATH = os.path.join(base_dir, "logs")

    GOOGLE_CSE_ID = config.get('GOOGLE_CSE_ID')
    GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")
    TESSERACT_EXECUTABLE_PATH = config.get("TESSERACT_EXECUTABLE_PATH")
    LOG_LEVEL = config.get("LOG_LEVEL") or "INFO"
    TEMP_FOLDER_PATH = config.get("TEMP_FOLDER_PATH")
    SQLALCHEMY_DATABASE_URL = fr"sqlite:///{DB_FILE_PATH}"
    CELERY_BACKEND = config.get("CELERY_BACKEND") or 'redis://localhost:6379/0'
    CELERY_BROKER = config.get("CELERY_BROKER") or 'redis://localhost:6379/0'
    PORT = int(config.get("PORT") or 5000)
    HOST = config.get("HOST")
except Exception as e:
    logger.error("Exception in loading variables", e)
    raise
