import os
import pandas as pd
from datetime import datetime


# ============================================================
# LOAD RECOVERAI RESULTS
# ============================================================

if os.path.exists("agent_results.csv"):
    INPUT_FILE = "agent_results.csv"
elif os.path.exists("recoverai_final_results.csv"):
    INPUT_FILE = "recoverai_final_results.csv"
else:
    raise FileNotFoundError(
        "Could not find agent_results.csv or recoverai_final_results.csv"
    )


df = pd.read_csv(INPUT_FILE)


# ============================================================
# LOAD RAZORPAY PAYMENT LINK RECORDS
# ============================================================

razorpay_file = "razorpay_payment_links.csv"

if os.path.exists(razorpay_file):

    razorpay_df = pd.read_csv(
        razorpay_file
    )

else:

    razorpay_df = pd.DataFrame()


# ============================================================
# CREATE AUDIT RECORDS
# ============================================================

audit_records = []


for _, row in df.iterrows():

    transaction_id = row["transaction_id"]

    # Support both "amount" and "amount_at_risk"
    if "amount" in row.index:
        amount = row["amount"]
    elif "amount_at_risk" in row.index:
        amount = row["amount_at_risk"]
    else:
        amount = 0.0


    # Customer message
    if "customer_message" in row.index:

        customer_message = row["customer_message"]

    elif "ai_customer_message" in row.index:

        customer_message = row[
            "ai_customer_message"
        ]

    else:

        customer_message = ""


    # ========================================================
    # RAZORPAY INFORMATION
    # ========================================================

    razorpay_link_id = ""
    razorpay_link_url = ""
    razorpay_link_status = ""


    if not razorpay_df.empty:

        matching = razorpay_df[
            razorpay_df["transaction_id"]
            == transaction_id
        ]


        if not matching.empty:

            razorpay_row = matching.iloc[-1]


            razorpay_link_id = str(
                razorpay_row.get(
                    "payment_link_id",
                    ""
                )
            )


            razorpay_link_url = str(
                razorpay_row.get(
                    "payment_link_url",
                    ""
                )
            )


            razorpay_link_status = str(
                razorpay_row.get(
                    "payment_link_status",
                    ""
                )
            )


    # ========================================================
    # AUDIT RECORD
    # ========================================================

    record = {

        "timestamp":
            datetime.now().isoformat(
                timespec="seconds"
            ),

        "transaction_id":
            transaction_id,

        "customer_id":
            row["customer_id"],

        "amount":
            amount,

        "failure_reason":
            row["failure_reason"],

        "attempts":
            row["attempts"],

        "recovery_score":
            row["recovery_score"],

        "recovery_risk":
            row["recovery_risk"],

        "priority_score":
            row["priority_score"],

        "priority":
            row["priority"],

        "decision":
            row["recommended_action"],

        "customer_message":
            customer_message,

        "razorpay_payment_link_id":
            razorpay_link_id,

        "razorpay_payment_link_url":
            razorpay_link_url,

        "razorpay_payment_link_status":
            razorpay_link_status,

        "audit_status":
            "RECORDED"
    }


    audit_records.append(record)


# ============================================================
# CREATE DATAFRAME
# ============================================================

audit_df = pd.DataFrame(
    audit_records
)


# ============================================================
# SAVE AUDIT LOG
# ============================================================

audit_df.to_csv(
    "audit_log.csv",
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print(
    "\n===== RecoverAI Audit Trail =====\n"
)


print(
    f"Audit records created : "
    f"{len(audit_df)}"
)


print(
    "\nAudit Status:"
)


print(
    audit_df[
        "audit_status"
    ].value_counts()
)


# ============================================================
# RAZORPAY LINK COUNT
# ============================================================

if "razorpay_payment_link_id" in audit_df.columns:

    razorpay_count = (

        audit_df[
            "razorpay_payment_link_id"
        ]

        .fillna("")

        .astype(str)

        .str.strip()

        .ne("")

        .sum()

    )

else:

    razorpay_count = 0


print(
    "\nRazorpay Payment Links Recorded:"
)


print(
    f"Payment links recorded : "
    f"{razorpay_count}"
)


# ============================================================
# SAMPLE RECORD
# ============================================================

print(
    "\nSample Audit Record:"
)


print(
    audit_df.iloc[0].to_string()
)


print(
    "\nSaved: audit_log.csv"
)