import streamlit as st
import pandas as pd
from razorpay_integration import create_test_payment_link


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RecoverAI | Revenue Recovery",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero-title {
    font-size: 38px;
    font-weight: 750;
    color: #173b73;
    margin-bottom: 0;
}

.hero-subtitle {
    font-size: 16px;
    color: #667085;
    margin-top: 2px;
    margin-bottom: 15px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #172033;
    margin-top: 20px;
    margin-bottom: 12px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD MAIN DATA
# ============================================================

try:

    df = pd.read_csv(
        "recoverai_final_results.csv"
    )

except FileNotFoundError:

    st.error(
        "recoverai_final_results.csv was not found."
    )

    st.info(
        "Run: python run_recoverai.py"
    )

    st.stop()


# ============================================================
# LOAD AI RESULTS
# ============================================================

try:

    ai_df = pd.read_csv(
        "ai_results.csv"
    )

except FileNotFoundError:

    st.error(
        "ai_results.csv was not found."
    )

    st.info(
        "Run: python generate_ai_results.py"
    )

    st.stop()


# ============================================================
# MERGE AI RESULTS
# ============================================================

df = df.merge(
    ai_df,
    on="transaction_id",
    how="left"
)


# ============================================================
# CALCULATE KPIs
# ============================================================

total_transactions = len(df)

total_at_risk = (
    df["amount_at_risk"].sum()
)

total_recovered = (
    df["recovered_amount"].sum()
)

recovery_rate = (

    total_recovered /
    total_at_risk *
    100

    if total_at_risk > 0

    else 0

)

successful = (
    df["recovery_status"]
    == "RECOVERED"
).sum()

failed = (
    df["recovery_status"]
    == "FAILED"
).sum()

escalated = (
    df["recovery_status"]
    == "ESCALATED"
).sum()

manual_review = (
    df["recovery_status"]
    == "MANUAL_REVIEW"
).sum()


# ============================================================
# FRIENDLY ACTION LABELS
# ============================================================

action_labels = {

    "STOP_AND_ESCALATE":
        "Stop & Escalate",

    "CUSTOMER_PROMPT":
        "Customer Prompt",

    "PAYMENT_LINK":
        "Payment Link",

    "MANUAL_REVIEW":
        "Manual Review",

    "RETRY":
        "Retry",

    "REMINDER":
        "Reminder"
}


status_labels = {

    "RECOVERED":
        "Recovered",

    "FAILED":
        "Failed",

    "ESCALATED":
        "Escalated",

    "MANUAL_REVIEW":
        "Manual Review"
}


# ============================================================
# DISPLAY DATA
# ============================================================

display_df = df.copy()


display_df[
    "recommended_action_display"
] = (

    display_df[
        "recommended_action"
    ]

    .map(action_labels)

    .fillna(
        display_df[
            "recommended_action"
        ]
    )

)


display_df[
    "recovery_status_display"
] = (

    display_df[
        "recovery_status"
    ]

    .map(status_labels)

    .fillna(
        display_df[
            "recovery_status"
        ]
    )

)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">RecoverAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'AI-Powered Payment Revenue Recovery Operations'
    '</div>',
    unsafe_allow_html=True
)

st.success(
    "● System Active"
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Recovery Performance'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Revenue at Risk",
        f"₹{total_at_risk:,.0f}"
    )

    st.caption(
        "Total failed payment value"
    )


with col2:

    st.metric(
        "Revenue Recovered",
        f"₹{total_recovered:,.0f}"
    )

    st.caption(
        "Simulated recovery"
    )


with col3:

    st.metric(
        "Recovery Rate",
        f"{recovery_rate:.2f}%"
    )

    st.caption(
        "Recovered / revenue at risk"
    )


with col4:

    st.metric(
        "Successful Recoveries",
        f"{successful:,}"
    )

    st.caption(
        "Payments recovered"
    )


# ============================================================
# SECONDARY METRICS
# ============================================================

st.write("")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Transactions Analyzed",
        f"{total_transactions:,}"
    )


