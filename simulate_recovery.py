import pandas as pd
import random

random.seed(42)

# Load RecoverAI evaluation results
df = pd.read_csv("recovery_results.csv")


def simulate_action(row):
    action = row["recommended_action"]

    # Stopping rule: no automatic recovery
    if action == "STOP_AND_ESCALATE":
        return "ESCALATED", 0.0

    # Simulated success probabilities for the prototype
    probabilities = {
        "RETRY": 0.60,
        "PAYMENT_LINK": 0.50,
        "CUSTOMER_PROMPT": 0.45,
        "REMINDER": 0.35
    }

    success = random.random() < probabilities[action]

    if success:
        return "RECOVERED", row["amount"]

    return "FAILED", 0.0


# Run simulation
results = []

for _, row in df.iterrows():

    status, recovered_amount = simulate_action(row)

    results.append({
        "transaction_id": row["transaction_id"],
        "amount_at_risk": row["amount"],
        "failure_reason": row["failure_reason"],
        "recommended_action": row["recommended_action"],
        "priority": row["priority"],
        "recovery_status": status,
        "recovered_amount": recovered_amount
    })


results_df = pd.DataFrame(results)

# Calculate metrics
total_at_risk = results_df["amount_at_risk"].sum()

total_recovered = results_df["recovered_amount"].sum()

recovered_count = (
    results_df["recovery_status"] == "RECOVERED"
).sum()

attempted_count = (
    results_df["recovery_status"].isin(["RECOVERED", "FAILED"])
).sum()

escalated_count = (
    results_df["recovery_status"] == "ESCALATED"
).sum()

recovery_rate = (
    total_recovered / total_at_risk * 100
)

attempt_success_rate = (
    recovered_count / attempted_count * 100
    if attempted_count > 0 else 0
)


print("\n===== RecoverAI Recovery Simulation =====\n")

print(f"Transactions analyzed : {len(results_df)}")
print(f"Revenue at risk       : ₹{total_at_risk:,.2f}")
print(f"Recovery attempts     : {attempted_count}")
print(f"Successful recoveries : {recovered_count}")
print(f"Money recovered       : ₹{total_recovered:,.2f}")
print(f"Revenue recovery rate : {recovery_rate:.2f}%")
print(f"Attempt success rate  : {attempt_success_rate:.2f}%")
print(f"Escalated cases       : {escalated_count}")

# Save detailed audit results
results_df.to_csv("recovery_simulation.csv", index=False)

print("\nDetailed results saved to: recovery_simulation.csv")