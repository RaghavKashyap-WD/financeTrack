import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = "root"
DB_PASS = "computer"
DB_HOST = "localhost"
DB_NAME = "finTrack"
DB_PORT = "3306"

REQUIRED = {"DB_USER": DB_USER, "DB_PASS": DB_PASS, "DB_NAME": DB_NAME}
missing = [k for k,v in REQUIRED.items() if not v]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
