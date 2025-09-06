from . import __version__ as app_version

app_name = "saas_packages"
app_title = "SaaS Packages"
app_publisher = "Your Company"
<<<<<<< HEAD
app_description = "Package-based feature toggling + per-site provisioning for ERPNext"
=======
app_description = "Package-based feature toggling + per-site provisioning"
>>>>>>> fe44143 (Flatten repo: move app to repo root (app dir = saas_packages))
app_email = "dev@yourco.com"
app_license = "MIT"

website_route_rules = [ {"from_route": "/plans", "to_route": "plans"} ]

def _get_allowed_origins():
    try:
        import frappe
        if frappe.local.site:
            settings = frappe.get_single("SaaS Settings")
            if settings and settings.allowed_origins:
                return [o.strip() for o in settings.allowed_origins.split("\n") if o.strip()]
    except Exception:
        pass
    return []

allow_cors = _get_allowed_origins

<<<<<<< HEAD
fixtures = [
    {"dt": "Role", "filters": [["role_name", "in", [
        "Accounts User", "Accounts Manager",
        "HR User", "HR Manager",
        "Sales User", "Sales Manager",
        "Projects User", "Projects Manager",
        "Manufacturing User", "Manufacturing Manager"
    ]]]},
]

=======
>>>>>>> fe44143 (Flatten repo: move app to repo root (app dir = saas_packages))
scheduler_events = {
    "daily": [
        "saas_packages.utils.handle_plan_expiry"
    ]
}
