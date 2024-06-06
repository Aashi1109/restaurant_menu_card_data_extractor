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
