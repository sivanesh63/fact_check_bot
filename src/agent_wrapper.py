# from langchain.llms.base import LLM
# from langchain.tools import BaseTool
# from langchain.agents import initialize_agent, AgentType
# from typing import Optional, List
# from prompt_chains import GeminiLLM
# from search_tools import EvidenceSearch

# # LLM Wrapper
# class LangChainGemini(LLM):
#     def __init__(self): self.gemini = GeminiLLM()
#     @property
#     def _llm_type(self): return "gemini"
#     def _call(self, prompt: str, stop: Optional[List[str]] = None): return self.gemini.predict(prompt)

# # Tool
# class EvidenceTool(BaseTool):
#     name = "EvidenceSearch"
#     description = "Use this to get evidence for a claim or assumption."
#     def __init__(self, searcher: EvidenceSearch): self.searcher = searcher
#     def _run(self, query: str): return self.searcher.gather_evidence([query])
#     async def _arun(self, query: str): raise NotImplementedError()

# # Agent
# def get_agent():
#     llm = LangChainGemini()
#     tool = EvidenceTool(EvidenceSearch(tavily_api_key=os.getenv("TAVILY_API_KEY")))
#     return initialize_agent([tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)






import os
from typing import List, Optional
from pydantic import PrivateAttr
from langchain.llms.base import LLM
from src.prompt_chains import GeminiLLM
from src.search_tools import EvidenceSearch


# LLM Wrapper
class LangChainGemini(LLM):
    _gemini: GeminiLLM = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._gemini = GeminiLLM()

    @property
    def _llm_type(self):
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None):
        return self._gemini.predict(prompt)


# Evidence Tool Wrapper
class EvidenceTool:
    """Simple wrapper around EvidenceSearch."""
    def __init__(self, tavily_api_key: str):
        self._searcher = EvidenceSearch(tavily_api_key=tavily_api_key)

    def run(self, query: str):
        return self._searcher.gather_evidence([query])


# Custom Fact-Checking Pipeline
class FactChecker:
    def __init__(self, tavily_api_key: str):
        self.llm = LangChainGemini()
        self.tool = EvidenceTool(tavily_api_key)

    def check_claim(self, claim: str) -> str:
        # Extract assumptions
        assumptions_prompt = f"Extract assumptions from the claim: {claim}"
        assumptions_text = self.llm._call(assumptions_prompt)
        assumptions = [a.strip() for a in assumptions_text.split("\n") if a.strip()]

        # Gather evidence
        evidence_summary = []
        for a in assumptions:
            evidence = self.tool.run(a)
            evidence_summary.append(f"Assumption: {a}\nEvidence: {evidence}\n")

        # Final synthesis
        synthesis_prompt = (
            f"Claim: {claim}\n"
            f"Evidence Summary:\n{''.join(evidence_summary)}\n"
            f"Provide a single final verdict (True/False) and a concise explanation."
        )
        final_answer = self.llm._call(synthesis_prompt)
        return final_answer


# Factory function for Streamlit
def get_agent():
    return FactChecker(tavily_api_key=os.getenv("TAVILY_API_KEY"))





















































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
# print("[DEBUG] Gemini API configured successfully.")

# # -----------------------------
# # Load prompts
# # -----------------------------
# with open("config/prompts.yaml", "r") as f:
#     PROMPTS = yaml.safe_load(f)
# print("[DEBUG] Prompts loaded:", PROMPTS.keys())

# # -----------------------------
# # Gemini LLM Wrapper
# # -----------------------------
# class GeminiLLM:
#     def __init__(self, model_name="gemini-2.5-flash"):
#         self.model = genai.GenerativeModel(model_name)
#         print(f"[DEBUG] Gemini LLM initialized with model: {model_name}")

#     def predict(self, prompt: str) -> str:
#         print(f"[DEBUG] Sending prompt to Gemini:\n{prompt}")
#         response = self.model.generate_content(contents=prompt)
#         print(f"[DEBUG] Gemini response received.")
#         return response.text

