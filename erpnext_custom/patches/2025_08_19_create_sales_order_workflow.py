import frappe

def execute():
    if frappe.db.exists("Workflow", "s1"):
        return

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "s1",
        "document_type": "Sales Order",
        "is_active": 1,
        "override_status": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {"state": "Draft", "doc_status": 0, "allow_edit": "All", "update_field": "workflow_state", "update_value": "Draft"},
            {"state": "Submit for Account Manager", "doc_status": 0, "allow_edit": "All", "update_field": "workflow_state", "update_value": "Submit for Account Manager"},
            {"state": "Approved", "doc_status": 1, "allow_edit": "All", "update_field": "workflow_state", "update_value": "Approved"},
            {"state": "Rejected", "doc_status": 0, "allow_edit": "All", "update_field": "workflow_state", "update_value": "Rejected"},
            {"state": "Pending", "doc_status": 0, "allow_edit": "All", "update_field": "workflow_state", "update_value": "Pending"},
        ],
        "transitions": [
            {"state": "Draft", "action": "Submit for Account Manager", "next_state": "Pending", "allowed": "Sales Manager", "allow_self_approval": 1},
            {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "Accounts Manager", "allow_self_approval": 1},
            {"state": "Pending", "action": "Reject", "next_state": "Rejected", "allowed": "Accounts Manager", "allow_self_approval": 1},
        ]
    })

    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
