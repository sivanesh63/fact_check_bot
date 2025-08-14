from langchain_tavily import TavilySearch

class EvidenceSearch:
    def __init__(self, tavily_api_key):
        self.search_tool = TavilySearch(api_key=tavily_api_key)

    def gather_evidence(self, assumptions: list) -> str:
        summary = []
        for a in assumptions:
            try:
                results = self.search_tool.run(a)
                summary.append(f"Assumption: {a}\nEvidence: {results}\n")
            except Exception as e:
                summary.append(f"Assumption: {a}\nEvidence: Error ({e})\n")
        return "\n".join(summary)





























# from langchain_tavily import TavilySearch

# class EvidenceSearch:
#     def __init__(self, tavily_api_key):
#         self.search_tool = TavilySearch(api_key=tavily_api_key)

#     def gather_evidence(self, assumptions: list) -> str:
#         summary = []
#         for a in assumptions:
#             try:
#                 results = self.search_tool.run(a)
#                 summary.append(f"Assumption: {a}\nEvidence: {results}\n")
#             except Exception as e:
#                 summary.append(f"Assumption: {a}\nEvidence: Error retrieving data ({e})\n")
#         return "\n".join(summary)
