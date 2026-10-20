import streamlit as st
import json
from pathlib import Path

from firewall import check_action
from database import (
    create_audit_table,
    log_action,
    get_audit_logs
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="TRUSTGATE AI",
    page_icon="🛡️",
    layout="wide"
)

# Create the audit table if it does not exist
create_audit_table()

# -----------------------------
# Application Header
# -----------------------------
st.title("🛡️ TRUSTGATE AI")

st.subheader(
    "AegisAgent — Real-Time AI Safety Firewall"
)

st.markdown("""
Monitor and evaluate AI-agent actions using a
**Task-Bound Trust Passport**.

TRUSTGATE AI evaluates actions against predefined security
policies and records the resulting decisions.
""")

# -----------------------------
# Load Trust Passport
# -----------------------------
passport_path = Path(__file__).parent / "trust_passport.json"

with open(passport_path, "r", encoding="utf-8") as file:
    passport = json.load(file)

# -----------------------------
# Sidebar: Trust Passport
# -----------------------------
st.sidebar.header("🔐 Trust Passport")

st.sidebar.write(
    "**Passport ID:**",
    passport["passport_id"]
)

st.sidebar.write(
    "**Task ID:**",
    passport["task_id"]
)

st.sidebar.write(
    "**Status:**",
    passport["status"]
)

st.sidebar.divider()

st.sidebar.caption(
    "Permissions are evaluated using the configured "
    "Trust Passport policy."
)

# -----------------------------
# Security Overview
# -----------------------------
st.divider()

st.header("📊 Security Overview")

audit_logs = get_audit_logs()

total_actions = len(audit_logs)

allowed_actions = sum(
    1 for row in audit_logs
    if row[2] == "ALLOW"
)

review_actions = sum(
    1 for row in audit_logs
    if row[2] == "REVIEW"
)

blocked_actions = sum(
    1 for row in audit_logs
    if row[2] == "BLOCK"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Actions",
    total_actions
)

col2.metric(
    "✅ Allowed",
    allowed_actions
)

col3.metric(
    "⚠️ Under Review",
    review_actions
)

col4.metric(
    "🚫 Blocked",
    blocked_actions
)

# -----------------------------
# Test an AI Agent Action
# -----------------------------
st.divider()

st.header("🧪 Test an AI Agent Action")

action_choice = st.selectbox(
    "Choose an action to test",
    [
        "Read authorised file",
        "Read unauthorised file",
        "Read student record",
        "Update phone number",
        "Delete protected student",
        "Unknown action"
    ]
)

if st.button("🛡️ Evaluate Action", type="primary"):

    # Evaluate the selected action
    if action_choice == "Read authorised file":

        decision = check_action(
            "read_file",
            "authorised_notes.txt"
        )

    elif action_choice == "Read unauthorised file":

        decision = check_action(
            "read_file",
            "secret.txt"
        )

    elif action_choice == "Read student record":

        decision = check_action(
            "read_student",
            "students"
        )

    elif action_choice == "Update phone number":

        decision = check_action(
            "update_phone",
            "students"
        )

    elif action_choice == "Delete protected student":

        decision = check_action(
            "delete_student",
            "students",
            student_id=2
        )

    else:

        decision = check_action(
            "hack_system",
            "system"
        )

    # Display the firewall decision
    if decision == "ALLOW":

        st.success(
            "✅ ALLOW — The action is permitted by the current policy."
        )

    elif decision == "REVIEW":

        st.warning(
            "⚠️ REVIEW — Human approval is required."
        )

    else:

        st.error(
            "🚫 BLOCK — The action is not permitted."
        )

    st.write(
        "**Action tested:**",
        action_choice
    )

    st.write(
        "**Firewall decision:**",
        decision
    )

    # Record the decision in the audit log
    log_action(
        action_choice,
        decision
    )

    # Refresh the page so the summary and audit log update
    st.rerun()

# -----------------------------
# Security Audit Log
# -----------------------------
st.divider()

st.header("📋 Security Audit Log")

audit_logs = get_audit_logs()

if audit_logs:

    st.dataframe(
        [
            {
                "ID": row[0],
                "Action": row[1],
                "Decision": row[2],
                "Timestamp": row[3]
            }
            for row in audit_logs
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No actions have been recorded yet. "
        "Test an action to create your first audit entry."
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "TRUSTGATE AI | AegisAgent | Task-Bound Trust Passport"
)

st.caption(
    "MVP demonstration: policy evaluation and audit logging. "
    "Real external agent operations are not executed by this demo."
)