import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import razorpay


# ============================================================
# LOAD RAZORPAY TEST MODE CREDENTIALS
# ============================================================

load_dotenv()

KEY_ID = os.getenv("RAZORPAY_KEY_ID")
KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


# ============================================================
# CREATE RAZORPAY CLIENT
# ============================================================

def get_client():

    if not KEY_ID or not KEY_SECRET:
        raise RuntimeError(
            "Razorpay Test API keys are missing from .env"
        )

    return razorpay.Client(
        auth=(KEY_ID, KEY_SECRET)
    )


# ============================================================
# CREATE TEST PAYMENT LINK
# ============================================================

def create_test_payment_link(
    amount,
    transaction_id,
    customer_id
):
    """
    Creates a Razorpay Test Mode payment link.

    Amount is provided in INR and converted to paise.
    """

    client = get_client()

    amount_paise = int(
        round(float(amount) * 100)
    )

    data = {
        "amount": amount_paise,
        "currency": "INR",
        "accept_partial": False,
        "description": (
            f"RecoverAI recovery for {transaction_id}"
        ),
        "reference_id": transaction_id,

        "customer": {
            "name": customer_id
        },

        "notify": {
            "sms": False,
            "email": False
        },

        "reminder_enable": False
    }

    # Create payment link through Razorpay Test API
    payment_link = client.payment_link.create(data)

    result = {
        "id": payment_link.get("id"),
        "short_url": payment_link.get("short_url"),
        "status": payment_link.get("status"),
        "amount": payment_link.get("amount"),
        "currency": payment_link.get("currency"),
        "reference_id": payment_link.get("reference_id")
    }

    # Save the Razorpay link for the audit trail
    save_payment_link_record(
        transaction_id=transaction_id,
        customer_id=customer_id,
        amount=amount,
        result=result
    )

    return result


# ============================================================
# SAVE PAYMENT LINK RECORD
# ============================================================

def save_payment_link_record(
    transaction_id,
    customer_id,
    amount,
    result
):

    file_name = "razorpay_payment_links.csv"

    record = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),

        "transaction_id": transaction_id,

        "customer_id": customer_id,

        "amount": float(amount),

        "payment_link_id": result.get(
            "id",
            ""
        ),

        "payment_link_url": result.get(
            "short_url",
            ""
        ),

        "payment_link_status": result.get(
            "status",
            ""
        ),

        "reference_id": result.get(
            "reference_id",
            ""
        )
    }

    new_record = pd.DataFrame([record])

    # Append to existing file if it exists
    if os.path.exists(file_name):

        existing = pd.read_csv(file_name)

        updated = pd.concat(
            [existing, new_record],
            ignore_index=True
        )

    else:

        updated = new_record

    updated.to_csv(
        file_name,
        index=False
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("===================================")
    print("   RecoverAI Razorpay Integration")
    print("===================================")

    if KEY_ID:
        print(
            f"Key ID loaded: {KEY_ID[:12]}..."
        )
    else:
        print("Key ID missing")

    result = create_test_payment_link(
        amount=873.17,
        transaction_id="TXN10000",
        customer_id="CUST1099"
    )

    print("\nTest Payment Link Created")
    print("-------------------------")

    print(
        "Link ID     :",
        result["id"]
    )

    print(
        "Payment URL :",
        result["short_url"]
    )

    print(
        "Status      :",
        result["status"]
    )

    print(
        "Amount      :",
        result["amount"] / 100
    )

    print(
        "Reference   :",
        result["reference_id"]
    )

    print(
        "\nSaved: razorpay_payment_links.csv"
    )