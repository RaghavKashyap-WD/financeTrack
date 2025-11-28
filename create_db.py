# create_db.py

from db import Base, engine
from models import *

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
