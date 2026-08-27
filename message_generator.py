def generate_recovery_message(row, action):
    customer_id = row["customer_id"]
    amount = float(row["amount"])
    reason = row["failure_reason"]

    name = customer_id.replace("CUST", "Customer ")

    if action == "RETRY":
        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} could not be completed "
            f"due to a temporary payment issue. Please try the payment again "
            f"after a short while."
        )

    elif action == "PAYMENT_LINK":
        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} could not be completed. "
            f"You can complete your payment using the secure payment link provided."
        )

    elif action == "CUSTOMER_PROMPT":
        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} needs your attention. "
            f"Please verify your payment details and try again."
        )

    elif action == "REMINDER":
        message = (
            f"Hi {name}, this is a reminder regarding your pending payment of "
            f"₹{amount:,.2f}. Please complete the payment at your convenience."
        )

    elif action in ["STOP_AND_ESCALATE", "ESCALATE"]:
        message = (
            f"Payment recovery for ₹{amount:,.2f} has been paused after multiple "
            f"unsuccessful attempts. Our support team will review the case."
        )

    else:
        message = (
           f"Your payment of ₹{amount:,.2f} has been flagged for manual review. "
        f"No further automatic recovery action will be taken at this time."
        )

    return message