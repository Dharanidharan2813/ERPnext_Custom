// frappe.query_reports["Report For Manager"] = {
//     filters: [
//         {
//             fieldname: "doctype_name",
//             label: "Document Type",
//             fieldtype: "Select",
//             options: [" ", "Sales Order", "Sales Invoice", "Purchase Order", "Purchase Invoice"],
//             default: " ",
//             reqd: 1
//         },
//         {
//             fieldname: "workflow_state",
//             label: "Workflow State",
//             fieldtype: "Select",
//             options: [" "],
//             default: " ",
//             reqd: 1
//         }
//     ],

//     onload: function(report) {
//         // 🔹 Bind onchange for Doctype filter
//         report.get_filter('doctype_name').$input.on("change", function() {
//             let doctype = frappe.query_report.get_filter_value("doctype_name");
//             console.log("📢 onchange fired, doctype =", doctype);

//             if (!doctype || doctype === " ") return;

//             frappe.call({
//                 method: "erpnext_custom.erpnext_custom.report.report_for_manager.report_for_manager.get_workflow_states",
//                 args: { doctype_name: doctype },
//                 callback: function(r) {
//                     console.log("📢 API response =", r);

//                     if (r.message) {
//                         let state_filter = frappe.query_report.get_filter('workflow_state');
//                         state_filter.df.options = [" "].concat(r.message);
//                         state_filter.df.default = " ";
//                         state_filter.refresh();
//                         state_filter.set_input(" ");
//                     }
//                 }
//             });
//         });

//         // 🔹 Add Workflow Action button
//         report.page.add_inner_button(__("Workflow Action"), function() {
//             let selected = [];
//             $(".row-select:checked").each(function() {
//                 selected.push($(this).data("name"));
//             });

//             if (selected.length === 0) {
//                 frappe.msgprint("Please select at least one document.");
//                 return;
//             }

//             let doctype = frappe.query_report.get_filter_value("doctype_name");
//             console.log("Selected documents:", doctype, selected);

//             frappe.call({
//                 method: "erpnext_custom.erpnext_custom.report.report_for_manager.report_for_manager.update_workflow_state",
//                 args: {
//                     doctype_name: doctype,
//                     docs: selected
//                 },
//                 callback: function(r) {
//                     if (!r.exc) {
//                         frappe.msgprint("Workflow updated successfully.");
//                         frappe.query_report.refresh();
//                     }
//                 }
//             });
//         });
//     }
// };



frappe.query_reports["Report For Manager"] = {
    filters: [
        {
            fieldname: "doctype_name",
            label: "Document Type",
            fieldtype: "Select",
            options: [" ", "Sales Order", "Sales Invoice", "Purchase Order", "Purchase Invoice"],
            default: " ",
            reqd: 1
        },
        {
            fieldname: "workflow_state",
            label: "Workflow State",
            fieldtype: "Select",
            options: [" "],
            default: " ",
            reqd: 1
        }
    ],

    onload: function(report) {
        // Bind onchange for Document Type filter
        report.get_filter('doctype_name').$input.on("change", function() {
            let doctype = frappe.query_report.get_filter_value("doctype_name");
            if (!doctype || doctype === " ") return;

            // Load workflow states
            frappe.call({
                method: "erpnext_custom.erpnext_custom.report.report_for_manager.report_for_manager.get_workflow_states",
                args: { doctype_name: doctype },
                callback: function(r) {
                    if (r.message) {
                        let state_filter = frappe.query_report.get_filter('workflow_state');
                        state_filter.df.options = [" "].concat(r.message);
                        state_filter.df.default = " ";
                        state_filter.refresh();
                        state_filter.set_input(" ");
                    }
                }
            });

            // Load workflow actions (for dropdown button)
            frappe.call({
                method: "erpnext_custom.erpnext_custom.report.report_for_manager.report_for_manager.get_workflow_actions",
                args: { doctype_name: doctype },
                callback: function(r) {
                    if (r.message) {
                        // remove old button first
                        report.page.clear_inner_toolbar();

                        // create dropdown
                        report.page.add_inner_button(__("Workflow Actions"), null, "Actions");

                        r.message.forEach(action => {
                            report.page.add_inner_button(action, function() {
                                let selected = [];
                                $(".row-select:checked").each(function() {
                                    selected.push($(this).data("name"));
                                });

                                if (selected.length === 0) {
                                    frappe.msgprint("Please select at least one document.");
                                    return;
                                }

                                frappe.call({
                                    method: "erpnext_custom.erpnext_custom.report.report_for_manager.report_for_manager.update_workflow_state",
                                    args: {
                                        doctype_name: doctype,
                                        docs: selected,
                                        action: action   // 👈 send chosen action
                                    },
                                    callback: function(r) {
                                        if (!r.exc) {
                                            frappe.msgprint(`Workflow action '${action}' applied successfully.`);
                                            frappe.query_report.refresh();
                                        }
                                    }
                                });
                            }, "Workflow Actions");
                        });
                    }
                }
            });
        });
    }
};
