import frappe, os, json

def load_workflows_from_fixtures():
    path = frappe.get_app_path("erpnext_custom", "path", "workflow.json")

    if not os.path.exists(path):
        frappe.logger().warning("workflow.json not found in fixtures folder")
        return

    with open(path) as f:
        workflows = json.load(f)

    for wf in workflows:
        workflow_name = wf.get("workflow_name")

        if frappe.db.exists("Workflow", workflow_name):
            doc = frappe.get_doc("Workflow", workflow_name)
            doc.update(wf)
            doc.save(ignore_permissions=True)
            frappe.logger().info(f"Updated workflow: {workflow_name}")
        else:
            doc = frappe.get_doc(wf)
            doc.insert(ignore_permissions=True)
            frappe.logger().info(f"Created workflow: {workflow_name}")

    frappe.db.commit()
