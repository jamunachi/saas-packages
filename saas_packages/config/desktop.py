from frappe import _

def get_data():
    return [
        {
            "label": _("SaaS Packages"),
            "items": [
                {"type": "doctype", "name": "Package", "label": _("Packages")},
                {"type": "doctype", "name": "Customer Plan", "label": _("Customer Plans")},
                {"type": "doctype", "name": "SaaS Settings", "label": _("Settings")}
            ]
        }
    ]
