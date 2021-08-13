# -*- coding: utf-8 -*-
# Copyright (c) 2021, OVENUBE and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests
import json
import datetime

class APIConsultas(Document):
	pass

@frappe.whitelist()
def test_connection(url, token):
	headers = {
			'Content-Type':  'application/json'
	}
	response = requests.post(url, headers=headers, data=json.dumps({
		'token': token,
		'tipo_cambio': {
			'moneda': 'PEN',
			'fecha_inicio': datetime.datetime.now().strftime('%d/%m/%Y'),
			'fecha_fin': datetime.datetime.now().strftime('%d/%m/%Y')
		}
	}))
	return json.loads(response.content)

@frappe.whitelist()
def get_exchange_rate():
	headers = {
			'Content-Type':  'application/json'
	}

	tipo_cambio = frappe.get_all("Currency Exchange", filters={
		'date': datetime.datetime.now().strftime('%Y-%m-%d'),
		'from_currency': "USD",
		'to_currency': 'PEN'}
	)

	if tipo_cambio == []:
		authentication = frappe.get_all('API Consultas', fields=['ruta','token'])
		if authentication:
			url = authentication[0].get('ruta')
			token = authentication[0].get('token')

			response = requests.post(url, headers=headers, data=json.dumps({
				'token': token,
				'tipo_cambio': {
					'moneda': 'PEN',
					'fecha_inicio': datetime.datetime.now().strftime('%d/%m/%Y'),
					'fecha_fin': datetime.datetime.now().strftime('%d/%m/%Y')
				}
			}))

			tipo_cambio_info = json.loads(response.content)
			if tipo_cambio_info['success']:
				tipo_cambio = frappe.get_doc({
					'doctype': 'Currency Exchange',
					'date': datetime.datetime.now().strftime('%Y-%m-%d'),
					'from_currency': "USD",
					'to_currency': 'PEN',
					'exchange_rate': tipo_cambio_info['exchange_rates'][0]['venta'],
					'tdx_c_compra': tipo_cambio_info['exchange_rates'][0]['compra'],
					"for_buying": 1,
					"for_selling": 1
				})

				tipo_cambio.save()
			return {
				"success": True,
				"msg": "T/C creado Satisfactoriamente"
			}
	else:
		return {
			"success": True,
			"msg": "T/C ya existe"
		}
	return {
		"success": False,
		"msg": "Error al momento de crear el T/C. Intente nuevamente más tarde"
	}

@frappe.whitelist()
def get_party(company, tax_id, party_type):
	try:
		party = frappe.get_all(party_type, filters={'tax_id': tax_id})

		if party == []:
			authentication = frappe.get_all('API Consultas', fields=['ruta','token'])
			if authentication:
				url = authentication[0].get('ruta')
				token = authentication[0].get('token')

				headers = {
						'Content-Type':  'application/json'
				}

				if len(tax_id) == 11:
					content = {
						'token': token,
						'ruc': tax_id
					}
				elif len(tax_id) == 8:
					content = {
						'token': token,
						'dni': tax_id
					}
				response = requests.post(url, headers=headers, data=json.dumps(content))

				party_info = json.loads(response.content)
				if party_info['success']:
					if len(tax_id) == 11:
						party = frappe.get_doc({
							'doctype': party_type,
							'party_name': party_info['nombre_o_razon_social'],
							party_type.lower() + '_name': party_info['nombre_o_razon_social'],
							'tax_id': party_info['ruc'],
							'tipo_documento_identidad' if party_type == 'Customer' else 'nombre_tipo_documento': 'REGISTRO ÚNICO DE CONTRIBUYENTES',
							'codigo_tipo_documento': '6'
						})
						party.save()

						address_shipping = frappe.get_doc({
							'doctype': 'Address',
							'address_title': party_info['nombre_o_razon_social'],
							'address_type': 'Shipping',
							'address_line1': party_info['direccion_completa'],
							'distrito': party_info['distrito'],
							'provincia': party_info['provincia'],
							'departamento': party_info['departamento'],
							'country': 'Peru'
						})
						address_shipping.save()

						address_billing = frappe.get_doc({
							'doctype': 'Address',
							'address_title': party_info['nombre_o_razon_social'],
							'address_type': 'Billing',
							'address_line1': party_info['direccion_completa'],
							'distrito': party_info['distrito'],
							'provincia': party_info['provincia'],
							'departamento': party_info['departamento'],
							'country': 'Peru'
						})
						address_billing.save()

						shipping_dynamic_link = frappe.get_doc({
									'doctype': 'Dynamic Link',
									'link_doctype': party_type,
									'link_name': party.name,
									'parenttype': 'Address',
									'parent': address_shipping.name
								})
						shipping_dynamic_link.save()

						billing_dynamic_link = frappe.get_doc({
									'doctype': 'Dynamic Link',
									'link_doctype': party_type,
									'link_name': party.name,
									'parenttype': 'Address',
									'parent': address_billing.name
								})
						billing_dynamic_link.save()
											
					elif len(tax_id) == 8:
						party = frappe.get_doc({
							'doctype': party_type,
							'party_name': party_info['nombre_completo'],
							party_type.lower() + '_name': party_info['nombre_completo'],
							'tax_id': party_info['dni'],
							'tipo_documento_identidad' if party_type == 'Customer' else 'nombre_tipo_documento': 'DOCUMENTO NACIONAL DE IDENTIDAD (DNI)',
							'codigo_tipo_documento': '1',
							'party_type': 'Individual'
						})
						party.save()
					return party.name
				else:
					return None
			else:
				return None
		else:
			return party[0]['name']
	except:
		return None