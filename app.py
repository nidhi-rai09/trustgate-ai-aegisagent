import streamlit as st
import json
from pathlib import Path
from firewall import check_action
from database import create_audit_table, log_action, get_audit_logs
st.set_page_config(
    page_title="TRUSTGATE AI",
    page_icon="🛡️",
    layout="wide"
)
create_audit_table()
st.title("🛡️ TRUSTGATE AI")
st.subheader("AegisAgent — Real-Time AI Safety Firewall")

st.markdown("""
Monitor and evaluate AI-agent actions using a
**Task-Bound Trust Passport**.
""")

# Load the trust passport
with open(Path(__file__).parent / "trust_passport.json", "r") as file:
    passport = json.load(file)

# Sidebar
st.sidebar.header("🔐 Trust Passport")
st.sidebar.write("Passport ID:", passport["passport_id"])
st.sidebar.write("Task ID:", passport["task_id"])
st.sidebar.write("Status:", passport["status"])

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

if st.button("🛡️ Evaluate Action"):
    if action_choice == "Read authorised file":
        decision = check_action("read_file", "authorised_notes.txt")

    elif action_choice == "Read unauthorised file":
        decision = check_action("read_file", "secret.txt")

    elif action_choice == "Read student record":
        decision = check_action("read_student", "students")

    elif action_choice == "Update phone number":
        decision = check_action("update_phone", "students")

    elif action_choice == "Delete protected student":
        decision = check_action(
            "delete_student",
            "students",
            student_id=2
        )

    else:
        decision = check_action("hack_system", "system")

    if decision == "ALLOW":
        st.success("✅ ALLOW — The action is permitted by the current policy.")
    elif decision == "REVIEW":
        st.warning("⚠️ REVIEW — Human approval is required.")
    else:
        st.error("🚫 BLOCK — The action is not permitted.")

    st.write("**Action tested:**", action_choice)
    st.write("**Firewall decision:**", decision)

    log_action(action_choice, decision)

st.divider()

st.caption(
    "TRUSTGATE AI | AegisAgent | Task-Bound Trust Passport"
)
st.divider()

st.header("📋 Security Audit Log")

audit_logs = get_audit_logs()

if audit_logs:
    st.table([
        {
            "ID": row[0],
            "Action": row[1],
            "Decision": row[2],
            "Timestamp": row[3]
        }
        for row in audit_logs
    ])
else:
    st.info("No actions have been recorded yet.")
