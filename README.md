# 🤖 Agentic AI Orchestrator

A multi-agent system built with **Streamlit** and **aisuite**. It features an intelligent router that directs queries to specialized agents for SQL analysis, weather data, and general knowledge.

## 🛠️ Features
- **Smart Routing**: Categorizes questions into SQL, Weather, or General topics.
- **SQL Agent**: Automatically generates and reviews SQL queries against a sales database.
- **Weather Agent**: Fetches real-time weather using the OpenWeatherMap API.
- **Modern UI**: Streamlit interface with custom CSS and theme selection.

## ⚙️ Setup
1. Clone the repo: `git clone https://github.com/DeepBhattarai/Agentic_AI.git`
2. Create venv and install: `pip install -r requirements.txt`
3. Add API keys to `.streamlit/secrets.toml`.
4. Run: `streamlit run Agentic_AI_main.py`
