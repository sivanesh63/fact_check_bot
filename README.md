

# 🕵️‍♂️ AI Fact-Checker

A modular, LLM-powered fact-checking bot that takes a claim, verifies it using online sources, and returns a synthesized, evidence-based answer.

---

## 📂 Project Structure

project-root/
├── config/
│ ├── settings.py # Centralized configuration
│ └── prompts.yaml # Prompt templates & examples
├── src/
│ ├── fact_checker.py # Core fact-checking pipeline
│ ├── prompt_chains.py # LLM prompt chaining logic
│ ├── search_tools.py # Evidence retrieval & web search
│ ├── utils.py # Logging, cleaning, caching, helpers
│ └── ui/
│ ├── cli.py # Command-line interface
│ ├── streamlit_app.py
│ └── gradio_app.py
├── tests/
│ ├── test_fact_checker.py
│ └── test_search_tools.py
├── examples/
│ ├── example_queries.txt
│ └── demo_notebook.ipynb
├── data/ # Optional: cached evidence / embeddings
├── requirements.txt
├── .env.example
└── README.md



## 🚀 Setup & Installation

### **1. Project Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/fact-checker.git
cd fact-checker

# Create a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # Linux/Mac
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Environment Variables
Copy .env.example to .env

Add API keys for:

OpenAI

DuckDuckGo / NewsAPI / SerpAPI

Any other services you integrate

Example:

env
Copy
Edit
OPENAI_API_KEY=your_key_here
NEWS_API_KEY=your_key_here

⚙️ Configuration
All configurable parameters are stored in:

config/settings.py → API keys, model parameters, search settings

config/prompts.yaml → Prompt templates, few-shot examples

This ensures all modules read from a single source of truth.

🧠 Core Workflow
Main process (in src/fact_checker.py):

Accepts a claim

Generates an initial LLM response

Extracts assumptions

Retrieves evidence from the web

Synthesizes a final, evidence-backed answer

🔗 Prompt Chaining
src/prompt_chains.py defines the sequence:

Initial Response

Assumption Extraction

Verification

Evidence Synthesis

Final Answer

Prompts are loaded from config/prompts.yaml.

🌐 Evidence Retrieval
src/search_tools.py handles:

DuckDuckGo Search API

NewsAPI / SerpAPI integration

Error handling & rate-limiting

Returning top snippets and URLs

🛠 Utilities
src/utils.py provides:

Logging helpers

Text cleaning functions

Query caching

Output formatting

🖥 User Interfaces
CLI (src/ui/cli.py) – Quick local testing

Streamlit (src/ui/streamlit_app.py) – Interactive web app

Gradio (src/ui/gradio_app.py) – Lightweight demo interface

✅ Testing
Run with pytest or unittest:

bash
Copy
Edit
pytest tests/
📊 Examples & Demo
examples/example_queries.txt – Sample claims

examples/demo_notebook.ipynb – Interactive notebook demo

💾 Optional: Database / Knowledge Storage
data/knowledge_base.db – Store verified claims & evidence

data/embeddings/ – Store semantic search vectors for fast lookup

🔄 Recommended Development Flow
Setup project structure & virtual environment

Add configuration files & API keys

Implement core logic (fact_checker.py)

Add prompt chaining (prompt_chains.py)

Integrate web search (search_tools.py)

Create utility functions (utils.py)

Build CLI interface

Add Streamlit / Gradio UI

Write unit tests & run examples

Optionally, add caching & vector embeddings