with col2:

    st.metric(
        "Escalated Cases",
        f"{escalated:,}"
    )


with col3:

    st.metric(
        "Failed Recoveries",
        f"{failed:,}"
    )


with col4:

    st.metric(
        "Manual Reviews",
        f"{manual_review:,}"
    )


st.divider()


# ============================================================
# RECOVERY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Recovery Overview'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# RISK DISTRIBUTION
# ============================================================

with col1:

    st.subheader(
        "Recovery Risk"
    )

    risk_counts = (

        df[
            "recovery_risk"
        ]

        .value_counts()

        .reindex(
            [
                "HIGH",
                "MEDIUM",
                "LOW"
            ]
        )

        .fillna(0)

        .astype(int)

    )

    st.bar_chart(
        risk_counts
    )


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

with col2:

    st.subheader(
        "Recommended Actions"
    )

    action_counts = (

        display_df[
            "recommended_action_display"
        ]

        .value_counts()

    )

    st.bar_chart(
        action_counts
    )


# ============================================================
# RECOVERY OUTCOMES
# ============================================================

st.subheader(
    "Recovery Outcomes"
)


outcome_counts = (

    display_df[
        "recovery_status_display"
    ]

    .value_counts()

)


st.bar_chart(
    outcome_counts
)


st.divider()


# ============================================================
# RECOVERY QUEUE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Recovery Queue'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTERS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    risk_filter = st.multiselect(

        "Risk",

        [
            "HIGH",
            "MEDIUM",
            "LOW"
        ],

        default=[
            "HIGH",
            "MEDIUM",
            "LOW"
        ]

    )


with col2:

    priority_filter = st.multiselect(

        "Priority",

        [
            "HIGH",
            "MEDIUM",
            "LOW"
        ],

        default=[
            "HIGH",
            "MEDIUM",
            "LOW"
        ]

    )


with col3:

    action_options = list(
        action_labels.values()
    )

    action_filter = st.multiselect(

        "Recovery Action",

        action_options,

        default=action_options

    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = display_df[

    display_df[
        "recovery_risk"
    ].isin(
        risk_filter
    )

    &

    display_df[
        "priority"
    ].isin(
        priority_filter
    )

    &

    display_df[
        "recommended_action_display"
    ].isin(
        action_filter
    )

]


st.caption(
    f"Showing {len(filtered):,} "
    f"of {len(df):,} transactions"
)


# ============================================================
# QUEUE TABLE
# ============================================================

queue_columns = [

    "transaction_id",

    "customer_id",

    "amount_at_risk",

    "failure_reason",

    "recovery_score",

    "recovery_risk",

    "priority",

    "recommended_action_display",

    "recovery_status_display"

]


queue = filtered[
    queue_columns
].rename(

    columns={

        "transaction_id":
            "Transaction",

        "customer_id":
            "Customer",

        "amount_at_risk":
            "Amount at Risk",

        "failure_reason":
            "Failure Reason",

        "recovery_score":
            "Recovery Score",

        "recovery_risk":
            "Risk",

        "priority":
            "Priority",

        "recommended_action_display":
            "Recommended Action",

        "recovery_status_display":
            "Status"

    }

)


st.dataframe(

    queue,

    use_container_width=True,

    hide_index=True,

    height=420

)


st.divider()


# ============================================================
# TRANSACTION INVESTIGATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Transaction Investigation'
    '</div>',
    unsafe_allow_html=True
)


if len(filtered) == 0:

    st.warning(
        "No transactions match the selected filters."
    )

