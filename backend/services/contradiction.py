from services.llm import call_llm
import json
import re


def find_contradictions(document_a: str, document_b: str) -> dict:
    system_prompt = """You are an expert Indian legal analyst specializing in contract review.
Your task is to compare two legal documents and identify every contradiction, conflict, or incompatibility between them.

For each contradiction found, provide:
1. The specific clause or topic
2. What Party A's document says
3. What Party B's document says
4. A practical suggested resolution

Respond ONLY in this exact JSON format with no text before or after:
{
  "total_contradictions": <number>,
  "overall_compatibility": "<High/Medium/Low> - one line explanation",
  "contradictions": [
    {
      "clause": "<topic or clause name>",
      "party_a_position": "<what document A says>",
      "party_b_position": "<what document B says>",
      "suggested_resolution": "<how to resolve this conflict>"
    }
  ]
}"""

    user_message = f"""Compare these two legal documents and identify all contradictions:

=== DOCUMENT A ===
{document_a[:4000]}

=== DOCUMENT B ===
{document_b[:4000]}

Return only the JSON response."""

    raw = call_llm(system_prompt, user_message)

    try:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"[Contradiction] JSON parse error: {e}")

    return {
        "total_contradictions": 0,
        "overall_compatibility": "Unable to analyze — please try again",
        "contradictions": []
    }
