import json, os, subprocess
import frappe
from frappe.utils import cstr

@frappe.whitelist()
def provision_site(customer: str, site: str, admin_password: str,
                   domains: list | None = None,
                   install_erpnext: int = 1,
                   country: str | None = None,
                   currency: str | None = None,
                   language: str | None = None,
                   timezone: str | None = None):
    bench = os.getcwd()
    _run(["bench", "new-site", site, "--admin-password", admin_password, "--no-mariadb-socket"], cwd=bench)
    _run(["bench", "--site", site, "install-app", "frappe"], cwd=bench)
    if install_erpnext:
        _run(["bench", "--site", site, "install-app", "erpnext"], cwd=bench)
    try:
        _run(["bench", "--site", site, "install-app", "saas_packages"], cwd=bench)
    except Exception:
        pass

    for k, v in {"country": country, "currency": currency, "language": language, "time_zone": timezone}.items():
        if v:
            _run(["bench", "--site", site, "set-config", k, cstr(v)], cwd=bench)

    domains = domains or []
    if domains:
        code = f"""
import frappe
from frappe.core.doctype.domain_settings.domain_settings import set_active_domains
set_active_domains({domains!r})
frappe.db.commit()
print('Enabled domains:', {domains!r})
"""
        _run(["bench", "--site", site, "execute", "frappe.utils.bench_helper.execute_code", "--kwargs", json.dumps({"code": code})], cwd=bench)

    return {"ok": True, "site": site, "domains": domains}

def _run(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise Exception(f"Command failed: {' '.join(cmd)}\n{res.stderr}")
    return res.stdout
