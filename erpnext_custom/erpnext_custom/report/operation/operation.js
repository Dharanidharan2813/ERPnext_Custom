frappe.query_reports["Operation"] = {
  filters: [
    {
      fieldname: "report_type",
      label: __("Select Report"),
      fieldtype: "Select",
      options: ["Sales Order", "Sales Invoice", "Purchase Order", "Purchase Invoice"],
      default: "Sales Order",
      reqd: 1,
      onchange: function (report) {
        let doctype = frappe.query_report.get_filter_value("report_type");

        frappe.call({
          method: "erpnext_custom.operation1.get_workflow_info",
          args: { doctype },
          callback: function (r) {
            if (r.message) {
              let workflow_state_filter = frappe.query_report.get_filter("workflow_state");
              workflow_state_filter.df.options = [""].concat(r.message.states || []);
              workflow_state_filter.refresh();

              if (report.page.action_dropdown) {
                report.page.action_dropdown.df.options = [""].concat(r.message.actions || []);
                report.page.action_dropdown.refresh();
              }
            }
          }
        });
      }
    },
    {
      fieldname: "workflow_state",
      label: __("Workflow State"),
      fieldtype: "Select",
      options: [""],
      default: "",
      reqd: 0,
    }
  ],

  onload: function (report) {
    if (report.page.custom_dropdown_added) return;

    let action_dropdown = report.page.add_field({
      fieldname: "workflow_action",
      label: __("Process"),
      fieldtype: "Select",
      options: [""],
      default: ""
    });

    report.page.action_dropdown = action_dropdown;

    action_dropdown.$input.on("change", function () {
      let action = action_dropdown.get_value();
      if (!action) return;

      let selected = report.datatable.rowmanager.getCheckedRows();
      if (!selected.length) {
        frappe.msgprint("Please select at least one record");
        action_dropdown.set_value("");
        return;
      }

      let doctype = report.get_values().report_type;

      selected.forEach(row_idx => {
        let row = report.datatable.datamanager.data[row_idx];
        let docname = row.name;
        let current_state = row.workflow_state;

        if (!docname) return;
        frappe.call({
          method: "frappe.client.get",
          args: { doctype: doctype, name: docname },
          callback: function (r) {
            if (r.message) {
              frappe.call({
                method: "frappe.model.workflow.apply_workflow",
                args: {
                  doc: r.message,
                  action: action
                },
                callback: function (res) {
                  if (!res.exc) {
                    report.refresh();
                  } else {
                    frappe.msgprint(`Failed to update ${docname}`);
                  }
                },
                error: function (err) {
                  console.error("Workflow error:", err);
                }
              });
            }
          }
        });
      });

      action_dropdown.set_value("");
    });

    report.page.custom_dropdown_added = true;

    let default_doctype = frappe.query_report.get_filter_value("report_type");
    frappe.call({
      method: "erpnext_custom.operation1.get_workflow_info",
      args: { doctype: default_doctype },
      callback: function (r) {
        if (r.message) {
          let workflow_state_filter = frappe.query_report.get_filter("workflow_state");
          workflow_state_filter.df.options = [""].concat(r.message.states || []);
          workflow_state_filter.refresh();

          if (report.page.action_dropdown) {
            report.page.action_dropdown.df.options = [""].concat(r.message.actions || []);
            report.page.action_dropdown.refresh();
          }
        }
      }
    });
  },

  get_datatable_options(options) {
    return Object.assign(options, {
      checkboxColumn: true,
    });
  },
};
