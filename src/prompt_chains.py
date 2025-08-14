import os
import yaml
from google import generativeai as genai
from src import utils
import os
from dotenv import load_dotenv

load_dotenv()
# Load API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
genai.configure(api_key=api_key)

class GeminiLLM:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        utils.log_info(f"Gemini LLM initialized with model: {model_name}")

    def predict(self, prompt: str) -> str:
        utils.log_debug(f"Sending prompt to Gemini:\n{prompt}")
        response = self.model.generate_content(contents=prompt)
        utils.log_debug("Received response from Gemini.")
        return response.text

class FactCheckChain:
    def __init__(self, llm=None, prompts_file="config/prompts.yaml"):
        self.llm = llm or GeminiLLM()
        with open(prompts_file, "r") as f:
            self.prompts = yaml.safe_load(f)
        utils.log_info("FactCheckChain initialized with prompts.")

    def initial_response(self, claim: str) -> str:
        template = self.prompts["initial_response"]["template"]
        prompt = template.format(claim=claim)
        return self.llm.predict(prompt)

    def extract_assumptions(self, initial_response: str) -> list:
        template = self.prompts["assumption_extraction"]["template"]
        prompt = template.format(initial_response=initial_response)
        assumptions_text = self.llm.predict(prompt)
        assumptions = [a.strip() for a in assumptions_text.split("\n") if a.strip()]
        utils.log_debug(f"Extracted assumptions: {assumptions}")
        return assumptions

    def final_synthesis(self, evidence_summary: str) -> str:
        template = self.prompts["final_synthesis"]["template"]
        prompt = template.format(evidence_summary=evidence_summary)
        return self.llm.predict(prompt)



































# # src/prompt_chains.py

# import os
# import yaml
# from dotenv import load_dotenv
# from langchain_tavily import TavilySearch
# from google import generativeai as genai

# # -----------------------------
# # Load environment variables
# # -----------------------------
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set in your environment variables.")
# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY is not set in your environment variables.")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# # -----------------------------
# # Load prompts
# # -----------------------------
# with open("config/prompts.yaml", "r") as f:
#     PROMPTS = yaml.safe_load(f)

# # -----------------------------
# # Gemini LLM Wrapper
# # -----------------------------
# class GeminiLLM:
#     def __init__(self, model_name="gemini-2.5-flash"):
#         self.model = genai.GenerativeModel(model_name)

#     def predict(self, prompt: str) -> str:
#         print(f"[DEBUG] Sending prompt to Gemini:\n{prompt}\n")
#         response = self.model.generate_content(contents=prompt)
#         print(f"[DEBUG] Received response from Gemini.\n")
#         return response.text

# # -----------------------------
# # Prompt Chain
# # -----------------------------
# class FactCheckChain:
#     def __init__(self, llm=None, search_tool=None):
#         self.llm = llm or GeminiLLM()
#         self.search_tool = search_tool or TavilySearch(api_key=TAVILY_API_KEY)
#         print("[DEBUG] FactCheckChain initialized.")

#     def initial_response(self, claim: str) -> str:
#         template = PROMPTS["initial_response"]["template"]
#         prompt = template.format(claim=claim)
#         response = self.llm.predict(prompt)
#         print(f"[DEBUG] Initial response:\n{response}\n")
#         return response

#     def extract_assumptions(self, initial_response: str) -> list:
#         template = PROMPTS["assumption_extraction"]["template"]
#         prompt = template.format(initial_response=initial_response)
#         assumptions_text = self.llm.predict(prompt)
#         assumptions = [a.strip() for a in assumptions_text.split("\n") if a.strip()]
#         print(f"[DEBUG] Extracted assumptions: {assumptions}\n")
#         return assumptions

#     def verify_assumptions(self, assumptions: list) -> str:
#         evidence_summary = []
#         for a in assumptions:
#             print(f"[DEBUG] Searching evidence for assumption: {a}")
#             search_results = self.search_tool.run(a)
#             evidence_summary.append(f"Assumption: {a}\nEvidence: {search_results}\n")
#             print(f"[DEBUG] Evidence found: {search_results}\n")
#         return "\n".join(evidence_summary)

#     def final_synthesis(self, evidence_summary: str) -> str:
#         template = PROMPTS["final_synthesis"]["template"]
#         prompt = template.format(evidence_summary=evidence_summary)
#         final_answer = self.llm.predict(prompt)
#         print(f"[DEBUG] Final synthesis result:\n{final_answer}\n")
#         return final_answer

#     def run_chain(self, claim: str) -> str:
#         print(f"[DEBUG] Running fact check chain for claim: {claim}\n")
#         init_resp = self.initial_response(claim)
#         assumptions = self.extract_assumptions(init_resp)
#         evidence_summary = self.verify_assumptions(assumptions)
#         final_answer = self.final_synthesis(evidence_summary)
#         return final_answer

# # -----------------------------
# # Example Usage
# # -----------------------------
# if __name__ == "__main__":
#     claim = "The capital of France is Paris."
#     chain = FactCheckChain()
#     result = chain.run_chain(claim)
#     print("Final Fact-Check Result:\n", result)



# import os
# from dotenv import load_dotenv  # import dotenv
# import yaml
# from google import generativeai as genai
# from src import utils

# # -----------------------------
# # Load environment variables
# # -----------------------------
# load_dotenv()  # loads variables from .env file into os.environ

# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# # -----------------------------
# # Gemini LLM
# # -----------------------------
# class GeminiLLM:
#     def __init__(self, model_name="gemini-2.5-flash"):
#         self.model = genai.GenerativeModel(model_name)
#         utils.log_info(f"Gemini LLM initialized with model: {model_name}")

#     def predict(self, prompt: str) -> str:
#         utils.log_debug(f"Sending prompt to Gemini:\n{prompt}")
#         response = self.model.generate_content(contents=prompt)
#         utils.log_debug("Received response from Gemini.")
#         return response.text

# # -----------------------------
# # FactCheckChain
# # -----------------------------
# class FactCheckChain:
#     def __init__(self, llm=None, prompts_file="config/prompts.yaml"):
#         self.llm = llm or GeminiLLM()
#         with open(prompts_file, "r") as f:
#             self.prompts = yaml.safe_load(f)
#         utils.log_info("FactCheckChain initialized with prompts.")

#     def initial_response(self, claim: str) -> str:
#         template = self.prompts["initial_response"]["template"]
#         prompt = template.format(claim=claim)
#         return self.llm.predict(prompt)

#     def extract_assumptions(self, initial_response: str) -> list:
#         template = self.prompts["assumption_extraction"]["template"]
#         prompt = template.format(initial_response=initial_response)
#         assumptions_text = self.llm.predict(prompt)
#         assumptions = [a.strip() for a in assumptions_text.split("\n") if a.strip()]
#         utils.log_debug(f"Extracted assumptions: {assumptions}")
#         return assumptions

#     def final_synthesis(self, evidence_summary: str) -> str:
#         template = self.prompts["final_synthesis"]["template"]
#         prompt = template.format(evidence_summary=evidence_summary)
#         return self.llm.predict(prompt)
