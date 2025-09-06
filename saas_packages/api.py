import frappe
from frappe import _
from .utils import get_customer_users, apply_roles_to_user, get_package_roles

@frappe.whitelist(allow_guest=True)
def get_public_packages():
    """List active packages for public plan selector."""
    pkgs = frappe.get_all(
        "Package",
        filters={"is_active": 1},
        fields=["name as package_name", "description", "monthly_price", "annual_price"],
    )
    return pkgs

@frappe.whitelist()
def set_plan(customer: str, package_name: str):
    """Apply a package to a customer's users (single-site / role-based)."""
    pkg = frappe.get_doc("Package", package_name)
    if not pkg.is_active:
        frappe.throw(_("Selected package is not active."))

    # record assignment
    plan = frappe.get_doc({
        "doctype": "Customer Plan",
        "customer": customer,
        "package": package_name,
        "status": "Active",
    })
    plan.insert(ignore_permissions=True)

    # apply roles to all users of that customer
    users = get_customer_users(customer)
    pkg_roles = get_package_roles(pkg)
    for u in users:
        apply_roles_to_user(u.name, pkg_roles)

    # snapshot
    frappe.get_doc({
        "doctype": "Plan Assignment",
        "customer": customer,
        "user": users[0].name if users else None,
        "package_snapshot_json": frappe.as_json({
            "roles": sorted(list(pkg_roles)),
            "workspaces": [w.workspace for w in pkg.get("allowed_workspaces")],
            "doctypes": [d.document_type for d in pkg.get("allowed_doctypes")],
        }),
    }).insert(ignore_permissions=True)

    frappe.db.commit()
    return {"ok": True}
