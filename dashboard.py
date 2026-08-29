import os
import pandas as pd
import streamlit as st

from razorpay_integration import create_test_payment_link


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RecoverAI | Revenue Recovery",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS - FINAL FINTECH UI
# ============================================================

st.html("""
<style>
/* ---------- Global ---------- */
[data-testid="stAppViewContainer"] {
    background: #eef3f8;
}

[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 0rem;
    padding-bottom: 3rem;
}

/* ---------- Hero ---------- */
.recover-header {
    background: linear-gradient(135deg, #081b35 0%, #123d73 55%, #1768b3 100%);
    border-radius: 24px;
    padding: 34px 38px;
    margin-bottom: 28px;
    color: white;
    box-shadow: 0 16px 35px rgba(8, 27, 53, 0.18);
}

.recover-eyebrow {
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.72;
    margin-bottom: 7px;
}

.recover-title {
    font-size: 42px;
    line-height: 1.05;
    font-weight: 850;
    letter-spacing: -1.5px;
}

.recover-subtitle {
    font-size: 17px;
    margin-top: 9px;
    opacity: 0.88;
}

.recover-status {
    display: inline-block;
    margin-top: 20px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 13px;
    font-weight: 650;
}

/* ---------- Sections ---------- */
.section-title {
    font-size: 27px;
    line-height: 1.2;
    font-weight: 850;
    color: #172235;
    margin-top: 16px;
    margin-bottom: 5px;
}

.section-subtitle {
    font-size: 14px;
    color: #66758c;
    margin-bottom: 18px;
}

/* ---------- KPI cards ---------- */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #dfe7f0;
    border-radius: 18px;
    padding: 19px 20px;
    box-shadow: 0 5px 18px rgba(21, 39, 63, 0.055);
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #172235 !important;
    font-weight: 800 !important;
}

/* ---------- Generic cards ---------- */
.info-card,
.razorpay-card,
.audit-card {
    background: #ffffff;
    border: 1px solid #dfe7f0;
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 5px 18px rgba(21, 39, 63, 0.045);
}

.info-title {
    font-size: 17px;
    font-weight: 800;
    color: #172235;
}

.info-subtitle {
    font-size: 13px;
    color: #718096;
    margin-top: 4px;
}

/* ---------- Analytics card headers ---------- */
.chart-head {
    background: #ffffff;
    border: 1px solid #dfe7f0;
    border-radius: 18px 18px 0 0;
    padding: 18px 20px 9px 20px;
    margin-top: 4px;
}

.chart-note {
    background: #ffffff;
    border: 1px solid #dfe7f0;
    border-top: 0;
    border-radius: 0 0 18px 18px;
    padding: 8px 20px 15px 20px;
    color: #718096;
    font-size: 12px;
}

/* ---------- Decision ---------- */
.decision-card {
    background: linear-gradient(135deg, #e9f3ff 0%, #f7fbff 100%);
    border: 1px solid #c8def7;
    border-radius: 20px;
    padding: 24px 26px;
    margin: 14px 0 22px 0;
    box-shadow: 0 7px 20px rgba(23, 104, 179, 0.07);
}

.decision-label {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #60718a;
}

.decision-value {
    font-size: 31px;
    font-weight: 850;
    color: #12579b;
    margin-top: 5px;
}

.decision-meta {
    margin-top: 6px;
    color: #60718a;
    font-size: 13px;
}

/* ---------- Razorpay ---------- */
.razorpay-card {
    background: linear-gradient(135deg, #fff8f1, #fffdf9);
    border-color: #efd7c2;
    margin-top: 20px;
}

/* ---------- Audit ---------- */
.audit-card {
    margin-top: 20px;
}

.timeline {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 15px;
}

.timeline-step {
    background: #f4f7fb;
    border: 1px solid #dfe7f0;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 12px;
    font-weight: 700;
    color: #334155;
}

.timeline-arrow {
    color: #94a3b8;
    font-weight: 800;
}

/* ---------- Buttons ---------- */
.stButton > button,
.stLinkButton > a {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

/* ---------- Filters ---------- */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div {
    border-radius: 11px;
}

/* ---------- Table ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #dfe7f0;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(21, 39, 63, 0.04);
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    padding: 20px 0 5px;
}

/* ---------- Mobile ---------- */
@media (max-width: 900px) {
    .recover-title { font-size: 34px; }
    .recover-header { padding: 28px 24px; }
}
</style>
""")


