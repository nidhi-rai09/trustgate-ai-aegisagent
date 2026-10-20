



import json
from pathlib import Path

import streamlit as st

from database import create_audit_table, get_audit_logs, log_action
from firewall import check_action


st.set_page_config(
    page_title="TRUSTGATE AI",
    page_icon="🛡️",
    layout="wide",
)

PASSPORT_PATH = Path(__file__).parent / "trust_passport.json"

try:
    with PASSPORT_PATH.open("r", encoding="utf-8") as file:
        passport = json.load(file)

    if not isinstance(passport, dict):
        raise ValueError("The passport must be a JSON object.")

except (OSError, ValueError) as exc:
    st.error("Unable to load a valid trust_passport.json.")
    st.code(str(exc))
    st.stop()

try:
    create_audit_table()
    audit_logs = list(get_audit_logs())
except Exception as exc:
    st.error("Unable to initialize or read the audit database.")
    st.code(str(exc))
    st.stop()


st.title("🛡️ TRUSTGATE AI")
st.subheader("AegisAgent — AI Action Safety Dashboard")

st.write(
    "Evaluate proposed actions against a Task-Bound Trust Passport "
    "and record each policy decision."
)

st.info(
    "MVP demonstration: predefined requests and policy evaluation. "
    "No real external agent operations are executed."
)


# Passport configuration
st.sidebar.header("🔐 Trust Passport")

for label, key in [
    ("Passport ID", "passport_id"),
    ("Task ID", "task_id"),
    ("Status", "status"),
    ("Expires at", "expires_at"),
]:
    st.sidebar.write(
        f"{label}:",
        passport.get(key, "Not specified"),
    )

with st.sidebar.expander("View configuration"):
    st.json(passport)

st.sidebar.caption(
    "The firewall reloads this configuration for each request. "
    "Expiry is checked using the server clock."
)


# Metrics
st.divider()
st.header("📊 Security Overview")

columns = st.columns(4)

columns[0].metric("Total Actions", len(audit_logs))
columns[1].metric(
    "✅ Allowed",
    sum(row[2] == "ALLOW" for row in audit_logs),
)
columns[2].metric(
    "⚠️ Flagged for Review",
    sum(row[2] == "REVIEW" for row in audit_logs),
)
columns[3].metric(
    "🚫 Blocked",
    sum(row[2] == "BLOCK" for row in audit_logs),
)


# Test scenarios
st.divider()
st.header("🧪 Test an AI Agent Action")

scenarios = {
    "Read authorised file": (
        "read_file",
        "authorised_notes.txt",
        {},
    ),
    "Read unauthorised file": (
        "read_file",
        "secret.txt",
        {},
    ),
    "Read student record": (
        "read_student",
        "students",
        {},
    ),
    "Update phone number": (
        "update_phone",
        "students",
        {},
    ),
    "Delete protected student": (
        "delete_student",
        "students",
        {"student_id": 2},
    ),
    "Unknown action": (
        "hack_system",
        "system",
        {},
    ),
}

selected = st.selectbox(
    "Choose a request",
    list(scenarios),
)

if st.button("🛡️ Evaluate Action", type="primary"):
    st.session_state.pop("last_result", None)

    action, resource, extra = scenarios[selected]

    try:
        decision = check_action(action, resource, **extra)

        if decision not in ("ALLOW", "REVIEW", "BLOCK"):
            raise ValueError("Unexpected firewall decision.")

        log_action(selected, decision)

    except Exception as exc:
        st.error(
            "Evaluation or audit logging failed. "
            "No external operation was executed."
        )
        st.code(str(exc))

    else:
        st.session_state["last_result"] = {
            "action": selected,
            "resource": resource,
            "decision": decision,
        }
        st.rerun()


# Preserve the result after rerunning
result = st.session_state.get("last_result")

if result:
    st.subheader("Latest Evaluation")

    if result["decision"] == "ALLOW":
        st.success(
            "✅ ALLOW — Permitted by the configured policy."
        )
    elif result["decision"] == "REVIEW":
        st.warning(
            "⚠️ REVIEW — Flagged for human review. "
            "No operation has been executed."
        )
    else:
        st.error(
            "🚫 BLOCK — The request is not permitted to proceed."
        )

    st.write("Action:", result["action"])
    st.write("Resource:", result["resource"])
    st.write("Decision:", result["decision"])

    st.caption(
        "This result belongs to the last evaluation. "
        "Evaluate again after changing the passport."
    )


# Audit history
st.divider()
st.header("📋 Security Audit Log")

if audit_logs:
    st.dataframe(
        [
            {
                "ID": row[0],
                "Action": row[1],
                "Decision": row[2],
                "Timestamp (UTC)": row[3],
            }
            for row in audit_logs
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Evaluate a request to create the first audit entry.")


st.divider()
st.caption(
    "TRUSTGATE AI | AegisAgent | Task-Bound Trust Passport"
)
st.caption(
    "Scope: policy evaluation and audit logging. "
    "Passports are preconfigured. Human approval execution, "
    "live LLM integration, and external tool execution "
    "are not implemented in this dashboard."
)
