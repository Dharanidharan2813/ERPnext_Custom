import frappe

def execute():
    if frappe.db.exists("Workflow", "sales invoice"):
        return

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "sales invoice",
        "document_type": "Sales Invoice",
        "is_active": 1,
        "override_status": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {"state": "Draft", "doc_status": 0, "allow_edit": "Sales Manager", "update_value": "Draft"},
            {"state": "Submit for Account Manager", "doc_status": 0, "allow_edit": "Sales Manager", "update_value": "Submit for Account Manager"},
            {"state": "Approved", "doc_status": 1, "allow_edit": "Accounts Manager", "update_value": "Approved"},
            {"state": "Pending", "doc_status": 0, "allow_edit": "Accounts Manager", "update_value": "Pending"},
            {"state": "Rejected", "doc_status": 0, "allow_edit": "Accounts Manager", "update_value": "Rejected"},
        ],
        "transitions": [
            {"state": "Draft", "action": "Submit for Account Manager", "next_state": "Pending", "allowed": "Sales Manager", "allow_self_approval": 1},
            {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "Accounts Manager", "allow_self_approval": 1},
            {"state": "Pending", "action": "Reject", "next_state": "Rejected", "allowed": "Accounts Manager", "allow_self_approval": 1},
        ]
    })

    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
