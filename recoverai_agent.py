import pandas as pd

from risk_engine import (
    calculate_recovery_score,
    classify_risk,
    calculate_priority_score,
    classify_priority,
    choose_action
)

from message_generator import generate_recovery_message


# Load transaction dataset
df = pd.read_csv("data/recoverai_transactions_1000.csv")

results = []

for _, row in df.iterrows():

    # Step 1: Recovery likelihood
    recovery_score = calculate_recovery_score(row)
    recovery_risk = classify_risk(recovery_score)

    # Step 2: Business priority
    priority_score = calculate_priority_score(
        row,
        recovery_score
    )
    priority = classify_priority(priority_score)

    # Step 3: Recovery decision
    action = choose_action(
        row,
        recovery_score
    )

    # Step 4: Customer communication
    message = generate_recovery_message(
        row,
        action
    )

    # Step 5: Audit record
    results.append({
        "transaction_id": row["transaction_id"],
        "customer_id": row["customer_id"],
        "amount": row["amount"],
        "failure_reason": row["failure_reason"],
        "attempts": row["attempts"],
        "recovery_score": recovery_score,
        "recovery_risk": recovery_risk,
        "priority_score": priority_score,
        "priority": priority,
        "recommended_action": action,
        "customer_message": message
    })


# Create final agent dataset
agent_df = pd.DataFrame(results)

# Save results
agent_df.to_csv(
    "agent_results.csv",
    index=False
)


# Summary
print("\n===== RecoverAI Agent =====\n")

print(f"Transactions processed : {len(agent_df)}")
print(
    f"Revenue at risk        : "
    f"₹{agent_df['amount'].sum():,.2f}"
)

print("\nRecovery Risk:")
print(agent_df["recovery_risk"].value_counts())

print("\nPriority:")
print(agent_df["priority"].value_counts())

print("\nRecovery Actions:")
print(agent_df["recommended_action"].value_counts())

print("\nSaved: agent_results.csv")