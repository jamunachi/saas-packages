import frappe
from frappe.utils import nowdate

def get_customer_users(customer: str):
<<<<<<< HEAD
    # Expect a custom Link field 'company' on User pointing to Company
=======
>>>>>>> fe44143 (Flatten repo: move app to repo root (app dir = saas_packages))
    return frappe.get_all("User", filters={"company": customer, "enabled": 1}, fields=["name"])

def get_managed_roles():
    settings = frappe.get_single("SaaS Settings")
    rows = getattr(settings, "managed_roles", []) or []
    roles = {r.role for r in rows if getattr(r, "role", None)}
    if not roles:
<<<<<<< HEAD
        roles = {"Accounts User", "Accounts Manager", "HR User", "HR Manager",
                 "Sales User", "Sales Manager", "Projects User", "Projects Manager",
                 "Manufacturing User", "Manufacturing Manager"}
=======
        roles = {"Accounts User", "Accounts Manager", "HR User", "HR Manager"}
>>>>>>> fe44143 (Flatten repo: move app to repo root (app dir = saas_packages))
    return roles

def apply_roles_to_user(user: str, roles_to_keep: set):
    managed_roles = get_managed_roles()
    ur = frappe.get_doc("User", user)
    ur.roles = [r for r in ur.roles if r.role not in managed_roles]
    base = getattr(frappe.get_single("SaaS Settings"), "base_role", None)
    existing = {r.role for r in ur.roles}
    if base and base not in existing:
        ur.append("roles", {"role": base})
        existing.add(base)
    for role in roles_to_keep:
        if role not in existing:
            ur.append("roles", {"role": role})
    ur.save(ignore_permissions=True)

def get_package_roles(pkg_doc):
    return {r.role for r in pkg_doc.get("granted_roles")}

def handle_plan_expiry():
    expired = frappe.get_all(
        "Customer Plan",
        filters={"status": ["in", ["Active", "Trial"]], "expires_on": ["<", nowdate()]},
        fields=["name"]
    )
    for p in expired:
        doc = frappe.get_doc("Customer Plan", p.name)
        doc.status = "Past Due"
        doc.save(ignore_permissions=True)