# ============================================================
# LOAD DATA
# ============================================================

try:
    df = pd.read_csv("recoverai_final_results.csv")
except FileNotFoundError:
    st.error("recoverai_final_results.csv was not found.")
    st.info("Run: python run_recoverai.py")
    st.stop()

try:
    ai_df = pd.read_csv("ai_results.csv")
except FileNotFoundError:
    st.error("ai_results.csv was not found.")
    st.info("Run: python generate_ai_results.py")
    st.stop()


# ============================================================
# MERGE AI DATA SAFELY
# ============================================================

df = df.merge(ai_df, on="transaction_id", how="left", suffixes=("", "_ai"))

# If the merge created duplicate columns, prefer the original values.
for col in [
    "recovery_score",
    "recovery_risk",
    "priority_score",
    "priority",
    "recommended_action",
]:
    ai_col = f"{col}_ai"
    if ai_col in df.columns:
        if col not in df.columns:
            df[col] = df[ai_col]
        else:
            df[col] = df[col].fillna(df[ai_col])

# Required display columns
required_columns = [
    "transaction_id",
    "customer_id",
    "amount_at_risk",
    "failure_reason",
    "attempts",
    "recovery_score",
    "recovery_risk",
    "priority_score",
    "priority",
    "recommended_action",
    "recovery_status",
    "recovered_amount",
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error("Dashboard is missing required columns:")
    st.code(", ".join(missing))
    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_transactions = len(df)
total_at_risk = pd.to_numeric(df["amount_at_risk"], errors="coerce").fillna(0).sum()
total_recovered = pd.to_numeric(df["recovered_amount"], errors="coerce").fillna(0).sum()

recovery_rate = (
    total_recovered / total_at_risk * 100
    if total_at_risk > 0
    else 0
)

successful = (df["recovery_status"] == "RECOVERED").sum()
failed = (df["recovery_status"] == "FAILED").sum()
escalated = (df["recovery_status"] == "ESCALATED").sum()
manual_review = (df["recovery_status"] == "MANUAL_REVIEW").sum()


# ============================================================
# LABELS
# ============================================================

action_labels = {
    "STOP_AND_ESCALATE": "Stop & Escalate",
    "CUSTOMER_PROMPT": "Customer Prompt",
    "PAYMENT_LINK": "Payment Link",
    "MANUAL_REVIEW": "Manual Review",
    "RETRY": "Retry",
    "REMINDER": "Reminder",
}

status_labels = {
    "RECOVERED": "Recovered",
    "FAILED": "Failed",
    "ESCALATED": "Escalated",
    "MANUAL_REVIEW": "Manual Review",
}


display_df = df.copy()

display_df["recommended_action_display"] = (
    display_df["recommended_action"]
    .map(action_labels)
    .fillna(display_df["recommended_action"])
)

display_df["recovery_status_display"] = (
    display_df["recovery_status"]
    .map(status_labels)
    .fillna(display_df["recovery_status"])
)


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="recover-header">
    <div class="recover-eyebrow">Payment Revenue Intelligence</div>
    <div class="recover-title">RecoverAI</div>
    <div class="recover-subtitle">
        AI-powered payment recovery operations for failed transactions.
    </div>
    <div class="recover-status">
        ● Recovery Engine Active &nbsp; | &nbsp; Razorpay Test Mode Integrated
    </div>
</div>
""")


# ============================================================
# PERFORMANCE
# ============================================================

st.html("""
<div class="section-title">Recovery Performance</div>
<div class="section-subtitle">
    Executive view of revenue exposure and recovery outcomes.
</div>
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue at Risk", f"₹{total_at_risk:,.0f}")

with col2:
    st.metric("Revenue Recovered", f"₹{total_recovered:,.0f}")

with col3:
    st.metric("Recovery Rate", f"{recovery_rate:.2f}%")

with col4:
    st.metric("Successful Recoveries", f"{successful:,}")

st.write("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Transactions Analyzed", f"{total_transactions:,}")

with col2:
    st.metric("Escalated Cases", f"{escalated:,}")

with col3:
    st.metric("Failed Recoveries", f"{failed:,}")

with col4:
    st.metric("Manual Reviews", f"{manual_review:,}")


st.divider()


# ============================================================
# ANALYTICS
# ============================================================

st.html("""
<div class="section-title">Recovery Analytics</div>
<div class="section-subtitle">
    See how RecoverAI distributes risk and chooses recovery actions.
</div>
""")

col1, col2 = st.columns(2)

with col1:
    st.html("""
    <div class="chart-head">
        <div class="info-title">Recovery Risk</div>
        <div class="info-subtitle">
            Number of transactions in each recovery-risk category.
        </div>
    </div>
    """)

    risk_counts = (
        df["recovery_risk"]
        .value_counts()
        .reindex(["HIGH", "MEDIUM", "LOW"])
        .fillna(0)
        .astype(int)
    )

    st.bar_chart(risk_counts,width="stretch")

    st.html("""
    <div class="chart-note">
        Higher-risk transactions receive greater attention in the recovery queue.
    </div>
    """)

with col2:
    st.html("""
    <div class="chart-head">
        <div class="info-title">Recommended Actions</div>
        <div class="info-subtitle">
            Recovery strategies selected by RecoverAI.
        </div>
    </div>
    """)

    action_counts = display_df["recommended_action_display"].value_counts()

    st.bar_chart(action_counts, width="stretch")

    st.html("""
    <div class="chart-note">
        Different failure conditions can lead to different recovery actions.
    </div>
    """)


st.write("")

st.html("""
<div class="chart-head">
    <div class="info-title">Recovery Outcomes</div>
    <div class="info-subtitle">
        Simulated outcomes across the transaction set.
    </div>
</div>
""")

outcome_counts = display_df["recovery_status_display"].value_counts()

st.bar_chart(outcome_counts, width="stretch")

st.html("""
<div class="chart-note">
    Recovery outcomes are simulated for this prototype evaluation.
</div>
""")


st.divider()


# ============================================================
# RECOVERY QUEUE
# ============================================================

st.html("""
<div class="section-title">Recovery Queue</div>
<div class="section-subtitle">
    Find the transactions that need attention and inspect their recommended action.
</div>
""")

search_col, risk_col, priority_col, action_col = st.columns([1.35, 1, 1, 1])

with search_col:
    search_term = st.text_input(
        "Search",
        placeholder="Transaction or customer ID",
    )

with risk_col:
    risk_filter = st.multiselect(
        "Risk",
        ["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"],
    )

with priority_col:
    priority_filter = st.multiselect(
        "Priority",
        ["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"],
    )

with action_col:
    action_options = list(action_labels.values())
    action_filter = st.multiselect(
        "Recovery Action",
        action_options,
        default=action_options,
    )


filtered = display_df[
    display_df["recovery_risk"].isin(risk_filter)
    & display_df["priority"].isin(priority_filter)
    & display_df["recommended_action_display"].isin(action_filter)
].copy()

if search_term.strip():
    term = search_term.strip().lower()
    filtered = filtered[
        filtered["transaction_id"].astype(str).str.lower().str.contains(term, na=False)
        | filtered["customer_id"].astype(str).str.lower().str.contains(term, na=False)
    ]

st.caption(
    f"Showing {len(filtered):,} of {len(df):,} transactions"
)


queue_columns = [
    "transaction_id",
    "customer_id",
    "amount_at_risk",
    "failure_reason",
    "recovery_score",
    "recovery_risk",
    "priority",
    "recommended_action_display",
    "recovery_status_display",
]

queue = filtered[queue_columns].rename(
    columns={
        "transaction_id": "Transaction",
        "customer_id": "Customer",
        "amount_at_risk": "Amount at Risk",
        "failure_reason": "Failure Reason",
        "recovery_score": "Recovery Score",
        "recovery_risk": "Risk",
        "priority": "Priority",
        "recommended_action_display": "Recommended Action",
        "recovery_status_display": "Status",
    }
)

st.dataframe(
    queue,
    width="stretch",
    hide_index=True,
    height=390,
)


st.divider()


# ============================================================
# TRANSACTION INVESTIGATION
# ============================================================

st.html("""
<div class="section-title">Transaction Investigation</div>
<div class="section-subtitle">
    Follow one payment from AI analysis to recovery execution and audit.
</div>
""")

if len(filtered) == 0:
    st.warning("No transactions match the selected filters.")
    st.stop()

# Prefer TXN10019 for the demo when it is currently visible.
preferred = "TXN10019"
transaction_ids = filtered["transaction_id"].tolist()

default_index = (
    transaction_ids.index(preferred)
    if preferred in transaction_ids
    else 0
)

selected_id = st.selectbox(
    "Select a transaction",
    transaction_ids,
    index=default_index,
)

transaction = df[df["transaction_id"] == selected_id].iloc[0]

action = action_labels.get(
    transaction["recommended_action"],
    transaction["recommended_action"],
)


# ============================================================
# DECISION HERO
# ============================================================

st.html(
    f"""
    <div class="decision-card">
        <div class="decision-label">RecoverAI Recommended Action</div>
        <div class="decision-value">{action}</div>
        <div class="decision-meta">
            Transaction {transaction["transaction_id"]}
            &nbsp; • &nbsp;
            ₹{transaction["amount_at_risk"]:,.2f} at risk
        </div>
    </div>
    """
)


# ============================================================
# PAYMENT + DECISION DETAILS
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.html("""
    <div class="info-card">
        <div class="info-title">Payment Details</div>
        <div class="info-subtitle">Transaction context</div>
    </div>
    """)

    st.write(f"**Transaction:** {transaction['transaction_id']}")
    st.write(f"**Customer:** {transaction['customer_id']}")
    st.write(f"**Amount at Risk:** ₹{transaction['amount_at_risk']:,.2f}")
    st.write(f"**Failure Reason:** {transaction['failure_reason']}")
    st.write(f"**Previous Attempts:** {transaction['attempts']}")

with col2:
    st.html("""
    <div class="info-card">
        <div class="info-title">Decision Intelligence</div>
        <div class="info-subtitle">Why this case was prioritized</div>
    </div>
    """)

    st.write(f"**Recovery Score:** {transaction['recovery_score']}/100")
    st.write(f"**Recovery Risk:** {transaction['recovery_risk']}")
    st.write(f"**Priority Score:** {transaction['priority_score']}/100")
    st.write(f"**Priority:** {transaction['priority']}")


# ============================================================
# AI EXPLANATION
# ============================================================

st.write("")

st.html("""
<div class="info-card">
    <div class="info-title">AI Decision Explanation</div>
    <div class="info-subtitle">
        RecoverAI explains the reasoning behind the recommended action.
    </div>
</div>
""")

ai_explanation = transaction.get("ai_decision_explanation")

if pd.isna(ai_explanation):
    st.warning("AI explanation is not available.")
else:
    st.info(ai_explanation)

st.caption(
    "Explanation source: "
    f"{transaction.get('explanation_source', 'Local Fallback')}"
)


# ============================================================
# RAZORPAY PAYMENT LINK
# ============================================================

if transaction["recommended_action"] == "PAYMENT_LINK":

    st.html("""
    <div class="razorpay-card">
        <div class="info-title">Razorpay Recovery Action</div>
        <div class="info-subtitle">
            Execute the selected payment-link recovery strategy using Razorpay Test Mode.
        </div>
    </div>
    """)

    st.warning("Razorpay Test Mode — no real customer money is moved.")

    if st.button(
        "Create Razorpay Test Payment Link",
        key=f"razorpay_{transaction['transaction_id']}",
    ):
        try:
            payment_link = create_test_payment_link(
                amount=transaction["amount_at_risk"],
                transaction_id=transaction["transaction_id"],
                customer_id=transaction["customer_id"],
            )

            st.success("Razorpay Test Payment Link created successfully.")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Payment Link ID:** {payment_link['id']}")
                st.write(f"**Status:** {payment_link['status']}")
                st.write(f"**Reference:** {payment_link['reference_id']}")

            with col2:
                st.link_button(
                    "Open Razorpay Test Payment Link",
                    payment_link["short_url"],
                )

        except Exception as e:
            st.error(f"Unable to create Razorpay payment link: {e}")


# ============================================================
# CUSTOMER MESSAGE
# ============================================================

st.write("")

st.html("""
<div class="info-card">
    <div class="info-title">Customer Recovery Message</div>
    <div class="info-subtitle">
        Customer-facing communication generated by RecoverAI.
    </div>
</div>
""")

ai_message = transaction.get("ai_customer_message")

if pd.isna(ai_message):
    st.warning("Customer message is not available.")
else:
    st.info(ai_message)

st.caption(
    "Message source: "
    f"{transaction.get('message_source', 'Local Fallback')}"
)


# ============================================================
# RECOVERY RESULT
# ============================================================

st.write("")

st.html("""
<div class="info-card">
    <div class="info-title">Recovery Result</div>
    <div class="info-subtitle">
        Current outcome of the recovery attempt.
    </div>
</div>
""")

col1, col2, col3 = st.columns(3)

with col1:
    status = status_labels.get(
        transaction["recovery_status"],
        transaction["recovery_status"],
    )
    st.metric("Recovery Status", status)

with col2:
    st.metric(
        "Recovered Amount",
        f"₹{transaction['recovered_amount']:,.2f}",
    )

with col3:
    st.metric("Audit Status", "Recorded")


# ============================================================
# AUDITABILITY
# ============================================================

st.write("")

st.html("""
<div class="audit-card">
    <div class="info-title">Recovery Auditability</div>
    <div class="info-subtitle">
        Trace the decision from transaction analysis through intervention and outcome.
    </div>

    <div class="timeline">
        <div class="timeline-step">1. Transaction detected</div>
        <div class="timeline-arrow">→</div>
        <div class="timeline-step">2. AI analyzed</div>
        <div class="timeline-arrow">→</div>
        <div class="timeline-step">3. Action selected</div>
        <div class="timeline-arrow">→</div>
        <div class="timeline-step">4. Recovery executed</div>
        <div class="timeline-arrow">→</div>
        <div class="timeline-step">5. Audit recorded</div>
    </div>
</div>
""")

st.write(f"**Transaction:** {transaction['transaction_id']}")
st.write(f"**Decision:** {action}")
st.write("**Audit Status:** RECORDED")


# ============================================================
# RAZORPAY AUDIT DATA
# ============================================================

razorpay_file = "razorpay_payment_links.csv"

if os.path.exists(razorpay_file):
    try:
        razorpay_df = pd.read_csv(razorpay_file)

        if "transaction_id" in razorpay_df.columns:
            matching = razorpay_df[
                razorpay_df["transaction_id"] == transaction["transaction_id"]
            ]

            if not matching.empty:
                rp = matching.iloc[-1]

                st.write(
                    "**Razorpay Payment Link ID:** "
                    f"{rp.get('payment_link_id', '')}"
                )

                st.write(
                    "**Razorpay Status:** "
                    f"{rp.get('payment_link_status', '')}"
                )

                url = rp.get("payment_link_url", "")

                if isinstance(url, str) and url.strip():
                    st.link_button(
                        "Open Recorded Razorpay Link",
                        url,
                    )

    except Exception:
        pass


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.html("""
<div class="footer">
    RecoverAI Prototype • Synthetic transaction data •
    Recovery outcomes are simulated for evaluation •
    Razorpay integration demonstrated in Test Mode
</div>
""")
