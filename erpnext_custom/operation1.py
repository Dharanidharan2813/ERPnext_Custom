import frappe
@frappe.whitelist()
def get_workflow_info(doctype):
    """Return workflow states and actions for a given doctype"""
    workflow = frappe.get_all(
        "Workflow",
        filters={"document_type": doctype, "is_active": 1},
        limit=1
    )
    if not workflow:
        return {"states": [], "actions": []}

    workflow_name = workflow[0].name

    states = frappe.get_all(
        "Workflow Document State",
        filters={"parent": workflow_name},
        fields=["state"]
    )
    state_list = [s["state"] for s in states]

    actions = frappe.get_all(
        "Workflow Transition",
        filters={"parent": workflow_name},
        fields=["action"]
    )
    action_list = list(set(a["action"] for a in actions))

    return {"states": state_list, "actions": action_list}

