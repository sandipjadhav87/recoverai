def generate_recovery_message(row, action):

    customer_id = row["customer_id"]

    # Support both dataset formats
    if "amount_at_risk" in row.index:
        amount = float(row["amount_at_risk"])
    else:
        amount = float(row["amount"])

    reason = row["failure_reason"]

    name = customer_id.replace("CUST", "Customer ")

    if action == "RETRY":

        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} "
            f"could not be completed due to a temporary "
            f"payment issue. Please try the payment again "
            f"after a short while."
        )

    elif action == "PAYMENT_LINK":

        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} "
            f"could not be completed. You can complete "
            f"your payment using the secure payment link provided."
        )

    elif action == "CUSTOMER_PROMPT":

        message = (
            f"Hi {name}, your payment of ₹{amount:,.2f} "
            f"needs your attention. Please verify your "
            f"payment details and try again."
        )

    elif action == "REMINDER":

        message = (
            f"Hi {name}, this is a reminder regarding your "
            f"pending payment of ₹{amount:,.2f}. "
            f"Please complete the payment at your convenience."
        )

    elif action in ["STOP_AND_ESCALATE", "ESCALATE"]:

        message = (
            f"Payment recovery for ₹{amount:,.2f} has been "
            f"paused after multiple unsuccessful attempts. "
            f"Our support team will review the case."
        )

    elif action == "MANUAL_REVIEW":

        message = (
            f"Your payment of ₹{amount:,.2f} has been "
            f"flagged for manual review. No further automatic "
            f"recovery action will be taken at this time."
        )

    else:

        message = (
            f"Your payment of ₹{amount:,.2f} requires "
            f"further review."
        )

    return message