# import frappe
# from frappe import _
# from frappe.model.workflow import apply_workflow

# def auto_approve_on_update(doc, method):
#     try:
#         if doc.grand_total < 100000:
#             doc.submit()
#             return

#         if doc.grand_total >= 100000:
#             if doc.workflow_state == "Draft":
#                 apply_workflow(doc, "Approve") 
#                 frappe.msgprint(_("Sales Order auto-approved (₹1L or more)."))
            
#             if doc.docstatus == 0:
#                 doc.submit()
#                 frappe.msgprint(_("Sales Order auto-submitted after approval."))
    
#     except Exception as e:
#         frappe.log_error(title="Auto-Approval or Submission Error", message=str(e))
#         frappe.throw(_("Auto-process failed: {0}").format(str(e)))


# import frappe

# def validate_sales_order(doc, method):
#     if doc.grand_total >= 100000:
#         doc.workflow_state = "Awaiting Approval"
#         frappe.sendmail(
#             recipients=frappe.get_all("User", filters={"enabled": 1}, fields=["email"]),
#             subject=f"Sales Order {doc.name} Awaiting Approval",
#             message=f"Sales Order {doc.name} with grand total of ₹{doc.grand_total} is awaiting approval."
#         )
#     else:
#         doc.workflow_state = "Draft"

# def validate_sales_invoice(doc, method):
#     for item in doc.items:
#         if item.sales_order:
#             so = frappe.get_doc("Sales Order", item.sales_order)
#             if so.grand_total >= 100000 and so.workflow_state != "Approved":
#                 frappe.throw(f"Cannot create Sales Invoice. Sales Order {so.name} is not approved.")


import frappe

# def validate_sales_order(doc, method):
#     if doc.grand_total >= 100000:
#         doc.workflow_state = "Awaiting Approval"

#         # Fetch Sales Manager emails only
#         sales_managers = frappe.get_all(
#             "User",
#             filters={"enabled": 1, "roles.role": "Sales Manager"},
#             fields=["email"]
#         )

#         recipients = [user.email for user in sales_managers if user.email]

#         if recipients:
#             frappe.sendmail(
#                 recipients=recipients,
#                 subject=f"Sales Order {doc.name} Awaiting Approval",
#                 message=f"""
#                     Dear Sales Manager,<br><br>
#                     Sales Order <b>{doc.name}</b> with a grand total of ₹{doc.grand_total:,.2f} 
#                     is awaiting your approval.<br><br>
#                     Please log in to the system to take action.<br><br>
#                     Regards,<br>
#                     ERP System
#                 """
#             )
#     else:
#         doc.workflow_state = "Draft"


# def validate_sales_invoice(doc, method):
#     for item in doc.items:
#         if item.sales_order:
#             so = frappe.get_doc("Sales Order", item.sales_order)import frappe

def validate_sales_order(doc, method):
    if doc.grand_total >= 100000:
        doc.workflow_state = "Awaiting Approval"

        sales_managers = frappe.db.sql("""
            SELECT u.email
            FROM `tabUser` u
            INNER JOIN `tabHas Role` r ON u.name = r.parent
            WHERE r.role = 'Sales Manager' AND u.enabled = 1 AND u.email IS NOT NULL
        """, as_dict=True)

        recipients = [user.email for user in sales_managers]

        order_url = f"{frappe.utils.get_url()}/app/sales-order/{doc.name}"

        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"Sales Order {doc.name} Awaiting Approval",
                message=f"""
                    Dear Sales Manager,<br><br>
                    Sales Order <b>{doc.name}</b> with a grand total of ₹{doc.grand_total:,.2f} 
                    is awaiting your approval.<br><br>
                    <b><a href="{order_url}">Click here to view the Sales Order</a></b><br><br>
                    Regards,<br>
                    ERP System
                """
            )
    else:
        doc.workflow_state = "Draft"

def validate_sales_invoice(doc, method):
    for item in doc.items:
        if item.sales_order:
            so = frappe.get_doc("Sales Order", item.sales_order)
            if so.grand_total >= 100000 and so.workflow_state != "Approved":
                frappe.throw(
                    f"Cannot create Sales Invoice. Sales Order {so.name} (₹{so.grand_total:,.2f}) is not yet approved by Sales Manager."
                )

            if so.grand_total >= 100000 and so.workflow_state != "Approved":
                frappe.throw(
                    f"Cannot create Sales Invoice. Sales Order {so.name} (₹{so.grand_total:,.2f}) is not yet approved by Sales Manager."
                )
