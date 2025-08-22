import frappe
import requests
import json

def validate_sales_order(doc, method):
    roles = frappe.get_roles(frappe.session.user)
    # if roles == "Customer":
    if doc.grand_total >= 100000:
        doc.workflow_state = "Send for Approval"
        sales_managers = frappe.db.sql("""
            SELECT u.email
            FROM `tabUser` u
            INNER JOIN `tabHas Role` r ON u.name = r.parent
            WHERE r.role = 'Sales Manager' AND u.enabled = 1 AND u.email IS NOT NULL
        """, as_dict=True)
        print(f"Sales Managers: {sales_managers}")

        recipients = [user.email for user in sales_managers]
        order_url = f"{frappe.utils.get_url()}/app/sales-order/{doc.name}"
        send_order_notification(doc, order_url)

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

def send_order_notification(doc, order_url):
    url = "https://graph.facebook.com/v22.0/673195579220918/messages"

    payload = json.dumps({
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "916382759393",
      "type": "text",
      "text": {
        "preview_url": False,
        "body": f"Dear Sales Manager, Sales Order *{doc.name}* with a grand total of ₹{doc.grand_total:,.2f} "
          f"is awaiting your approval.\n\n"
          f"👉 View the order: {order_url}\n\n"
          f"Regards,\nERP System"}
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer EAAUA4RZB7hoEBPMavBTTQD96nvNswJY3j4ZBnvdYjQV1BrSqp2IUSEOwpDgFMsgvI4ZBvvsJHzNUGXfyJgJsyZBkxE8imOsZBSAtERTFQZCnU813eJusnMakwGctVz1EXR6cZCC67jhSu9ZAGcDsijUpM1b0l4Vpz93XmPq9eFsZBQKStow98QTXMGryWreF3Rp0CXsQ0tpcFWf4fVViSDnQKb7Ml27XuWNqEuAsvGyIh8AZDZD'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
