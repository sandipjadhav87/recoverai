import pandas as pd

from message_generator import generate_recovery_message

df = pd.read_csv("data/recoverai_transactions_1000.csv")

transaction = df.iloc[0]

action = transaction["recovery_action"]

message = generate_recovery_message(
    transaction,
    action
)

print("\n===== RecoverAI Message Generator =====\n")
print("Customer:", transaction["customer_id"])
print("Amount: ₹", transaction["amount"])
print("Action:", action)
print("\nGenerated Message:")
print(message)