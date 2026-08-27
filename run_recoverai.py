import pandas as pd
import random
from datetime import datetime

from risk_engine import (
    calculate_recovery_score,
    classify_risk,
    calculate_priority_score,
    classify_priority,
    choose_action
)

from message_generator import generate_recovery_message


random.seed(42)


# --------------------------------
# Load transactions
# --------------------------------

df = pd.read_csv(
    "data/recoverai_transactions_1000.csv"
)


# --------------------------------
# Recovery simulation
# --------------------------------

def simulate_recovery(action, amount):

    if action == "STOP_AND_ESCALATE":
        return "ESCALATED", 0.0

    if action == "MANUAL_REVIEW":
        return "MANUAL_REVIEW", 0.0

    probabilities = {
        "RETRY": 0.60,
        "PAYMENT_LINK": 0.50,
        "CUSTOMER_PROMPT": 0.45,
        "REMINDER": 0.35
    }

    probability = probabilities.get(action, 0.30)

    success = random.random() < probability

    if success:
        return "RECOVERED", amount

    return "FAILED", 0.0


# --------------------------------
# Run RecoverAI
# --------------------------------

results = []

for _, row in df.iterrows():

    recovery_score = calculate_recovery_score(row)

    recovery_risk = classify_risk(
        recovery_score
    )

    priority_score = calculate_priority_score(
        row,
        recovery_score
    )

    priority = classify_priority(
        priority_score
    )

    action = choose_action(
        row,
        recovery_score
    )

    message = generate_recovery_message(
        row,
        action
    )

    recovery_status, recovered_amount = simulate_recovery(
        action,
        row["amount"]
    )

    results.append({

        "timestamp":
            datetime.now().isoformat(timespec="seconds"),

        "transaction_id":
            row["transaction_id"],

        "customer_id":
            row["customer_id"],

        "amount_at_risk":
            row["amount"],

        "failure_reason":
            row["failure_reason"],

        "attempts":
            row["attempts"],

        "customer_type":
            row["customer_type"],

        "recovery_score":
            recovery_score,

        "recovery_risk":
            recovery_risk,

        "priority_score":
            priority_score,

        "priority":
            priority,

        "recommended_action":
            action,

        "recovery_status":
            recovery_status,

        "recovered_amount":
            recovered_amount,

        "customer_message":
            message,

        "audit_status":
            "RECORDED"
    })


# --------------------------------
# Create final dataset
# --------------------------------

final_df = pd.DataFrame(results)


# --------------------------------
# Calculate metrics
# --------------------------------

total_transactions = len(final_df)

total_at_risk = (
    final_df["amount_at_risk"].sum()
)

total_recovered = (
    final_df["recovered_amount"].sum()
)

successful_recoveries = (
    final_df["recovery_status"]
    .eq("RECOVERED")
    .sum()
)

recovery_attempts = (
    final_df["recovery_status"]
    .isin(["RECOVERED", "FAILED"])
    .sum()
)

escalated = (
    final_df["recovery_status"]
    .eq("ESCALATED")
    .sum()
)

manual_review = (
    final_df["recovery_status"]
    .eq("MANUAL_REVIEW")
    .sum()
)

recovery_rate = (
    total_recovered / total_at_risk * 100
    if total_at_risk > 0 else 0
)


# --------------------------------
# Display summary
# --------------------------------

print("\n===================================")
print("        RECOVERAI AGENT")
print("===================================\n")

print(
    f"Transactions processed : "
    f"{total_transactions:,}"
)

print(
    f"Revenue at risk        : "
    f"₹{total_at_risk:,.2f}"
)

print(
    f"Recovery attempts      : "
    f"{recovery_attempts:,}"
)

print(
    f"Successful recoveries  : "
    f"{successful_recoveries:,}"
)

print(
    f"Money recovered        : "
    f"₹{total_recovered:,.2f}"
)

print(
    f"Recovery rate          : "
    f"{recovery_rate:.2f}%"
)

print(
    f"Escalated cases        : "
    f"{escalated:,}"
)

print(
    f"Manual review          : "
    f"{manual_review:,}"
)


# --------------------------------
# Save final output
# --------------------------------

final_df.to_csv(
    "recoverai_final_results.csv",
    index=False
)

print(
    "\nFinal dataset saved to: "
    "recoverai_final_results.csv"
)