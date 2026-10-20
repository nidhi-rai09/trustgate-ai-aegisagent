# TrustGate AI — AegisAgent

### Permission With Purpose for Every AI Action

A Python-based hackathon prototype exploring real-time safety checks for AI agent actions using Task-Bound Trust Passports.

## Problem Statement

AI agents can interact with tools, APIs, and data, but broad permissions may allow actions beyond the user's intended task. This creates risks of unauthorized access, unintended changes, and tool misuse.

TrustGate AI explores task-specific permissions and a safety checkpoint before action execution.

## Solution Overview

AegisAgent evaluates proposed actions against a Task-Bound Trust Passport.

The intended decision flow is:

- **Allow:** The action is permitted for the current task.
- **Human Approval:** The action requires explicit authorization before execution.
- **Block:** The action is outside the permitted scope.

Audit records provide visibility into decisions and their reasons.

## Core Innovation: Task-Bound Trust Passport

The Trust Passport represents the permission boundary for a specific task.

The project design includes:

- Allowed tools and actions.
- Permitted data and resource scope.
- Access expiry.
- Human approval requirements.

See `trust_passport.json` for the configuration used by this prototype. The fields and checks implemented in the source code determine the permissions actually enforced.

## System Workflow

1. Configure the task-specific Trust Passport.
2. Submit a proposed agent action.
3. Evaluate the action against the configured permissions.
4. Allow, request human approval, or block according to the implemented rules.
5. Record the decision and its reason.

Only permitted actions—or sensitive actions after approval—should proceed to execution. Blocked actions must stop.

## Repository Structure

| File | Purpose |
|---|---|
| `app.py` | Application entry point and dashboard |
| `firewall.py` | Safety-checking and action-decision logic |
| `database.py` | Database-related functionality |
| `trust_passport.json` | Trust Passport configuration |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from version control |

## Quick Setup

### Prerequisites

- Python 3
- pip
- Git, if using the clone command below

### 1. Download the Project

```bash
git clone [https://github.com/nidhi-rai09/trustgate-ai-aegisagent.git](https://github.com/nidhi-rai09/trustgate-ai-aegisagent.git)
cd trustgate-ai-aegisagent
```

Alternatively, download the repository ZIP from GitHub and extract it.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```bash
.venvScriptsactivate.bat
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

These instructions assume `app.py` is the Streamlit entry point and `requirements.txt` contains the required dependencies.

## Demo Walkthrough

Use the actions and controls available in the application:

1. Review the configured Trust Passport.
2. Submit an action permitted by that configuration.
3. Submit an action outside the permitted scope.
4. Inspect the displayed decision and explanation.
5. Review human approval controls and audit records where implemented.

Verify approval and expiry behavior against the current code and configuration.

A displayed decision alone is not proof that an external tool action was executed or prevented.

## Prototype Status and Limitations

This repository is a hackathon prototype, not a production security product.

- The source code and running demonstration define the implemented functionality.
- Live LLM, email, payment, or enterprise API integrations should not be assumed.
- Mock integrations and simulated actions must be identified during the demonstration.
- Enforcement depends on tool requests passing through the security layer.
- The prototype does not guarantee protection against every prompt-injection attack, unauthorized action, or data leak.
- No independently validated security benchmarks or percentage improvements are claimed.

## Future Scope

- Integration with live AI agents and external tools.
- Stronger resource-level authorization.
- Signed, tamper-resistant Trust Passports.
- Expanded approval and revocation workflows.
- Automated security and regression tests.
- Multi-user and multi-tenant support.

## Security

Do not commit passwords, API keys, access tokens, or real personal data.

Use synthetic data for testing and demonstrations.