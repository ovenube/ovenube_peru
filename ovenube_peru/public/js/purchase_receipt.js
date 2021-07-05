cur_frm.add_fetch('tipo_comprobante', 'codigo_tipo_comprobante', 'codigo_tipo_comprobante');
cur_frm.add_fetch('tipo_operacion', 'codigo_tipos_operacion', 'codigo_tipo_operacion');
function filter_operacion(frm, cdt, cdn){
	cur_frm.set_query("tipo_operacion", function(){
		return {
			"filters": [
				["Tipos de Operaciones", "codigo_tipos_operacion", "in", ["02", "04", "06"]]]
		};
	});
}
function filter_comprobantes(frm, cdt, cdn){
	cur_frm.set_query("tipo_comprobante", function(){
		return {
			"filters": [
				["Tipos de Comprobante", "codigo_tipo_comprobante", "in", ["31"]]]
		};
	});
}
frappe.ui.form.on("Purchase Receipt", {
	onload: function(frm, cdt, cdn){
		filter_operacion(frm, cdt, cdn);
		filter_comprobantes(frm, cdt, cdn);
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