from dotenv import load_dotenv

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('./flightservice/public.env')

load_dotenv(dotenv_path=env_path)