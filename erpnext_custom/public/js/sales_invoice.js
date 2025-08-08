// frappe.listview_settings['Sales Order'] = {
//     get_indicator: function (doc) {
//         if (doc.workflow_state === "Approved") {
//             return [__("Approved"), "green", "workflow_state,=,Approved"];
//         } else if (doc.workflow_state === "Draft") {
//             return [__("Draft"), "orange", "workflow_state,=,Draft"];
//         } else if (doc.workflow_state === "Rejected") {
//             return [__("Rejected"), "red", "workflow_state,=,Rejected"];
//         } else {
//             return [__(doc.workflow_state), "gray", `workflow_state,=,${doc.workflow_state}`];
//         }
//     }
// };


// frappe.listview_settings['Sales Order'] = {
//     get_indicator: function (doc) {
//         console.log("get_indicator triggered", doc.name, doc.workflow_state); // ✅ debug log

//         if (doc.workflow_state === "Approved") {
//             return [__("Approved"), "green", "workflow_state,=,Approved"];
//         } else if (doc.workflow_state === "Draft") {
//             return [__("Draft"), "orange", "workflow_state,=,Draft"];
//         } else if (doc.workflow_state === "Rejected") {
//             return [__("Rejected"), "red", "workflow_state,=,Rejected"];
//         } else {
//             return [__(doc.workflow_state), "gray", "workflow_state,=," + doc.workflow_state];
//         }
//     }
// };

frappe.ui.form.on('Sales Invoice', {
    validate: function(frm) {
        const sales_orders = frm.doc.items.map(i => i.sales_order).filter(i => i);
        if (!sales_orders.length) return;

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Sales Order",
                filters: {
                    name: ["in", sales_orders]
                },
                fields: ["name", "grand_total", "workflow_state"]
            },
            callback: function(r) {
                let not_approved = r.message.filter(so => so.grand_total >= 100000 && so.workflow_state !== "Approved");
                if (not_approved.length) {
                    frappe.throw(`Sales Order ${not_approved[0].name} is not approved. Invoice creation blocked.`);
                }
            }
        });
    }
});