else:

    selected_id = st.selectbox(

        "Select a transaction",

        filtered[
            "transaction_id"
        ].tolist()

    )


    transaction = df[
        df["transaction_id"]
        == selected_id
    ].iloc[0]


    # ========================================================
    # PAYMENT DETAILS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Payment Details"
        )

        st.write(
            f"**Transaction:** "
            f"{transaction['transaction_id']}"
        )

        st.write(
            f"**Customer:** "
            f"{transaction['customer_id']}"
        )

        st.write(
            f"**Amount at Risk:** "
            f"₹{transaction['amount_at_risk']:,.2f}"
        )

        st.write(
            f"**Failure Reason:** "
            f"{transaction['failure_reason']}"
        )

        st.write(
            f"**Previous Attempts:** "
            f"{transaction['attempts']}"
        )


    # ========================================================
    # RECOVERAI DECISION
    # ========================================================

    with col2:

        st.subheader(
            "RecoverAI Decision"
        )

        st.write(
            f"**Recovery Score:** "
            f"{transaction['recovery_score']}/100"
        )

        st.write(
            f"**Recovery Risk:** "
            f"{transaction['recovery_risk']}"
        )

        st.write(
            f"**Priority Score:** "
            f"{transaction['priority_score']}/100"
        )

        st.write(
            f"**Priority:** "
            f"{transaction['priority']}"
        )


        action = action_labels.get(

            transaction[
                "recommended_action"
            ],

            transaction[
                "recommended_action"
            ]

        )


        st.write(
            f"**Recommended Action:** "
            f"{action}"
        )


    # ========================================================
    # AI DECISION EXPLANATION
    # ========================================================

    st.subheader(
        "Why did RecoverAI choose this?"
    )


    ai_explanation = transaction[
        "ai_decision_explanation"
    ]


    if pd.isna(ai_explanation):

        st.warning(
            "AI explanation is not available."
        )

    else:

        st.info(
            ai_explanation
        )


    # ========================================================
    # AI SOURCE
    # ========================================================

    explanation_source = transaction[
        "explanation_source"
    ]


    st.caption(
        f"Explanation source: "
        f"{explanation_source}"
    )

    # ========================================================
# RAZORPAY TEST PAYMENT LINK
# ========================================================

if transaction["recommended_action"] == "PAYMENT_LINK":

    st.subheader(
        "Razorpay Recovery Payment Link"
    )

    st.write(
        "RecoverAI selected PAYMENT_LINK as the "
        "recommended recovery action."
    )

    if st.button(
        "Create Razorpay Test Payment Link",
        key=f"razorpay_{transaction['transaction_id']}"
    ):

        try:

            payment_link = create_test_payment_link(

                amount=transaction["amount_at_risk"],

                transaction_id=transaction[
                    "transaction_id"
                ],

                customer_id=transaction[
                    "customer_id"
                ]

            )

            st.success(
                "Razorpay Test Payment Link created successfully."
            )

            st.write(
                f"**Payment Link ID:** "
                f"{payment_link['id']}"
            )

            st.write(
                f"**Status:** "
                f"{payment_link['status']}"
            )

            st.link_button(
                "Open Razorpay Test Payment Link",
                payment_link["short_url"]
            )

        except Exception as e:

            st.error(
                f"Unable to create Razorpay payment link: {e}"
            )
    # ========================================================
    # CUSTOMER MESSAGE
    # ========================================================

    st.subheader(
        "Customer Recovery Message"
    )


    ai_message = transaction[
        "ai_customer_message"
    ]


    if pd.isna(ai_message):

        st.warning(
            "Customer message is not available."
        )

    else:

        st.info(
            ai_message
        )


    # ========================================================
    # MESSAGE SOURCE
    # ========================================================

    message_source = transaction[
        "message_source"
    ]


    st.caption(
        f"Message source: "
        f"{message_source}"
    )


    # ========================================================
    # RECOVERY RESULT
    # ========================================================

    st.subheader(
        "Recovery Result"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        status = status_labels.get(

            transaction[
                "recovery_status"
            ],

            transaction[
                "recovery_status"
            ]

        )

        st.metric(
            "Recovery Status",
            status
        )


    with col2:

        st.metric(

            "Recovered Amount",

            f"₹{transaction['recovered_amount']:,.2f}"

        )


    with col3:

        st.metric(
            "Audit Status",
            "Recorded"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "RecoverAI Prototype • Synthetic transaction data • "
    "Recovery outcomes are simulated for evaluation"
)