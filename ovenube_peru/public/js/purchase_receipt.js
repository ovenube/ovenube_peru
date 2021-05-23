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
	}
});