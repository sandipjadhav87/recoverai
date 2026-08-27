import pandas as pd

from risk_engine import (
    calculate_recovery_score,
    classify_risk,
    calculate_priority_score,
    classify_priority,
    choose_action
)

# Load all transactions
df = pd.read_csv("data/recoverai_transactions_1000.csv")

results = []

for _, row in df.iterrows():

    recovery_score = calculate_recovery_score(row)

    recovery_risk = classify_risk(recovery_score)

    priority_score = calculate_priority_score(
        row,
        recovery_score
    )

    priority = classify_priority(priority_score)

    action = choose_action(
        row,
        recovery_score
    )

    results.append({
        "transaction_id": row["transaction_id"],
        "customer_id": row["customer_id"],
        "amount": row["amount"],
        "failure_reason": row["failure_reason"],
        "attempts": row["attempts"],
        "customer_type": row["customer_type"],
        "recovery_score": recovery_score,
        "recovery_risk": recovery_risk,
        "priority_score": priority_score,
        "priority": priority,
        "recommended_action": action
    })

results_df = pd.DataFrame(results)

# Summary
total_transactions = len(results_df)
total_revenue = results_df["amount"].sum()

print("\n===== RecoverAI Batch Evaluation =====\n")

print(f"Transactions analyzed : {total_transactions}")
print(f"Revenue at risk       : ₹{total_revenue:,.2f}")

print("\nRecovery Risk:")
print(results_df["recovery_risk"].value_counts())

print("\nPriority:")
print(results_df["priority"].value_counts())

print("\nRecommended Actions:")
print(results_df["recommended_action"].value_counts())

# Save results
results_df.to_csv(
    "batch_risk_results.csv",
    index=False
)

print("\nSaved: batch_risk_results.csv")