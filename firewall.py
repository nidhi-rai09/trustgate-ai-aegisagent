import json
from pathlib import Path

# Load the Task-Bound Trust Passport
PASSPORT_PATH = Path(__file__).parent / "trust_passport.json"


def load_passport():
    with open(PASSPORT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_action(action, resource, student_id=None):
    passport = load_passport()
    permissions = passport["permissions"]

    # Check file access
    if action == "read_file":
        if resource in permissions["read_file"]:
            return "ALLOW"
        return "BLOCK"

    # Check student record access
    elif action == "read_student":
        if permissions["read_student"]:
            return "ALLOW"
        return "BLOCK"

    # Check database update
    elif action == "update_phone":
        if permissions["update_phone"] == "review":
            return "REVIEW"
        elif permissions["update_phone"] is True:
            return "ALLOW"
        return "BLOCK"

    # Prevent deletion of protected records
    elif action == "delete_student":
        protected_ids = passport["protected_student_ids"]

        if student_id in protected_ids:
            return "BLOCK"

        if permissions["delete_student"]:
            return "ALLOW"

        return "BLOCK"

    # Unknown actions are denied by default
    return "BLOCK"


# Quick demonstration
if __name__ == "__main__":
    print("TRUSTGATE AI — AegisAgent Firewall")
    print("----------------------------------")

    print(
        "Read authorised file:",
        check_action("read_file", "authorised_notes.txt")
    )

    print(
        "Update phone number:",
        check_action("update_phone", "student_records")
    )

    print(
        "Delete protected record:",
        check_action("delete_student", "student_records", student_id=2)
    )
