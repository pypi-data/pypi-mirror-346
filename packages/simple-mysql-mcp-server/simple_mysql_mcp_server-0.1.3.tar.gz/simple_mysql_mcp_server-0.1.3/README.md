# Simple MySQL MCP Server

A minimal FastAPI-based MCP server that lets GitHub Copilot or other MCP-compatible tools securely query your local or Dockerized MySQL database.

---

## ⚡ Features

- 🔌 Connects to any MySQL instance (XAMPP, Docker, Linux-native, etc.)
- 🚀 Fast and lightweight (built with FastAPI)
- 🛡️ Auto-blocks destructive SQL (`DROP`, `DELETE`, etc.)
- 📊 Logs queries with timing
- 🧩 MCP.so-compatible (`mcp.json` included)

---

## 🛠 Installation (Python)

```bash
git clone https://github.com/your-username/simple-mysql-mcp-server.git
cd simple-mysql-mcp-server
cp config.sample.json config.json
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8081
