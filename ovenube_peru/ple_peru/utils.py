# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from erpnext.setup.doctype.naming_series.naming_series import NamingSeries
import datetime
from datetime import timedelta 
import codecs
import os

class Utils(NamingSeries):
	def get_series(self):
		sales_series = self.get_options("Sales Invoice")
		sales_prefix = []
		sales = ""
		for series in sales_series:
			tipo = series[:2]
			if not tipo in sales_prefix:
				sales_prefix.append(tipo + "%")
		sales = " OR ".join(map(str, sales_prefix))
		return sales

	def get_dates(self, year, periodo):
		if periodo == 'Enero':
			from_date = year+'-01-01'
			to_date = year+'-01-31'
		elif periodo == 'Febrero':
			from_date = year+'-02-01'
			to_date = year+'-02-28'
		elif periodo == 'Marzo':
			from_date = year+'-03-01'
			to_date = year+'-03-31'
		elif periodo == 'Abril':
			from_date = year+'-04-01'
			to_date = year+'-04-30'
		elif periodo == 'Mayo':
			from_date = year+'-05-01'
			to_date = year+'-05-31'
		elif periodo == 'Junio':
			from_date = year+'-06-01'
			to_date = year+'-06-30'
		elif periodo == 'Julio':
			from_date = year+'-07-01'
			to_date = year+'-07-31'
		elif periodo == 'Agosto':
			from_date = year+'-08-01'
			to_date = year+'-08-31'
		elif periodo == 'Setiembre':
			from_date = year+'-09-01'
			to_date = year+'-09-30'
		elif periodo == 'Octubre':
			from_date = year+'-10-01'
			to_date = year+'-10-31'
		elif periodo == 'Noviembre':
			from_date = year+'-11-01'
			to_date = year+'-11-30'
		elif periodo == 'Diciembre':
			from_date = year+'-12-01'
			to_date = year+'-12-31'
		return from_date, to_date

	def ple_name(self, year, periodo):
		if periodo == 'Enero':
			codigo_periodo = year + "01"
		elif periodo == 'Febrero':
			codigo_periodo = year + "02"
		elif periodo == 'Marzo':
			codigo_periodo = year + "03"
		elif periodo == 'Abril':
			codigo_periodo = year + "04"
		elif periodo == 'Mayo':
			codigo_periodo = year + "05"
		elif periodo == 'Junio':
			codigo_periodo = year + "06"
		elif periodo == 'Julio':
			codigo_periodo = year + "07"
		elif periodo == 'Agosto':
			codigo_periodo = year + "08"
		elif periodo == 'Setiembre':
			codigo_periodo = year + "09"
		elif periodo == 'Octubre':
			codigo_periodo = year + "10"
		elif periodo == 'Noviembre':
			codigo_periodo = year + "11"
		elif periodo == 'Diciembre':
			codigo_periodo = year + "12"
		return codigo_periodo

	def get_work_days(self, current_date, num_work_days):
		holidays = []
		i = 0
		first_date = datetime.date(datetime.date.today().year, 1, 1)
		last_date = datetime.date(datetime.date.today().year, 12, 31)
		holidays_lists = frappe.get_all("Holiday List", filters={
			'from_date': first_date,
			'to_date': last_date
		})
		for holidays_list_name in holidays_lists:
			holidays_list = frappe.get_doc('Holiday List', holidays_list_name.name)
			for holiday in holidays_list.holidays:
				holidays.append(holiday)			
		while (i < num_work_days):
			current_date = current_date + timedelta(days=1)
			if not (current_date.strftime('%Y-%m-%d') in holidays or current_date.weekday() == 5 or current_date.weekday() == 6):
				i += 1
		return current_date

@frappe.whitelist()
def send_file_to_client(file, tipo, nombre):
	data = read_txt(file)
	frappe.response['result'] = cstr(data)
	frappe.response['type'] = tipo
	frappe.response['doctype'] = nombre

