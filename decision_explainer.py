def explain_decision(row):
    action = row["recommended_action"]
    reason = row["failure_reason"]
    attempts = int(row["attempts"])
    score = int(row["recovery_score"])
    priority = row["priority"]

    if action == "STOP_AND_ESCALATE":
        return (
            f"RecoverAI stopped automatic recovery because the payment "
            f"has already reached {attempts} unsuccessful attempts. "
            f"Although the failure reason is {reason.replace('_', ' ').lower()}, "
            f"further automatic attempts are restricted to avoid repeated failures. "
            f"The case is therefore escalated for operator review."
        )

    if action == "RETRY":
        return (
            f"RecoverAI recommends a controlled retry because the failure "
            f"is related to {reason.replace('_', ' ').lower()}. "
            f"The recovery score is {score}/100 and the transaction has not "
            f"exceeded the automatic retry limit."
        )

    if action == "PAYMENT_LINK":
        return (
            f"RecoverAI recommends a payment link because the failure is "
            f"related to insufficient funds. This gives the customer another "
            f"way to complete the outstanding payment."
        )

    if action == "CUSTOMER_PROMPT":
        return (
            f"RecoverAI recommends a customer prompt because the payment "
            f"requires customer attention. The customer can verify the "
            f"payment details and attempt the transaction again."
        )

    if action == "REMINDER":
        return (
            f"RecoverAI recommends a reminder because the payment remains "
            f"recoverable but does not require an immediate technical retry."
        )

    if action == "MANUAL_REVIEW":
        return (
            f"RecoverAI recommends manual review because the recovery score "
            f"is {score}/100 and automatic recovery is not considered suitable."
        )

    return (
        f"RecoverAI selected {action} based on the transaction's "
        f"risk, priority, failure reason, and previous attempts."
    )