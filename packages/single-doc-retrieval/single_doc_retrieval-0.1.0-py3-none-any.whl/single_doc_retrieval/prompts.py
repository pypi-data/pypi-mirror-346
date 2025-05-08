# LLM Prompts

SUFFICIENCY_PROMPT_TEMPLATE = """Given the following query: {}

And the following context from a document:

---
{}
---

Does the provided context contain sufficient information to answer the query? Answer only with 'Yes' or 'No'."""

SUFFICIENCY_SYSTEM_ROLE = "You are an assistant determining context sufficiency. Respond only with 'Yes' or 'No'."

QUERY_REFINEMENT_SYSTEM_ROLE = """You are an expert search query assistant. Your task is to refine a user's query based on the original goal and provided (insufficient) context to improve search results.
Do not try to answer the original question. Only output the refined search query. The refined query should be on a single line."""

QUERY_REFINEMENT_PROMPT_TEMPLATE = """The user's original goal is to find: "{original_query}"
The current search query used is: "{current_query}"
The following context was retrieved using the current query, but it was deemed INSUFFICIENT to answer the original goal:
---
{insufficient_context}
---
Based on the original goal, the current query, and the insufficient context, generate a new, improved search query.
The new query should aim to find text snippets that would better help answer the original goal.
If the context is empty, try to rephrase or broaden the current query to get some initial results.
Output ONLY the new search query text and nothing else.
""" 