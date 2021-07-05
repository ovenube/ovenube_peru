frappe.ui.form.on("Quotation", {
	refresh: function(frm) {
        if (frm.doc.status === 'Draft') {
			frm.add_custom_button(__('Buscar por DNI/RUC'), function () {
				frappe.prompt(
					[{'fieldname': 'tax_id', 'fieldtype': 'Data', 'label': 'DNI, RUC del cliente', 'reqd': 0}],
					function (values) {
						if (values.tax_id && values.tax_id.length) {
							frappe.call({
								method: "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_party",
								args: {
									company: frm.doc.company,
									tax_id: values.tax_id,
                                    party_type: "Customer"
								},
								callback: function(r) {
									if (r.message) {
										frm.set_value("party_name", r.message);
										frm.refresh_fields();
									}
									else {
										frappe.msgprint("El cliente no pudo ser encontrado, revise el número de documento");
									}
								},
								async: false
							});
						}
						else {
							frappe.throw("Debe ingresar un número de documento");
						}
					},
					'Consultar Cliente',
					'Aceptar'
				)
			}, __(""));
		}
    }
});