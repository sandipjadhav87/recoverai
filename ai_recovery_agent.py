import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from decision_explainer import explain_decision
from message_generator import generate_recovery_message


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None
AI_ENABLED = False

def generate_ai_explanation(row):

    # Try OpenAI first
    if client and AI_ENABLED:

        try:
            prompt = f"""
You are RecoverAI, a payment revenue recovery assistant.

The recovery engine has already selected this action:
{row['recommended_action']}

Do not change the action.

Transaction:
Amount: ₹{row['amount_at_risk']}
Failure reason: {row['failure_reason']}
Attempts: {row['attempts']}
Customer type: {row['customer_type']}
Recovery score: {row['recovery_score']}/100
Recovery risk: {row['recovery_risk']}
Priority: {row['priority']}

Explain in 2-4 simple sentences why this recovery action was selected.
Do not invent information.
"""

            response = client.responses.create(
                model="gpt-5.2",
                input=prompt,
                text={"verbosity": "low"}
            )

            return response.output_text.strip(), "OpenAI"

        except Exception as e:

            print(
                f"\nOpenAI unavailable. Using local fallback.\n"
                f"Reason: {type(e).__name__}"
            )

    # Local fallback
    return explain_decision(row), "Local Fallback"


def generate_ai_customer_message(row):

    # Try OpenAI first
    if client and AI_ENABLED:

        try:
            prompt = f"""
Create a short professional customer message for this failed payment.

Amount: ₹{row['amount_at_risk']}
Failure reason: {row['failure_reason']}
Attempts: {row['attempts']}
Recovery action: {row['recommended_action']}

Rules:
- Do not mention AI.
- Do not mention internal scores.
- Do not guarantee successful payment.
- Keep it below 50 words.
"""

            response = client.responses.create(
                model="gpt-5.2",
                input=prompt,
                text={"verbosity": "low"}
            )

            return response.output_text.strip(), "OpenAI"

        except Exception:

            pass

    # Local fallback
    return generate_recovery_message(
        row,
        row["recommended_action"]
    ), "Local Fallback"


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    df = pd.read_csv(
        "recoverai_final_results.csv"
    )

    transaction = df.iloc[0]

    print("\n===================================")
    print("       RecoverAI AI Layer")
    print("===================================\n")

    print(
        "Transaction:",
        transaction["transaction_id"]
    )

    print(
        "Selected Action:",
        transaction["recommended_action"]
    )

    explanation, explanation_source = generate_ai_explanation(
        transaction
    )

    message, message_source = generate_ai_customer_message(
        transaction
    )

    print("\nDecision Explanation:")
    print(explanation)

    print(
        f"\nExplanation Source: {explanation_source}"
    )

    print("\nCustomer Message:")
    print(message)

    print(
        f"\nMessage Source: {message_source}"
    )