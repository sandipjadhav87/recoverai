def analyze_transaction(txn):

    amount = float(txn["amount"])
    reason = txn["failure_reason"]
    attempts = int(txn["attempts"])
    customer_type = txn["customer_type"]
    previous_successes = int(txn["previous_successes"])
    days = int(txn["days_since_failure"])

    # Stopping rule
    if attempts >= 3:
        return {
            "action": "STOP_AND_ESCALATE",
            "priority": "HIGH",
            "reason": "Maximum automatic recovery attempts reached."
        }

    # Temporary technical failures
    if reason in ["TEMPORARY_BANK_ERROR", "NETWORK_ERROR"]:
        return {
            "action": "RETRY",
            "priority": "HIGH" if amount >= 5000 else "MEDIUM",
            "reason": "Failure appears temporary and may succeed on retry."
        }

    # Insufficient funds
    if reason == "INSUFFICIENT_FUNDS":
        return {
            "action": "PAYMENT_LINK",
            "priority": "MEDIUM",
            "reason": "Customer may need to arrange funds before retrying."
        }

    # Authentication/card problems
    if reason in ["AUTHENTICATION_FAILURE", "CARD_EXPIRED"]:
        return {
            "action": "CUSTOMER_PROMPT",
            "priority": "MEDIUM",
            "reason": "Customer action is required to resolve the payment issue."
        }

    # Old unresolved payment
    if days > 7:
        return {
            "action": "REMINDER",
            "priority": "LOW",
            "reason": "Payment has remained unresolved for several days."
        }

    return {
        "action": "REMINDER",
        "priority": "LOW",
        "reason": "General recovery follow-up recommended."
    }