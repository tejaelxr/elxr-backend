import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path to the config file
# TODO: move tese config.ini and DigiCertGlobalRootCA.crt.pem to deploy folder
config_file_path = os.path.join(current_dir, 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_file_path)

# Get the database URL
url = config.get('DB_URL', 'DATABASE_URL')
if os.environ.get("DATABASE_URL"):
    url = os.environ.get("DATABASE_URL")

use_ssl = config.get('DB_URL', 'USE_SSL')

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