# # -----------------------------
# # FactChecker Class
# # -----------------------------
# class FactChecker:
#     def __init__(self, llm=None, search_tool=None):
#         self.llm = llm or GeminiLLM()
#         self.search_tool = search_tool or TavilySearch(api_key=TAVILY_API_KEY)
#         print("[DEBUG] FactChecker initialized.")

#     def initial_response(self, claim: str) -> str:
#         template = PROMPTS["initial_response"]["template"]
#         prompt = template.format(claim=claim)
#         print(f"[DEBUG] Initial response prompt:\n{prompt}")
#         return self.llm.predict(prompt)

#     def extract_assumptions(self, initial_response: str) -> list:
#         template = PROMPTS["assumption_extraction"]["template"]
#         prompt = template.format(initial_response=initial_response)
#         print(f"[DEBUG] Extract assumptions prompt:\n{prompt}")
#         assumptions_text = self.llm.predict(prompt)
#         assumptions = [a.strip() for a in assumptions_text.split("\n") if a.strip()]
#         print(f"[DEBUG] Extracted assumptions: {assumptions}")
#         return assumptions

#     def gather_evidence(self, assumptions: list) -> str:
#         evidence_summary = []
#         for a in assumptions:
#             print(f"[DEBUG] Searching evidence for assumption: {a}")
#             search_results = self.search_tool.run(a)
#             evidence_summary.append(f"Assumption: {a}\nEvidence: {search_results}\n")
#             print(f"[DEBUG] Evidence found: {search_results}")
#         return "\n".join(evidence_summary)

#     def final_synthesis(self, evidence_summary: str) -> str:
#         template = PROMPTS["final_synthesis"]["template"]
#         prompt = template.format(evidence_summary=evidence_summary)
#         print(f"[DEBUG] Final synthesis prompt:\n{prompt}")
#         final_answer = self.llm.predict(prompt)
#         print(f"[DEBUG] Final synthesis result:\n{final_answer}")
#         return final_answer

#     def check_claim(self, claim: str) -> str:
#         print(f"[DEBUG] Checking claim: {claim}")
#         init_resp = self.initial_response(claim)
#         assumptions = self.extract_assumptions(init_resp)
#         evidence_summary = self.gather_evidence(assumptions)
#         final_answer = self.final_synthesis(evidence_summary)
#         return final_answer

# # -----------------------------
# # Example Usage
# # -----------------------------
# if __name__ == "__main__":
#     claim = "The capital of France is Paris."
#     fact_checker = FactChecker()
#     result = fact_checker.check_claim(claim)
#     print("Final Fact-Check Result:\n", result)




# import os
# from dotenv import load_dotenv
# from prompt_chains import FactCheckChain
# from search_tools import EvidenceSearch
# from google import generativeai as genai

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# # ------------------ DEBUG ------------------
# print(f"[DEBUG] GEMINI_API_KEY loaded: {bool(GEMINI_API_KEY)}")
# print(f"[DEBUG] TAVILY_API_KEY loaded: {bool(TAVILY_API_KEY)}")
# # -------------------------------------------


# if not GEMINI_API_KEY or not TAVILY_API_KEY:
#     raise ValueError("Missing API keys in environment variables")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# class FactChecker:
#     def __init__(self):
#         self.chain = FactCheckChain()
#         self.search = EvidenceSearch(tavily_api_key=TAVILY_API_KEY)

#     def check_claim(self, claim: str) -> str:
#         # Step 1: Initial response
#         initial_resp = self.chain.initial_response(claim)

#         # Step 2: Extract assumptions
#         assumptions = self.chain.extract_assumptions(initial_resp)

#         # Step 3: Gather evidence
#         evidence_summary = self.search.gather_evidence(assumptions)

#         # Step 4: Synthesize final answer
#         final_answer = self.chain.final_synthesis(evidence_summary)
#         return final_answer

# if __name__ == "__main__":
#     claim = "The capital of France is India."
#     checker = FactChecker()
#     result = checker.check_claim(claim)
#     print("\nFinal Fact-Check Result:\n", result)

