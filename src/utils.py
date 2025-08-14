import os, json, hashlib, logging, re

# Logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "fact_checker.log"),
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_info(msg): print(f"[INFO] {msg}"); logging.info(msg)
def log_debug(msg): print(f"[DEBUG] {msg}"); logging.debug(msg)
def log_error(msg): print(f"[ERROR] {msg}"); logging.error(msg)

# Text cleaning
def clean_text(text): return re.sub(r"\s+", " ", re.sub(r"[^\w\s.,!?]", "", text)).strip()

# Caching
CACHE_DIR = "data/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_key(query): return hashlib.md5(query.encode("utf-8")).hexdigest()
def load_cache(query):
    path = os.path.join(CACHE_DIR, f"{get_cache_key(query)}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    return None
def save_cache(query, data):
    path = os.path.join(CACHE_DIR, f"{get_cache_key(query)}.json")
    with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

# Format output
def format_fact_check_result(claim, answer):
    return f"\n==========================\nClaim: {claim}\nFact-Check Result:\n{answer}\n==========================\n"


































# import os
# import json
# import hashlib
# import logging
# from datetime import datetime
# import re

# # -----------------------------
# # Logging Setup
# # -----------------------------
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
# logging.basicConfig(
#     filename=os.path.join(LOG_DIR, "fact_checker.log"),
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )

# def log_info(message: str):
#     print(f"[INFO] {message}")
#     logging.info(message)

# def log_debug(message: str):
#     print(f"[DEBUG] {message}")
#     logging.debug(message)

# def log_error(message: str):
#     print(f"[ERROR] {message}")
#     logging.error(message)

# # -----------------------------
# # Text Cleaning
# # -----------------------------
# def clean_text(text: str) -> str:
#     """Remove extra spaces, newlines, and unwanted characters."""
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"[^\w\s.,!?]", "", text)
#     return text.strip()

# # -----------------------------
# # Caching
# # -----------------------------
# CACHE_DIR = "data/cache"
# os.makedirs(CACHE_DIR, exist_ok=True)

# def get_cache_key(query: str) -> str:
#     """Generate a unique hash for a query string."""
#     return hashlib.md5(query.encode("utf-8")).hexdigest()

# def load_cache(query: str):
#     """Load cached response if exists."""
#     key = get_cache_key(query)
#     path = os.path.join(CACHE_DIR, f"{key}.json")
#     if os.path.exists(path):
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     return None

# def save_cache(query: str, data):
#     """Save response to cache."""
#     key = get_cache_key(query)
#     path = os.path.join(CACHE_DIR, f"{key}.json")
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)

# # -----------------------------
# # Output Formatting
# # -----------------------------
# def format_fact_check_result(claim: str, final_answer: str) -> str:
#     return f"""
# ==========================
# Claim: {claim}
# --------------------------
# Fact-Check Result:
# {final_answer}
# ==========================
# """
