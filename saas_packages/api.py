import frappe
from frappe import _
from .utils import (
    get_customer_users, apply_roles_to_user, get_package_roles
)

@frappe.whitelist(allow_guest=True)
def get_public_packages():
    pkgs = frappe.get_all(
        "Package",
        filters={"is_active": 1},
        fields=["name as package_name", "description", "monthly_price", "annual_price"]
    )
    return pkgs

@frappe.whitelist()
def set_plan(customer: str, package_name: str):
    pkg = frappe.get_doc("Package", package_name)
    if not pkg.is_active:
        frappe.throw(_("Selected package is not active."))

    plan = frappe.get_doc({
        "doctype": "Customer Plan",
        "customer": customer,
        "package": package_name,
        "status": "Active"
    })
    plan.insert(ignore_permissions=True)

    users = get_customer_users(customer)
    pkg_roles = get_package_roles(pkg)

    for u in users:
        apply_roles_to_user(u.name, pkg_roles)

    frappe.get_doc({
        "doctype": "Plan Assignment",
        "customer": customer,
        "user": users[0].name if users else None,
        "package_snapshot_json": frappe.as_json({
            "roles": list(pkg_roles),
            "workspaces": [w.workspace for w in pkg.get("allowed_workspaces")],
            "doctypes": [d.document_type for d in pkg.get("allowed_doctypes")]
        })
    }).insert(ignore_permissions=True)

    frappe.db.commit()
    return {"ok": True}

@frappe.whitelist(allow_guest=True)
def payment_webhook(session_id: str = None, **payload):
    settings = frappe.get_single("SaaS Settings")
    customer = (payload.get("customer") 
                or payload.get("metadata", {}).get("customer"))
    package_name = (payload.get("package") 
                    or payload.get("metadata", {}).get("package"))
    if not (customer and package_name):
        frappe.throw(_("Missing customer or package in webhook payload."))
    return set_plan(customer=customer, package_name=package_name)
