import pandas as pd

from risk_engine import (
    calculate_recovery_score,
    classify_risk,
    calculate_priority_score,
    classify_priority,
    choose_action
)

df = pd.read_csv("data/recoverai_transactions_1000.csv")

transaction = df.iloc[0]

recovery_score = calculate_recovery_score(transaction)
risk = classify_risk(recovery_score)

priority_score = calculate_priority_score(
    transaction,
    recovery_score
)

priority = classify_priority(priority_score)

action = choose_action(
    transaction,
    recovery_score
)

print("\n===== RecoverAI Risk Engine =====")
print(f"Transaction       : {transaction['transaction_id']}")
print(f"Amount            : ₹{transaction['amount']:,.2f}")
print(f"Failure           : {transaction['failure_reason']}")
print(f"Attempts           : {transaction['attempts']}")
print(f"Recovery Score     : {recovery_score}/100")
print(f"Recovery Risk      : {risk}")
print(f"Priority Score     : {priority_score}/100")
print(f"Priority           : {priority}")
print(f"Recommended Action : {action}")