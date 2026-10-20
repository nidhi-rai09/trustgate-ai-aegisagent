
import json
from datetime import datetime, timezone
from pathlib import Path


PASSPORT_PATH = Path(__file__).parent / "trust_passport.json"


def load_passport():
    with PASSPORT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def passport_is_valid(passport):
    if not isinstance(passport, dict):
        return False

    if passport.get("status") != "active":
        return False

    for field in ("passport_id", "task_id"):
        value = passport.get(field)

        if not isinstance(value, str) or not value.strip():
            return False

    expiry_text = passport.get("expires_at")

    if not isinstance(expiry_text, str):
        return False

    try:
        expiry = datetime.fromisoformat(
            expiry_text.replace("Z", "+00:00")
        )
    except ValueError:
        return False

    if expiry.tzinfo is None:
        return False

    if datetime.now(timezone.utc) >= expiry:
        return False

    return isinstance(passport.get("permissions"), dict)


def permission_decision(value):
    if value is True:
        return "ALLOW"

    if isinstance(value, str) and value == "review":
        return "REVIEW"

    return "BLOCK"


def check_action(action, resource, student_id=None):
    if not isinstance(action, str):
        return "BLOCK"

    if not isinstance(resource, str) or not resource:
        return "BLOCK"

    try:
        passport = load_passport()
    except (OSError, ValueError):
        return "BLOCK"

    if not passport_is_valid(passport):
        return "BLOCK"

    permissions = passport["permissions"]

    if action == "read_file":
        allowed_files = permissions.get("read_file")

        if not isinstance(allowed_files, list):
            return "BLOCK"

        if not all(isinstance(item, str) for item in allowed_files):
            return "BLOCK"

        return "ALLOW" if resource in allowed_files else "BLOCK"

    student_actions = {
        "read_student",
        "update_phone",
        "delete_student",
    }

    if action not in student_actions:
        return "BLOCK"

    allowed_resources = passport.get("allowed_student_resources")

    if not isinstance(allowed_resources, list):
        return "BLOCK"

    if not all(isinstance(item, str) for item in allowed_resources):
        return "BLOCK"

    if resource not in allowed_resources:
        return "BLOCK"

    if action == "delete_student":
        if type(student_id) is not int or student_id <= 0:
            return "BLOCK"

        protected_ids = passport.get("protected_student_ids")

        if not isinstance(protected_ids, list):
            return "BLOCK"

        if not all(type(item) is int for item in protected_ids):
            return "BLOCK"

        if student_id in protected_ids:
            return "BLOCK"

    return permission_decision(permissions.get(action))


if __name__ == "__main__":
    scenarios = [
        (
            "Read authorised file",
            "read_file",
            "authorised_notes.txt",
            None,
        ),
        (
            "Read unauthorised file",
            "read_file",
            "secret.txt",
            None,
        ),
        (
            "Read student record",
            "read_student",
            "students",
            None,
        ),
        (
            "Update phone number",
            "update_phone",
            "students",
            None,
        ),
        (
            "Delete protected student",
            "delete_student",
            "students",
            2,
        ),
        (
            "Unknown action",
            "hack_system",
            "system",
            None,
        ),
    ]

    for label, action, resource, student_id in scenarios:
        decision = check_action(
            action,
            resource,
            student_id=student_id,
        )
        print(f"{label}: {decision}")
