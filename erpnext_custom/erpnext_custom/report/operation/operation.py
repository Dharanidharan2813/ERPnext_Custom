import frappe

def execute(filters=None):
    filters = filters or {}
    report_type = (filters.get("report_type") or "Sales Order").strip()

    if report_type == "Sales Order":
        return _sales_order_report(filters)
    elif report_type == "Sales Invoice":
        return _sales_invoice_report(filters)
    elif report_type == "Purchase Order":
        return _purchase_order_report(filters)
    elif report_type == "Purchase Invoice":
        return _purchase_invoice_report(filters)
    elif report_type == "Payment Entry":
        return _payment_entry_report(filters)
    else:
        return _sales_order_report(filters)


def _sales_order_report(filters):
    conditions, values = _build_conditions(filters, has_workflow=True)

    data = frappe.db.sql(f"""
        SELECT
            name, customer, status, workflow_state, transaction_date, delivery_date, grand_total
        FROM `tabSales Order`
        WHERE docstatus < 2 {conditions}
        ORDER BY transaction_date DESC
    """, values, as_dict=True)

    columns = [
        {"label": "Sales Order", "fieldname": "name", "fieldtype": "Link", "options": "Sales Order"},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Workflow State", "fieldname": "workflow_state", "fieldtype": "Data"},
        {"label": "Order Date", "fieldname": "transaction_date", "fieldtype": "Date"},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date"},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency"},
    ]
    return columns, data


def _sales_invoice_report(filters):
    conditions, values = _build_conditions(filters, has_workflow=True)

    data = frappe.db.sql(f"""
        SELECT
            name, customer, status, workflow_state, posting_date, due_date, grand_total
        FROM `tabSales Invoice`
        WHERE docstatus < 2 {conditions}
        ORDER BY posting_date DESC
    """, values, as_dict=True)

    columns = [
        {"label": "Sales Invoice", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice"},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Workflow State", "fieldname": "workflow_state", "fieldtype": "Data"},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date"},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency"},
    ]
    return columns, data


def _purchase_order_report(filters):
    conditions, values = _build_conditions(filters, has_workflow=True)

    data = frappe.db.sql(f"""
        SELECT
            name, supplier, status, workflow_state, transaction_date, schedule_date, grand_total
        FROM `tabPurchase Order`
        WHERE docstatus < 2 {conditions}
        ORDER BY transaction_date DESC
    """, values, as_dict=True)

    columns = [
        {"label": "Purchase Order", "fieldname": "name", "fieldtype": "Link", "options": "Purchase Order"},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Data"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Workflow State", "fieldname": "workflow_state", "fieldtype": "Data"},
        {"label": "Order Date", "fieldname": "transaction_date", "fieldtype": "Date"},
        {"label": "Schedule Date", "fieldname": "schedule_date", "fieldtype": "Date"},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency"},
    ]
    return columns, data


def _purchase_invoice_report(filters):
    conditions, values = _build_conditions(filters, has_workflow=True)

    data = frappe.db.sql(f"""
        SELECT
            name, supplier, status, workflow_state, posting_date, due_date, grand_total
        FROM `tabPurchase Invoice`
        WHERE docstatus < 2 {conditions}
        ORDER BY posting_date DESC
    """, values, as_dict=True)

    columns = [
        {"label": "Purchase Invoice", "fieldname": "name", "fieldtype": "Link", "options": "Purchase Invoice"},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Data"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Workflow State", "fieldname": "workflow_state", "fieldtype": "Data"},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date"},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency"},
    ]
    return columns, data




def _build_conditions(filters, has_workflow=False):
    """Helper to build WHERE conditions safely."""
    conditions = ""
    values = {}

    if has_workflow and filters.get("workflow_state"):
        conditions += " AND workflow_state = %(workflow_state)s"
        values["workflow_state"] = filters["workflow_state"]

    return conditions, values





