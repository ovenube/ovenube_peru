cur_frm.add_fetch('student', 'codigo_tipo_documento', 'codigo_tipo_documento');
cur_frm.add_fetch('student', 'tipo_documento_identidad', 'tipo_documento_identidad');
cur_frm.add_fetch('student', 'tax_id', 'tax_id');
cur_frm.add_fetch('razon_social', 'tax_id', 'tax_id');
cur_frm.add_fetch('razon_social', 'customer_primary_address', 'direccion');
cur_frm.add_fetch('tipo_transaccion_sunat', 'codigo_tipo_transaccion', 'codigo_transaccion_sunat');
cur_frm.add_fetch('tipo_nota_credito', 'codigo_notas_credito', 'codigo_nota_credito');

function get_document_series(frm, cdt, cdn){
	frappe.call({
		type: "GET",
		method: "ovenube_peru.nubefact_integration.doctype.configuracion_nubefact.configuracion_nubefact.get_doc_serie",
		args: {
			company: frm.doc.company,
			doctype: frm.doc.doctype,
			is_return: frm.doc.is_return ? "1" : "0",
			contingencia: frm.doc.contingencia ? "1" : "0",
			codigo_tipo_documento: frm.doc.codigo_tipo_documento
		},
		callback: function(r) {
			frappe.model.set_value(cdt, cdn, "tipo_comprobante", r.message.descripcion);
			frappe.model.set_value(cdt, cdn, "codigo_comprobante", r.message.codigo);
			if (frm.doc.is_return === 1) {
				frm.set_df_property("serie_nota_credito", "options", r.message.series);
			}
			else {
				frm.set_df_property("serie_comprobante", "options", r.message.series);
			}
		}
	});
}

function get_document_transaction(frm, cdt, cdn){
	frappe.call({
		type: "GET",
		method: "ovenube_peru.nubefact_integration.doctype.tipos_de_transaccion_sunat.tipos_de_transaccion_sunat.get_tipo_transaccion_fee",
		args: {
			student: frm.doc.student,
			is_return: frm.doc.is_return ? "1" : "0"
		},
		callback: function(r) {
			frappe.model.set_value(cdt, cdn, "tipo_transaccion_sunat", r.message.descripcion);
			frappe.model.set_value(cdt, cdn, "codigo_transaccion_sunat", r.message.codigo);
		}
	});
}

