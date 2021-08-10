# -*- coding: utf-8 -*-
# Copyright (c) 2019, OVENUBE and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests
import json

class AutenticacionNubefact(Document):
	pass

@frappe.whitelist()
def test_connection(url, token):
	headers = {
			"Authorization": token,
			"Content-Type":  "application/json"
	}
	response = requests.post(url, headers=headers)
	return json.loads(response.content)

def get_autentication(company):
	try:
		authentication = frappe.get_doc("Autenticacion Nubefact", company)
		token = authentication.get("token_nubefact")
	except:
		headers = {}
	else:
		headers = {
			"Authorization": token,
			"Content-Type": "application/json"
		}
	return headers

def get_url(company):
	try:
		authentication = frappe.get_doc("Autenticacion Nubefact", company)
		url = authentication.get("ruta_nubefact")
	except:
		url = ""
	return url
