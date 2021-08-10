// Copyright (c) 2021, OVENUBE and contributors
// For license information, please see license.txt


frappe.provide("nubefact_integration.api_consultas");

frappe.ui.form.on('API Consultas', {
	onload_post_render: function(frm) {
		nubefact_integration.api_consultas.check_mandatory_to_set_button(frm);	
	},

	ruta: function(frm) {
		nubefact_integration.api_consultas.check_mandatory_to_set_button(frm);	
	},

	token: function(frm) {
		nubefact_integration.api_consultas.check_mandatory_to_set_button(frm);	
	}
});

nubefact_integration.api_consultas.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.ruta != "" && frm.doc.token != ""){
		frm.fields_dict.test_connection.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.test_connection.$input.removeClass("btn-primary");
	}
};

nubefact_integration.api_consultas.check_mandatory_to_fetch = function(doc) {
	$.each(["ruta"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["token"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
};

frappe.ui.form.on('API Consultas', 'test_connection', function(frm) {
	nubefact_integration.api_consultas.check_mandatory_to_fetch(frm.doc);
	frappe.call({
		method: "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.test_connection",
		args: {
			'url': frm.doc.ruta,
			'token': frm.doc.token
		},
		callback: function (data) {
			if (!data.message.success){
				frappe.throw(data.message.errors);
			}
			else{
				msgprint(__("Successful Connection"),__("Success"));
			}
        }
	});
});