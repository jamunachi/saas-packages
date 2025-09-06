from . import __version__ as app_version

app_name = "saas_packages"
app_title = "SaaS Packages"
app_publisher = "Your Company"
app_description = "Package-based feature toggling + per-site provisioning"
app_email = "dev@yourco.com"
app_license = "MIT"

website_route_rules = [{"from_route": "/plans", "to_route": "plans"}]

def _get_allowed_origins():
    try:
        import frappe
        if getattr(frappe.local, "site", None):
            settings = frappe.get_single("SaaS Settings")
            if settings and settings.allowed_origins:
                return [o.strip() for o in settings.allowed_origins.split("\n") if o.strip()]
    except Exception:
        pass
    return []

allow_cors = _get_allowed_origins

scheduler_events = {
    "daily": ["saas_packages.utils.handle_plan_expiry"],
}
