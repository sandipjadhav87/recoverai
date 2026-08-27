import pandas as pd

from decision_explainer import explain_decision


df = pd.read_csv("recoverai_final_results.csv")

transaction = df.iloc[0]

explanation = explain_decision(transaction)

print("\n===== RecoverAI Decision Explanation =====\n")

print("Transaction:", transaction["transaction_id"])
print("Action:", transaction["recommended_action"])

print("\nWhy did RecoverAI choose this?")

print(explanation)