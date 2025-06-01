import os
import json
from openai import OpenAI
from collections import defaultdict

def calculate_spending_summary(transactions):
    summary = defaultdict(float)
    for txn in transactions:
        category = txn.get("category", "OTHER")
        amount = float(txn.get("amount", 0))
        summary[category] += amount
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))


def get_card_recommendation(spending_summary):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    formatted_summary = "\n".join([
        f"{category}: ${amount:.2f}"
        for category, amount in spending_summary.items()
    ])

    prompt = f"""Based on this monthly spending pattern:
{formatted_summary}

Analyze the spending and return **strictly valid JSON** in the following format:
{{
  "recommended_cards": [
    {{
      "card_name": "string",
      "issuer": "string",
      "annual_fee": number,
      "signup_bonus": "string",
      "rewards_structure": [
        {{
          "category": "string",
          "rate": "string",
          "cap": "string"
        }}
      ],
      "estimated_monthly_savings": number,
      "justification": "string",
      "best_for_categories": ["string"]
    }}
  ],
  "cards_to_avoid": [
    {{
      "card_name": "string",
      "reason": "string"
    }}
  ],
  "spending_analysis": {{
    "highest_spending_category": "string",
    "potential_savings": number,
    "recommendation_summary": "string"
  }}
}}

Respond ONLY with valid JSON, no explanation, no markdown, no commentary.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a credit card expert. Only respond with JSON data. Do not include any markdown or free text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1800
        )
        
        # Try parsing JSON
        content = response.choices[0].message.content.strip()
        return json.loads(content)
        
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse GPT response",
            "details": str(e),
            "raw_response": content
        }
    except Exception as e:
        return {
            "error": "Error getting card recommendations",
            "details": str(e)
        }
