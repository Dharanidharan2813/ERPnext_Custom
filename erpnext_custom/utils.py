import frappe

def check_vip_customer(doc, method):
    if not doc.customer:
        return
    try:
        customer = frappe.get_doc("Customer", doc.customer)

        if getattr(customer, "custom_is_vip_customer", 0) == 1:
            increment_count("vip_sales_count")
        else:
            increment_count("normal_sales_count")

    except Exception:
        frappe.log_error(frappe.get_traceback(), "VIP/Normal Customer Check Error")


def increment_count(fieldname):
    try:
        if not frappe.db.has_column("System Settings", fieldname):
            return  
        current = frappe.db.get_single_value("System Settings", fieldname) or 0
        frappe.db.set_value("System Settings", "System Settings", fieldname, current + 1)

    except Exception:
        pass
