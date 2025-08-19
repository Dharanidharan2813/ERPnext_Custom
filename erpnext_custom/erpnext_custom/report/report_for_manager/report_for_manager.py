import frappe


def execute(filters=None):
    if not filters or not filters.get("doctype_name"):
        return [], []

    doctype = filters.get("doctype_name")

    roles = frappe.get_roles(frappe.session.user)
    allowed_doctypes = []

    if "Administrator" in roles or "Account Manager" in roles:
        allowed_doctypes = ["Sales Order", "Sales Invoice", "Purchase Order", "Purchase Invoice"]
    elif roles == "Sales Manager":
        allowed_doctypes = ["Sales Order", "Sales Invoice"]
    elif roles == "Purchase Manager":
        allowed_doctypes = ["Purchase Order", "Purchase Invoice"]
    elif roles == "Accounts Manager":
        allowed_doctypes = ["Sales Invoice", "Purchase Invoice"]
         
    if doctype not in allowed_doctypes:
        frappe.throw(f"You do not have permission to view {doctype}")

    doc_filters = {}
    if filters.get("workflow_state"):
        doc_filters["workflow_state"] = filters.get("workflow_state")

    columns = [
        {"label": "Select", "fieldname": "select_row", "fieldtype": "HTML"},
        {"label": "Document", "fieldname": "name", "fieldtype": "Link", "options": doctype},
        {"label": "Party", "fieldname": "party", "fieldtype": "Data"},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency"},
        {"label": "Workflow State", "fieldname": "workflow_state", "fieldtype": "Data"},
    ]

    # --- Fetch Data ---
    if doctype == "Sales Invoice":
        data = frappe.get_all(
            "Sales Invoice",
            fields=["name", "customer as party", "grand_total", "workflow_state"],
            filters=doc_filters
        )

    elif doctype == "Sales Order":
        data = frappe.get_all(
            "Sales Order",
            fields=["name", "customer as party", "grand_total", "workflow_state"],
            filters=doc_filters
        )

    elif doctype == "Purchase Invoice":
        data = frappe.get_all(
            "Purchase Invoice",
            fields=["name", "supplier as party", "grand_total", "workflow_state"],
            filters=doc_filters
        )

    elif doctype == "Purchase Order":
        data = frappe.get_all(
            "Purchase Order",
            fields=["name", "supplier as party", "grand_total", "workflow_state"],
            filters=doc_filters
        )

    # --- Add checkbox for each row ---
    for row in data:
        row["select_row"] = f'<input type="checkbox" class="row-select" data-name="{row["name"]}">'

    return columns, data

import frappe

@frappe.whitelist()
def get_workflow_states(doctype_name):
    workflows = frappe.get_all(
        "Workflow", 
        filters={"document_type": doctype_name}, 
        pluck="name"
    )
    if workflows:
        states = frappe.get_all(
            "Workflow Document State",
            filters={"parent": workflows[0]},
            pluck="state"
        )
    
    states = (set(states))
    return states


@frappe.whitelist()
def update_workflow_state(doctype_name, docs, action):
    """Apply a specific workflow action (chosen by Manager) on multiple docs."""
    import json
    from frappe.model.workflow import apply_workflow

    docs = json.loads(docs) if isinstance(docs, str) else docs
    results = []

    for docname in docs:
        try:
            doc = frappe.get_doc(doctype_name, docname)

            # Apply the chosen action
            apply_workflow(doc, action)
            frappe.db.commit()

            results.append({"doc": docname, "status": f"Moved via {action}"})

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Workflow Update Failed for {docname}")
            results.append({"doc": docname, "status": f"Error: {str(e)}"})

    return results

@frappe.whitelist()
def get_workflow_actions(doctype_name):
    """Return all possible workflow actions for a given Doctype."""
    actions = []
    workflows = frappe.get_all(
        "Workflow",
        filters={"document_type": doctype_name},
        pluck="name"
    )
    if workflows:
        actions = frappe.get_all(
            "Workflow Transition",
            filters={"parent": ["in", workflows]},
            pluck="action"
        )
    return sorted(set(actions))