frappe.ui.form.on("Fees", {
	student: function(frm, cdt, cdn) {
		if (frm.doc.codigo_tipo_documento){
			get_document_series(frm, cdt, cdn);
			get_document_transaction(frm, cdt, cdn);
		}
		else {
			frappe.model.set_value(cdt, cdn, "tipo_comprobante", null);
			frappe.model.set_value(cdt, cdn, "codigo_comprobante", null);
			frappe.model.set_value(cdt, cdn, "tipo_transaccion_sunat", null);
			frappe.model.set_value(cdt, cdn, "codigo_transaccion_sunat", null);
		}
	},

    contingencia: function(frm, cdt, cdn) {
		if (frm.doc.codigo_tipo_documento){
			get_document_series(frm, cdt, cdn);
		}
	},

    is_return: function(frm, cdt, cdn) {
		if (frm.doc.codigo_tipo_documento){
			get_document_series(frm, cdt, cdn);
		}
	},

    factura_de_venta: function(frm, cdt, cdn) {
		if (frm.doc.codigo_tipo_documento){
			if (frm.doc.factura_de_venta == "1"){
				frappe.model.set_value(cdt, cdn, "tipo_documento_identidad", "REGISTRO ÚNICO DE CONTRIBUYENTES");
				frappe.model.set_value(cdt, cdn, "codigo_tipo_documento", "6");
				frappe.model.set_value(cdt,cdn, "tax_id", "");
			}
			else{
				frappe.model.set_value(cdt, cdn, "tipo_documento_identidad", "DOCUMENTO NACIONAL DE IDENTIDAD (DNI)");
				frappe.model.set_value(cdt, cdn, "codigo_tipo_documento", "1");
			}			
			get_document_series(frm, cdt, cdn);
		}
	},

    refresh: function(frm, cdt, cdn){
		if (frm.doc.is_return == 1){
			get_document_series(frm, cdt, cdn);
		}
		if(frm.doc.docstatus === 1 && frm.doc.outstanding_amount == 0 && frm.doc.numero_comprobante == null) {
			frm.add_custom_button(__("Generate Invoice"), function() {
				frm.events.make_electronic_invoice(frm, cdt, cdn);
			}, __("Make"));
			frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
		if(frm.doc.is_return===1 && frm.doc.tipo_nota_credito != null && frm.doc.serie_nota_credito != null && frm.doc.numero_nota_credito == null) {
			frm.add_custom_button(__("Generate Credit Note"), function() {
				frm.events.make_electronic_invoice(frm, cdt, cdn);
			}, __("Make"));
			frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
		if(frm.doc.enlace_pdf != null) {
			frm.add_custom_button(__("View Invoice"), function() {
				window.open(frm.doc.enlace_pdf);
			}, __("View"));
			frm.page.set_inner_btn_group_as_primary(__("View"));
		}
	},

	make_electronic_invoice: function(frm, cdt, cdn){
		var flag = true;
		if (frm.doc.factura_de_venta == 1){
			if (typeof frm.doc.razon_social === 'undefined' || typeof frm.doc.tax_id === 'undefined' || typeof frm.doc.direccion === 'undefined'){
				flag = false;
			}
		}
		if (flag) {
			if (frm.doc.estado_sunat == null || frm.doc.is_return == 1) {
				frappe.call({
					method: "ovenube_peru.nubefact_integration.facturacion_electronica.send_document",
					args: {
						'company': frm.doc.company,
						'invoice': frm.doc.name,
						'doctype': frm.doc.doctype
					},
					callback: function(data) {
						if (frm.doc.is_return === 1) {
							frm.set_value("numero_nota_credito", data.message.numero_nota_credito);
							frm.set_value("fecha_nota_credito", frappe.datetime.nowdate());
						}
						else {
							frm.set_value("numero_comprobante", data.message.numero_comprobante);
							frm.set_value("fecha_comprobante", frappe.datetime.nowdate());
						}
						if (data.message.codigo_hash) {
							frm.set_value("estado_sunat", (data.message.codigo_hash) ? ("Aceptado") : ("Rechazado"));
							frm.set_value("respuesta_sunat", data.message.sunat_description);
							frm.set_value("codigo_qr_sunat", data.message.cadena_para_codigo_qr);
							frm.set_value("codigo_barras_sunat", data.message.codigo_de_barras);
							frm.set_value("enlace_pdf", data.message.enlace_del_pdf);
							frm.set_value("codigo_hash_sunat", data.message.codigo_hash);
							frm.save_or_update();
						} else{
							return new Promise(function(resolve, reject) {
								frappe.call({
									method: "ovenube_peru.nubefact_integration.utils.revert_fee_numero_comprobante",
									args: {
										'serie_comprobante': frm.doc.serie_comprobante,
										'numero_comprobante': frm.doc.numero_comprobante,
										'serie_nota_credito': frm.doc.serie_nota_credito,
										'numero_nota_credito': frm.doc.numero_nota_credito,
									}
								});								
							}).then(function(values) {
								frappe.throw(data.message.errors);
								if (frm.doc.is_return === 1) {
									frm.set_value("numero_nota_credito", "");
									frm.set_value("fecha_nota_credito", "");
								}
								else {
									frm.set_value("numero_comprobante", "");
									frm.set_value("fecha_comprobante", "");
								}
								frm.save_or_update();
							});
						}
					}
				});
			}
		}
	},

	setup: function(frm, cdt, cdn) {
		frm.set_query('direccion', function(doc) {
			return {
				query: "erpnext.selling.doctype.customer.customer.get_customer_address",
				filters: {
					'customer': doc.razon_social
				}
			};
		});
	},

    before_cancel: function(frm, cdt, cdn){
		if (frappe.datetime.get_day_diff(frm.doc.posting_date, frappe.datetime.get_today()) < 7 && frm.doc.estado_anulacion != "En proceso" && frm.doc.numero_nota_credito == null){
			return new Promise(function(resolve, reject) {
				frappe.prompt([
					{'fieldname': 'motivo', 'fieldtype': 'Data', 'label': 'Motivo de la cancelacion', 'reqd': 1}  
				],
				function(values){
					resolve(values);
				},
				'Cancelacion de Comprobante',
				'Anular'
				);
			}).then(function (values){
				frappe.validated = false;
				frappe.call({
					method: "ovenube_peru.nubefact_integration.facturacion_electronica.cancel_document",
					args: {
						'company': frm.doc.company,
						'invoice': frm.docname,
						'doctype': frm.doctype,
						'motivo': values.motivo
					},
					callback: function (data) {
						console.log(data);
						frappe.msgprint("<b>Esperando respuesta de SUNAT</b>", 'Cancelación');
					}
				});
			});
		}
		else {
			frappe.validated = false;
			frappe.msgprint("<b>Documento no se puede anular o esta en proceso de anulación</b>", 'Cancelación');
		}
	}
});