def to_file(data, tipo, nombre, primer=None):
	path = frappe.get_site_path('public', 'files') + "/libros/" + tipo
	if not os.path.isdir(path):
		os.makedirs(path)
	archivo = path + "/" + nombre
	exported_file = codecs.open(archivo, "w", encoding='utf-8')
	nombre, ext = nombre.split(".")
	if tipo == "compras":
		for row in data:
			for key, value in row.items():
				if value is None:
					row[key] = ""
			exported_file.write(
				row['periodo'] + '|' +
				row['cuo'] + '|' +
				row['correlativo_asiento'] + '|' +
				str(row['fecha_emision']) + '|' +
				str(row['fecha_cancelacion']) + '|' +
				row['codigo_tipo_comprobante'] + '|' +
				row['serie_comprobante'] + '|' +
				row['codigo_DUA'] + '|' +
				row['numero_comprobante'] + '|' +
				row['resumen_diario'] + '|' +
				row['tipo_documento'] + '|' +
				row['numero_documento'] + '|' +
				row['nombre_proveedor'] + '|' +
				str(row['base_imponible']) + '|' +
				str(row['monto_impuesto']) + '|' +
				row['base_imponible_exportacion'] + '|' +
				row['monto_impuesto_exportacion'] + '|' +
				row['base_imponible_no_gravada'] + '|' +
				str(row['monto_impuesto_no_gravada']) + '|' +
				str(row['valor_adquisicion_no_gravada']) + '|' +
				row['monto_isc'] + '|' +
				row['monto_ibp'] + "|" + 
				row['otros_conceptos'] + '|' +
				str(row['valor_adquisicion']) + '|' +
				row['moneda'] + '|' +
				str(row['tipo_cambio']) + '|' +
				row['fecha_inicial_devolucion'] + '|' +
				row['tipo_devolucion'] + '|' +
				row['serie_devolucion'] + '|' +
				row['numero_devolucion'] + '|' +
				row['numero_devolucion'] + '|' +
				row['fecha_detraccion'] + '|' +
				row['constancia_detraccion'] + '|' +
				row['marca_retencion'] + '|' +
				row['clasificacion_items'] + '|' +
				row['contrato'] + '|' +
				row['error_1'] + '|' +
				row['error_2'] + '|' +
				row['error_3'] + '|' +
				row['error_4'] + '|' +
				str(row['indicador_pago']) + '|' +
				str(row['anotacion'] + '|\n'))
	elif tipo == "ventas":
		for row in data:
			for key, value in row.items():
				if value is None:
					row[key] = ""
			exported_file.write(
				row['periodo'] + "|" +
				row['cuo'] + "|" +
				row['correlativo_asiento'] + "|" +
				str(row['fecha_emision']) + "|" +
				str(row['fecha_cancelacion']) + "|" +
				row['codigo_tipo_comprobante'] + "|" +
				row['serie_comprobante'] + "|" +
				row['numero_comprobante'] + "|" +
				row['resumen_diario'] + "|" +
				row['tipo_documento'] + "|" +
				row['numero_documento'] + "|" +
				row['nombre_cliente'] + "|" +
				row['valor_exportacion'] + "|" +
				str(row['base_imponible']) + "|" +
				row['descuento'] + "|" +
				str(row['monto_impuesto']) + "|" +
				row['descuento_igv'] + "|" +
				str(row['total_exonerado']) + "|" +
				str(row['total_inafecto']) + "|" +
				row['monto_isc'] + "|" +
				row['base_arroz'] + "|" +
				row['impuesto_arroz'] + "|" +
				row['monto_ibp'] + "|" + 
				row['otros_conceptos'] + "|" +
				str(row['valor_adquisicion']) + "|" +
				row['moneda'] + "|" +
				str(row['tipo_cambio']) + "|" +
				str(row['fecha_inicial_devolucion']) + "|" +
				str(row['tipo_devolucion']) + "|" +
				str(row['serie_devolucion']) + "|" +
				str(row['numero_devolucion']) + "|" +
				row['contrato'] + "|" +
				row['error_1'] + "|" +
				str(row['indicador_pago']) + "|" +
				str(row['anotacion'] + "|\n"))
	elif tipo == "diario":
		if primer == "1":
			for row in data:
				exported_file.write(
					row['periodo'] + "|" +
					row['codigo_asiento'] + "|" +
					row['descripcion_asiento'] + "|" +
					row['codigo_plan'] + "|" +
					row['descripcion_plan'] + "|" +
					row['codigo_cuenta'] + "|" +
					row['descripcion_cuenta'] + "|" +
					row['indicador_cuenta'] + "|\n")
		else:
			for row in data:
				for key, value in row.items():
					if value is None:
						row[key] = ""
				exported_file.write(
					row['periodo'] + "|" +
					row['cuo'] + "|" +
					row['correlativo_asiento'] + "|" +
					row['codigo_asiento'] + "|" +
					row['cuo_ue'] + "|" +
					row['centro_costo'] + "|" +
					row['tipo_moneda'] + "|" +
					row['tipo_documento'] + "|" +
					row['tax_id'] + "|" +
					row['codigo_comprobante'] + "|" +
					row['serie_comprobante'] + "|" +
					row['numero_comprobante'] + "|" +
					str(row['fecha_contable']) + "|" +
					str(row['fecha_vencimiento']) + "|" +
					str(row['fecha_emision']) + "|" +
					row['glosa'] + "|" +
					row['glosa_referencial'] + "|" +
					str(row['debe']) + "|" +
					str(row['haber']) + "|" +
					row['estructurado'] + "|" +
					str(row['estado'] + "|\n"))
	elif tipo == "diario_simplificado":
		if primer == "1":
			for row in data:
				exported_file.write(
					row['periodo'] + "|" +
					row['codigo_asiento'] + "|" +
					row['descripcion_asiento'] + "|" +
					row['codigo_plan'] + "|" +
					row['descripcion_plan'] + "|" +
					row['codigo_cuenta'] + "|" +
					row['descripcion_cuenta'] + "|" +
					row['indicador_cuenta'] + "|\n")
		else:
			for row in data:
				for key, value in row.items():
					if value is None:
						row[key] = ""
				exported_file.write(
					row['periodo'] + "|" +
					row['cuo'] + "|" +
					row['correlativo_asiento'] + "|" +
					row['codigo_asiento'] + "|" +
					row['cuo_ue'] + "|" +
					row['centro_costo'] + "|" +
					row['tipo_moneda'] + "|" +
					row['tipo_documento'] + "|" +
					row['tax_id'] + "|" +
					row['codigo_comprobante'] + "|" +
					row['serie_comprobante'] + "|" +
					row['numero_comprobante'] + "|" +
					str(row['fecha_contable']) + "|" +
					str(row['fecha_vencimiento']) + "|" +
					str(row['fecha_emision']) + "|" +
					row['glosa'] + "|" +
					row['glosa_referencial'] + "|" +
					str(row['debe']) + "|" +
					str(row['haber']) + "|" +
					row['estructurado'] + "|" +
					str(row['estado'] + "|\n"))
	elif tipo == "mayor":
		for row in data:
			for key, value in row.items():
				if value is None:
					row[key] = ""
			exported_file.write(
				row['periodo'] + "|" +
				row['cuo'] + "|" +
				row['correlativo_asiento'] + "|" +
				row['codigo_asiento'] + "|" +
				row['cuo_ue'] + "|" +
				row['centro_costo'] + "|" +
				row['tipo_moneda'] + "|" +
				row['tipo_documento'] + "|" +
				row['tax_id'] + "|" +
				row['codigo_comprobante'] + "|" +
				row['serie_comprobante'] + "|" +
				row['numero_comprobante'] + "|" +
				str(row['fecha_contable']) + "|" +
				str(row['fecha_vencimiento']) + "|" +
				str(row['fecha_emision']) + "|" +
				row['glosa'] + "|" +
				row['glosa_referencial'] + "|" +
				str(row['debe']) + "|" +
				str(row['haber']) + "|" +
				row['estructurado'] + "|" +
				str(row['estado'] + "|\n"))
	elif tipo == "inventario":
		for row in data:
			for key, value in row.items():
				if value is None:
					row[key] = ""
			exported_file.write(
				row['periodo'] + "|"+
				row['cuo'] + "|" +
				row['correlativo_asiento'] + "|" +
				row['almacen'] + "|" +
				row['codigo_catalogo'] + "|" +
				row['codigo_tipo_existencia'] + "|" +
				row['codigo_producto'] + "|" +
				row['codigo_sunat'] + "|" +
				str(row['fecha_emision']) + "|" +
				row['codigo_comprobante'] + "|" +
				row['serie_comprobante'] + "|" +
				row['correlativo_comprobante'] + "|" +
				row['codigo_operacion'] + "|" +
				row['descripcion_producto'] + "|" +
				row['uom'] + "|" +
				row['codigo_valuacion'] + "|" +
				str(row['cantidad']) + "|" +
				str(row['costo_unitario']) + "|" +
				str(row['costo_total']) + "|" +
				str(row['cantidad_retirado']) + "|" +
				str(row['costo_unitario_retirado']) + "|" +
				str(row['costo_total_retirado']) + "|" +
				str(row['saldo_final']) + "|" +
				str(row['costo_unitario_saldo_final']) + "|" +
				str(row['costo_total_saldo_final']) + "|" +
				str(row['anotacion'] + "|\n"))
	return {"archivo": archivo, "tipo": ext, "nombre": nombre}

def read_txt(file):
	data = ""
	exported_file = codecs.open(file, 'r', encoding='utf-8')
	for line in exported_file:
		data = data + line
	return data
