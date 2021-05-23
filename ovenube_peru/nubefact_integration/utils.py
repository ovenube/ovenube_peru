# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, revert_series_if_last

@frappe.whitelist()
def generate_fee_numero_comprobante(serie_comprobante):
    numero_comprobante = make_autoname(key=serie_comprobante)
    return numero_comprobante

@frappe.whitelist()
def revert_fee_numero_comprobante(serie_comprobante, numero_comprobante, serie_nota_credito="", numero_nota_credito=""):
    if serie_nota_credito != "":
        revert_series_if_last(serie_nota_credito, numero_nota_credito)
    else:
        revert_series_if_last(serie_comprobante, numero_comprobante)

def tipo_de_comprobante(codigo):
    if codigo == "01":
        tipo_comprobante = 1
    elif codigo == "03":
        tipo_comprobante = 2
    elif codigo == "07":
        tipo_comprobante = 3
    elif codigo == "08":
        tipo_comprobante = 4
    elif codigo == "09":
        tipo_comprobante = 7
    return tipo_comprobante

def get_serie_correlativo(name):
    try:
        tipo, serie, correlativo = name.split("-")
    except:
        return "", "", ""
    else:
        return tipo, serie, correlativo

def get_doc_transportista(name):
    return frappe.get_doc("Supplier", name)

def get_doc_conductor(name):
    return frappe.get_doc("Driver", name)

def get_moneda(currency):
    if currency == "PEN" or currency == "SOL":
        moneda = 1
    elif currency == "USD":
        moneda = 2
    return moneda

def get_address_information(party_address):
    address = frappe.get_doc("Address", party_address)
    return frappe._dict({
        "address": "-".join(filter(None, (address.get('address_line1'), address.get('city'), address.get('state'), address.get('country')))),
        "email": address.get('email_id'),
        "ubigeo": address.get('ubigeo')
    })

def get_igv(company, name, doctype):
    configuracion = frappe.get_doc("Configuracion Nubefact", company)
    if doctype == "Sales Invoice":
        conf_tax = configuracion.igv_ventas
        account_head = frappe.db.get_value("Sales Taxes and Charges", filters={"parent": conf_tax})
        tax = frappe.get_doc("Sales Taxes and Charges", account_head)
        doc_tax_name = frappe.db.get_value("Sales Taxes and Charges",
                                           filters={"account_head": tax.account_head, "parent": name})
        doc_tax = frappe.get_doc("Sales Taxes and Charges", doc_tax_name)
    return doc_tax.rate, doc_tax.tax_amount, doc_tax.included_in_print_rate

def get_impuesto_bolsas_plasticas(company, name, doctype):
    if frappe.get_single("Accounts Settings").allow_plastic_bags_tax:
        if doctype == "Sales Invoice":
            conf_tax = frappe.get_single("Accounts Settings").plastic_bags_tax_sales
            account_head = frappe.db.get_value("Sales Taxes and Charges", filters={"parent": conf_tax})
            tax = frappe.get_doc("Sales Taxes and Charges", account_head)
            doc_tax_name = frappe.db.get_value("Sales Taxes and Charges",
                                            filters={"account_head": tax.account_head, "parent": name})
            if doc_tax_name:
                doc_tax = frappe.get_doc("Sales Taxes and Charges", doc_tax_name)
            else:
                return 0, 0, 0
        return doc_tax.rate, doc_tax.tax_amount, doc_tax.included_in_print_rate
    else:
        return 0, 0, 0

def get_tipo_producto(item_name):
    producto = frappe.get_doc("Item", item_name)
    if producto.item_group == "Servicios":
        tipo_producto = "ZZ"
    else:
        tipo_producto = "NIU"
    return tipo_producto

def get_serie_online(company, doc_serie):
    online_serie =[]
    online = False
    configuracion = frappe.get_doc("Configuracion Nubefact", company)
    #recorre todos los tipos de comprobante y almacena las series online en un diccionario
    series = configuracion.serie_factura
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_factura)
    series = configuracion.serie_factura_contingencia
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_factura_contingencia)
    series = configuracion.serie_boleta
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_boleta)
    series = configuracion.serie_boleta_contingencia
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_boleta_contingencia)
    series = configuracion.serie_nota_credito
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_nota_credito)
    series = configuracion.serie_nota_credito_contingencia
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_nota_credito_contingencia)
    series = configuracion.serie_nota_debito
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_nota_debito)
    series = configuracion.serie_nota_debito_contingencia
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_nota_debito_contingencia)
    series = configuracion.serie_guia_remision
    for serie in series:
        if serie.online:
            online_serie.append(serie.serie_guia_remision)
    #devuelve True si el serie es online
    for serie in online_serie:
        if doc_serie in serie:
            online = True
    return online