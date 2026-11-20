import frappe

# subject key -> field whose options list the team members
TEAM_FIELD = [
    ("technical deployment", "custom_assigned_pmo"),
    ("invoice generation", "custom_account_owner"),
    ("customer feedback", "custom_assigned_cet"),
]
BYPASS_ROLES = {"Project Editor"}


def _team_users(fieldname):
    df = frappe.get_meta("Task").get_field(fieldname)
    return {o.strip().lower() for o in (df.options or "").split("\n") if o.strip()}


def has_permission(doc, ptype=None, user=None, debug=False):
    # only restrict editing and deleting; None means "no opinion"
    if ptype not in ("write", "delete"):
        return None

    user = user or frappe.session.user
    if user == "Administrator" or doc.is_new():
        return None
    if BYPASS_ROLES & set(frappe.get_roles(user)):
        return None

    subject = (doc.subject or "").lower()
    field = next((f for key, f in TEAM_FIELD if key in subject), None)
    if not field:
        return None          # not a team task, so the normal rules apply

    if user.lower() in _team_users(field):
        return None
    return False
