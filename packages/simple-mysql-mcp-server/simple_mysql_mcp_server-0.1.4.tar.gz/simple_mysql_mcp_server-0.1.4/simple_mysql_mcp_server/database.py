import json
import sqlalchemy

def get_engine():
    with open("config.json") as f:
        config = json.load(f)

    url = f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    return sqlalchemy.create_engine(url)
