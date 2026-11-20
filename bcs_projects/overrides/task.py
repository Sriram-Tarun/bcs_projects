import frappe

PREFIXES = [
    ("technical deployment", "BCSPMO"),
    ("invoice generation", "BCSACC"),
    ("customer feedback", "BCSCET"),
]

def autoname(doc, method=None):
    subject = (doc.subject or "").lower()
    prefix = next((p for key, p in PREFIXES if key in subject), None)

    # Other tasks, or tasks without a project, keep the default TASK- series
    if not prefix or not doc.project:
        return

    base = "{}-{}-{}".format(prefix, frappe.utils.nowdate()[:4], doc.project.split("-")[-1])
    n = 1
    while frappe.db.exists("Task", "{}-{:02d}".format(base, n)):
        n += 1
    doc.name = "{}-{:02d}".format(base, n)
