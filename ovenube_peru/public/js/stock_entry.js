//PERSONALIZACION
cur_frm.add_fetch("tdx_c_solicitadopor", "employee_name", "tdx_c_solicitadonombre");
cur_frm.add_fetch("tdx_c_autorizadopor", "employee_name", "tdx_c_autorizadonombre");
cur_frm.add_fetch("tdx_c_ut_transportista", "tax_id", "tdx_c_ut_transportistan");
cur_frm.add_fetch("tdx_c_ut_placa", "make", "tdx_c_ut_marca");
//FIN PERSONALIZACION
cur_frm.add_fetch('tipo_operacion', 'codigo_tipos_operacion', 'codigo_tipo_operacion');
function filter_operacion(frm, cdt, cdn){
	if (frm.doc.purpose == "Material Issue"){
		cur_frm.set_query("tipo_operacion", function(){
			return {
				"filters": [
					["Tipos de Operaciones", "codigo_tipos_operacion", "in", ["12", "13", "14", "15", "28"]]]
			}
		});
	}
	else {
		frm.toggle_display("tipo_operacion", false);
		frm.toggle_display("codigo_tipo_operacion", false);
		frm.toggle_display("sb_sunat", false);
		frappe.model.set_value(cdt, cdn, "codigo_tipo_operacion", "00");
	}
}
frappe.ui.form.on("Stock Entry", {
	onload: function(frm, cdt, cdn){
		filter_operacion(frm, cdt, cdn);
	},

    purpose: function(frm, cdt, cdn){
		filter_operacion(frm, cdt, cdn);
	}
});