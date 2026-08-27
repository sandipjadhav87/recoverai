import pandas as pd
from datetime import datetime

# Load the final RecoverAI agent results
df = pd.read_csv("agent_results.csv")

audit_records = []

for _, row in df.iterrows():

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "transaction_id": row["transaction_id"],
        "customer_id": row["customer_id"],
        "amount": row["amount"],
        "failure_reason": row["failure_reason"],
        "attempts": row["attempts"],
        "recovery_score": row["recovery_score"],
        "recovery_risk": row["recovery_risk"],
        "priority_score": row["priority_score"],
        "priority": row["priority"],
        "decision": row["recommended_action"],
        "customer_message": row["customer_message"],
        "audit_status": "RECORDED"
    }

    audit_records.append(record)

audit_df = pd.DataFrame(audit_records)

audit_df.to_csv(
    "audit_log.csv",
    index=False
)

print("\n===== RecoverAI Audit Trail =====\n")

print(f"Audit records created : {len(audit_df)}")

print("\nAudit Status:")
print(audit_df["audit_status"].value_counts())

print("\nSample Audit Record:")
print(audit_df.iloc[0].to_string())

print("\nSaved: audit_log.csv")