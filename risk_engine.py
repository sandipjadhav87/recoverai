def calculate_recovery_score(row):
    score = 50

    amount = float(row["amount"])
    reason = row["failure_reason"]
    attempts = int(row["attempts"])
    customer_type = row["customer_type"]
    previous_successes = int(row["previous_successes"])
    days = int(row["days_since_failure"])

    # Customer history
    if customer_type == "LOYAL":
        score += 20
    elif customer_type == "RETURNING":
        score += 10

    # Previous successful payments
    if previous_successes >= 10:
        score += 10
    elif previous_successes >= 5:
        score += 5

    # Failure reason
    if reason in ["TEMPORARY_BANK_ERROR", "NETWORK_ERROR"]:
        score += 15
    elif reason == "INSUFFICIENT_FUNDS":
        score -= 5
    elif reason in ["AUTHENTICATION_FAILURE", "CARD_EXPIRED"]:
        score -= 10

    # Previous attempts
    if attempts == 1:
        score += 5
    elif attempts >= 3:
        score -= 25

    # Age of failed payment
    if days > 7:
        score -= 15
    elif days <= 2:
        score += 5

    # Very large payments get higher priority,
    # but not automatically a higher success probability
    if amount >= 10000:
        score += 5

    return max(0, min(100, score))


def classify_risk(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


def choose_action(row, score):
    reason = row["failure_reason"]
    attempts = int(row["attempts"])

    # Hard stopping rule
    if attempts >= 3:
        return "STOP_AND_ESCALATE"

    # Low recovery score
    if score < 30:
        return "MANUAL_REVIEW"

    # Temporary technical failures
    if reason in ["TEMPORARY_BANK_ERROR", "NETWORK_ERROR"]:
        return "RETRY"

    # Insufficient funds
    if reason == "INSUFFICIENT_FUNDS":
        return "PAYMENT_LINK"

    # Customer-action failures
    if reason in ["AUTHENTICATION_FAILURE", "CARD_EXPIRED"]:
        return "CUSTOMER_PROMPT"

    return "REMINDER"
def calculate_priority_score(row, recovery_score):
    amount = float(row["amount"])
    days = int(row["days_since_failure"])
    customer_type = row["customer_type"]

    score = 0

    # Revenue value
    if amount >= 25000:
        score += 40
    elif amount >= 10000:
        score += 30
    elif amount >= 5000:
        score += 20
    elif amount >= 1000:
        score += 10
    else:
        score += 5

    # Customer value
    if customer_type == "LOYAL":
        score += 25
    elif customer_type == "RETURNING":
        score += 15
    else:
        score += 5

    # Recency
    if days <= 2:
        score += 20
    elif days <= 7:
        score += 10
    else:
        score += 5

    # Recovery likelihood
    if recovery_score >= 70:
        score += 15
    elif recovery_score >= 40:
        score += 10
    elif recovery_score >= 20:
        score += 5

    return min(100, score)


def classify_priority(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"