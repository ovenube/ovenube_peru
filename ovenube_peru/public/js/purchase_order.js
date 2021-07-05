frappe.ui.form.on("Purchase Order", {
	validate: function(frm) {
		var material_request = 0;
		$.each(frm.doc.items || [], function(i, d) {
			material_request = d.material_request;
		});
		frm.set_value("tdx_c_solicitud", material_request);
	},

	refresh: function(frm) {
        if (frm.doc.status === 'Draft') {
			frm.add_custom_button(__('Buscar por DNI/RUC'), function () {
				frappe.prompt(
					[{'fieldname': 'tax_id', 'fieldtype': 'Data', 'label': 'DNI, RUC del proveedor', 'reqd': 0}],
					function (values) {
						if (values.tax_id && values.tax_id.length) {
							frappe.call({
								method: "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_party",
								args: {
									company: frm.doc.company,
									tax_id: values.tax_id,
                                    party_type: "Supplier"
								},
								callback: function(r) {
									if (r.message) {
										frm.set_value("supplier", r.message);
										frm.refresh_fields();
									}
									else {
										frappe.msgprint("Oops! No pudo ser encontrado el proveedor, por favor verifique la información y vuelva a intentarlo.");
									}
								},
								async: false
							});
						}
						else {
							frappe.throw("Debe ingresar un número de documento");
						}
					},
					'Consultar Proveedor',
					'Aceptar'
				)
			}, __(""));
		}
    }
});