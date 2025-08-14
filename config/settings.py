import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -------------------------------
# API Keys
# -------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# -------------------------------
# LangChain / LLM Settings
# -------------------------------
LLM_MODEL = "gemini-2.5-flash"   # You can switch to other models like gpt-4, Claude, etc.
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# -------------------------------
# Search Settings
# -------------------------------
SEARCH_ENGINE = "tavily"   # Options: tavily, duckduckgo, newsapi
MAX_SEARCH_RESULTS = 5
SEARCH_DEPTH = "basic"     # Options: basic, advanced

# -------------------------------
# Other Settings
# -------------------------------
CACHE_ENABLED = True        # Enable caching of repeated queries
CACHE_DIR = "data/cache"    # Directory to store cached responses
