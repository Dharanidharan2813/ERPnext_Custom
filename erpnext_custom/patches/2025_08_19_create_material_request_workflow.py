import frappe

def execute():
    if frappe.db.exists("Workflow", "test1"):
        return

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "test1",
        "document_type": "Material Request",
        "is_active": 1,
        "override_status": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {"state": "Draft", "doc_status": 0, "allow_edit": "Warehouse Manager", "update_field": "workflow_state", "update_value": "Draft"},
            {"state": "Pending", "doc_status": 0, "allow_edit": "Warehouse Manager", "update_field": "workflow_state", "update_value": "Pending"},
            {"state": "Approved", "doc_status": 1, "allow_edit": "Warehouse Manager", "update_field": "workflow_state", "update_value": "Approved"},
            {"state": "Rejected", "doc_status": 2, "allow_edit": "Warehouse Manager", "update_field": "workflow_state", "update_value": "Rejected"},
        ],
        "transitions": [
            {"state": "Draft", "action": "Approve", "next_state": "Approved", "allowed": "Warehouse Manager", "allow_self_approval": 1},
        ]
    })

    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
