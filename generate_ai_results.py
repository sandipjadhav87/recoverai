import pandas as pd

from ai_recovery_agent import (
    generate_ai_explanation,
    generate_ai_customer_message
)


# ============================================================
# LOAD RECOVERY RESULTS
# ============================================================

df = pd.read_csv("recoverai_final_results.csv")


results = []


print("\n===================================")
print("      RecoverAI AI Processing")
print("===================================\n")


# ============================================================
# PROCESS TRANSACTIONS
# ============================================================

for index, row in df.iterrows():

    explanation, explanation_source = generate_ai_explanation(row)

    message, message_source = generate_ai_customer_message(row)

    results.append({

        "transaction_id":
            row["transaction_id"],

        "ai_decision_explanation":
            explanation,

        "ai_customer_message":
            message,

        "explanation_source":
            explanation_source,

        "message_source":
            message_source

    })

    # Show progress
    if (index + 1) % 100 == 0:

        print(
            f"Processed {index + 1:,} / {len(df):,}"
        )


# ============================================================
# SAVE AI RESULTS
# ============================================================

ai_df = pd.DataFrame(results)


ai_df.to_csv(
    "ai_results.csv",
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n===================================")
print("       AI Processing Complete")
print("===================================\n")

print(
    f"Transactions processed : {len(ai_df):,}"
)

print("\nExplanation Sources:")

print(
    ai_df["explanation_source"].value_counts()
)

print("\nMessage Sources:")

print(
    ai_df["message_source"].value_counts()
)

print(
    "\nSaved: ai_results.csv"
)