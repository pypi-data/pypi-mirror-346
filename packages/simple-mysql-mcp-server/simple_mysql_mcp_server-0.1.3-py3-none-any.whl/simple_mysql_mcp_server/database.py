import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load config
with open("config.json") as f:
    config = json.load(f)

DATABASE_URL = (
    f"mysql+pymysql://{config['username']}:{config['password']}"
    f"@{config['host']}:{config['port']}/{config['database']}"
)
print("✅{DATABASE_URL}.\n")
# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
