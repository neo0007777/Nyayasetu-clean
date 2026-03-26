from services.llm import call_llm
import json
import re


def find_contradictions(document_a: str, document_b: str) -> dict:
    system_prompt = """You are an expert Indian legal analyst specializing in contract review.
Compare two legal documents and identify every contradiction, conflict, or incompatibility.

You MUST respond ONLY with a valid JSON object. No text before or after. No markdown. No explanation.
Use exactly this format:
{
  "total_contradictions": 2,
  "overall_compatibility": "Low - multiple conflicts found",
  "contradictions": [
    {
      "clause": "Termination Notice Period",
      "party_a_position": "30 days written notice required",
      "party_b_position": "90 days notice required per addendum",
      "suggested_resolution": "Adopt the longer 90-day period to protect both parties"
    }
  ]
}

If no contradictions exist, return:
{"total_contradictions": 0, "overall_compatibility": "High - documents are compatible", "contradictions": []}"""

    user_message = f"""Find ALL contradictions between these two documents:

=== DOCUMENT A ===
{document_a[:5000]}

=== DOCUMENT B ===
{document_b[:5000]}

Return ONLY the JSON object. Nothing else."""

    raw = call_llm(system_prompt, user_message)
    print(f"[Contradiction] Raw LLM response: {raw[:500]}")

    # Try multiple JSON extraction strategies
    # Strategy 1: Direct parse
    try:
        return json.loads(raw.strip())
    except Exception:
        pass

    # Strategy 2: Extract JSON block
    try:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    # Strategy 3: Find JSON after any text
    try:
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(raw[start:end])
    except Exception as e:
        print(f"[Contradiction] All parse strategies failed: {e}")
        print(f"[Contradiction] Full raw response: {raw}")

    # Fallback: manually build response from text
    return {
        "total_contradictions": 1,
        "overall_compatibility": "Unable to parse structured response - manual review needed",
        "contradictions": [
            {
                "clause": "AI Analysis",
                "party_a_position": "See raw analysis",
                "party_b_position": raw[:500] if raw else "No response",
                "suggested_resolution": "Please review documents manually"
            }
        ]
    }
