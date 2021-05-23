frappe.ui.form.on("Purchase Order", {
	validate: function(frm) {
		var material_request = 0;
		$.each(frm.doc.items || [], function(i, d) {
			material_request = d.material_request;
		});
		frm.set_value("tdx_c_solicitud", material_request);
	}
});