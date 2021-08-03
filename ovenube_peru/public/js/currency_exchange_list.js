frappe.listview_settings['Currency Exchange'] = {
    refresh: function(listview) {
        listview.page.add_menu_item(__("Consulta Sunat"), function() {
            frappe.call({
                method: "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate",
                callback: function(r) {
                    if (r.message.success){
                        frappe.msgprint(r.message.msg);
                    }
                    else {
                        frappe.throw(r.message.msg);
                    }
                }
            })
        });
    } 
}