from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlalchemy
import time
from datetime import datetime
import os
import json
import logging

# Step 1: Logging setup
os.makedirs("logs", exist_ok=True)
log_file = "logs/query.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Step 2: Only generate config.json if running manually
def ensure_config():
    if not os.path.exists("config.json"):
        import getpass
        print("[config] No config.json found. Let's create one.")
        cfg = {
            "host": input("MySQL host [localhost]: ") or "localhost",
            "port": int(input("MySQL port [3306]: ") or "3306"),
            "username": input("MySQL username [root]: ") or "root",
            "password": getpass.getpass("MySQL password: "),
            "database": input("MySQL database: ")
        }
        with open("config.json", "w") as f:
            json.dump(cfg, f, indent=2)
        print("[config] config.json created successfully.\n")

# Step 3: Load database engine (assumes config.json already exists)
from simple_mysql_mcp_server.database import engine

# Step 4: FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    sql: str
    params: dict = None

@app.post("/query")
async def run_query(request: QueryRequest):
    DANGEROUS_KEYWORDS = ["DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "RENAME", "CREATE"]
    sql_upper = request.sql.upper().strip()
    if any(keyword in sql_upper for keyword in DANGEROUS_KEYWORDS):
        logging.warning(f"BLOCKED: Dangerous query attempted → {request.sql}")
        return {
            "status": "blocked",
            "message": "This query contains restricted keywords and was blocked for safety."
        }

    try:
        start = time.time()
        with engine.connect() as conn:
            stmt = sqlalchemy.text(request.sql).bindparams(**(request.params or {}))
            result = conn.execute(stmt)
            rows = [dict(zip(result.keys(), row)) for row in result]
        duration = round((time.time() - start) * 1000, 2)
        logging.info(f"SQL: {request.sql} | Duration: {duration}ms")
        return {
            "status": "success",
            "execution_time_ms": duration,
            "data": rows
        }
    except Exception as e:
        logging.error(f"ERROR: {request.sql} → {e}")
        return {"status": "error", "message": str(e)}

# Step 5: Entrypoint — safe for both CLI and MCP
def main():
    # Only prompt for config in manual CLI mode
    if os.environ.get("MCP_MODE") != "1":
        ensure_config()

    import uvicorn
    uvicorn.run("simple_mysql_mcp_server.main:app", host="0.0.0.0", port=8081)

if __name__ == "__main__":
    main()
