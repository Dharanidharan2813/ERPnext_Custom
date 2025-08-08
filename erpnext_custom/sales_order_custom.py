import frappe
from frappe.utils import get_url_to_form
from frappe import _

def handle_vip_sales_order(doc, method):
    customer = frappe.get_doc("Customer", doc.customer)
    
    if not customer.get("custom_is_vip_customer"):
        return  

    for item in doc.items:
        actual_qty = frappe.db.get_value("Bin", {
            "item_code": item.item_code,
            "warehouse": item.warehouse
        }, "actual_qty") or 0

        if actual_qty < item.qty:
            create_material_request(doc, item, item.warehouse)

def create_material_request(sales_order, item, warehouse):
    mr = frappe.new_doc("Material Request")
    mr.material_request_type = "Purchase"
    mr.schedule_date = sales_order.delivery_date
    mr.customer = sales_order.customer
    mr.sales_order = sales_order.name
    mr.company = sales_order.company

    mr.append("items", {
        "item_code": item.item_code,
        "qty": item.qty,
        "warehouse": warehouse,
        "schedule_date": sales_order.delivery_date,
        "sales_order": sales_order.name
    })

    mr.insert(ignore_permissions=True)
    send_material_request_email(mr.name)


def send_material_request_email(mr_name):
    doc = frappe.get_doc("Material Request", mr_name)
    url = get_url_to_form("Material Request", doc.name)

    message = f"""
    Dear Warehouse Manager,<br><br>
    A new Material Request <b>{doc.name}</b> has been created from a VIP Sales Order.<br>
    <a href="{url}">Click here to view and take action</a>.<br><br>
    Regards,<br>ERP System
    """

    frappe.sendmail(
        recipients=["22ita58@karpagamtech.ac.in"],
        subject=f"[Action Needed] Material Request {doc.name} Created",
        message=message
    )
