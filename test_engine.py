from recovery_engine import analyze_transaction

transaction = {
    "amount": 4999,
    "failure_reason": "TEMPORARY_BANK_ERROR",
    "attempts": 1,
    "customer_type": "RETURNING",
    "previous_successes": 7,
    "days_since_failure": 1
}

result = analyze_transaction(transaction)

print("RecoverAI Decision")
print("------------------")
print("Action:", result["action"])
print("Priority:", result["priority"])
print("Reason:", result["reason"])