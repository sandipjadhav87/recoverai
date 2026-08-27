import pandas as pd
from recovery_engine import analyze_transaction

# Load dataset
df = pd.read_csv("data/recoverai_transactions_1000.csv")

results = []

for _, row in df.iterrows():
    result = analyze_transaction(row)

    results.append({
        "transaction_id": row["transaction_id"],
        "amount": row["amount"],
        "failure_reason": row["failure_reason"],
        "recommended_action": result["action"],
        "priority": result["priority"],
        "reason": result["reason"]
    })

results_df = pd.DataFrame(results)

# Calculate revenue at risk
total_revenue_at_risk = results_df["amount"].sum()

# Count recommended actions
action_counts = results_df["recommended_action"].value_counts()

print("\n===== RecoverAI Evaluation =====\n")

print(f"Transactions analyzed : {len(results_df)}")
print(f"Revenue at risk       : ₹{total_revenue_at_risk:,.2f}")

print("\nRecommended Actions:")
print(action_counts)

# Save results
results_df.to_csv("recovery_results.csv", index=False)

print("\nResults saved to: recovery_results.csv")