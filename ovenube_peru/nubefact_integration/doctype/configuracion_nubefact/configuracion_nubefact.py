# -*- coding: utf-8 -*-
# Copyright (c) 2019, OVENUBE and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.setup.doctype.naming_series.naming_series import NamingSeries


class ConfiguracionNubefact(NamingSeries):
    def get_series(self):
        serie_ventas = self.get_options("Sales Invoice")
        serie_ventas.replace("\n\n", "\n")
        serie_ventas = serie_ventas.split("\n")
        serie_guias = self.get_options("Delivery Note")
        serie_guias.replace("\n\n", "\n")
        serie_guias = serie_guias.split("\n")
        series_dict = {}
        series_dict["venta"] = []
        series_dict["guia"] = []
        for serie in serie_ventas:
            series_dict["venta"].append(serie)
        for serie in serie_guias:
            series_dict["guia"].append(serie)
        return series_dict

@frappe.whitelist()
def get_product_anticipo(company):
    configuracion = frappe.get_doc("Configuracion Nubefact", company)
    return configuracion.anticipo

@frappe.whitelist()
def get_cuentas_bancarias(company, currency):
    configuracion = frappe.get_doc("Configuracion Nubefact", company)
    cuenta_bancaria = ""
    if currency == "USD":
        cuenta_bancaria = configuracion.cuenta_bancaria_dolares
    else:
        cuenta_bancaria = configuracion.cuenta_bancaria_soles
    return cuenta_bancaria if cuenta_bancaria else ""

@frappe.whitelist()
def get_doc_serie(company, doctype, is_return="", contingencia="", codigo_tipo_documento="", codigo_comprobante="", es_nota_debito="", online=None):
    doc_series = []
    configuracion = frappe.get_doc("Configuracion Nubefact", company)
    if doctype == "Sales Invoice":
        if is_return == "1":
            comprobante = frappe.get_doc("Tipos de Comprobante", "Nota de Crédito")
            if contingencia == "1":
                series = configuracion.serie_nota_credito_contingencia
                if codigo_tipo_documento == "6" or codigo_tipo_documento == "0":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_credito_contingencia)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_credito_contingencia)
            else:
                series = configuracion.serie_nota_credito
                if codigo_tipo_documento == "6" or codigo_tipo_documento == "0":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_credito)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_credito)
        elif es_nota_debito == "1":
            comprobante = frappe.get_doc("Tipos de Comprobante", "Nota de Débito")
            if contingencia == "1":
                series = configuracion.serie_nota_debito_contingencia
                if codigo_tipo_documento == "6" or codigo_tipo_documento == "0":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_debito_contingencia)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_debito_contingencia)
            else:
                series = configuracion.serie_nota_debito
                if codigo_tipo_documento == "6" or codigo_tipo_documento == "0":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_debito)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_debito)
        else:
            if codigo_tipo_documento == "6" or codigo_tipo_documento == "0":
                comprobante = frappe.get_doc("Tipos de Comprobante", "Factura")
                if contingencia == "1":
                    series = configuracion.serie_factura_contingencia
                    for serie in series:
                        doc_series.append(serie.serie_factura_contingencia)
                else:
                    series = configuracion.serie_factura
                    for serie in series:
                        if online is not None:
                            if serie.online == online:
                                doc_series.append(serie.serie_factura)
                        else:
                            doc_series.append(serie.serie_factura)
            else:
                comprobante = frappe.get_doc("Tipos de Comprobante", "Boleta de Venta")
                if contingencia == "1":
                    series = configuracion.serie_boleta_contingencia
                    for serie in series:
                        doc_series.append(serie.serie_boleta_contingencia)
                else:
                    series = configuracion.serie_boleta
                    for serie in series:
                        if online is not None:
                            if serie.online == online:
                                doc_series.append(serie.serie_boleta)
                        else:
                            doc_series.append(serie.serie_boleta)
    elif doctype == "Fees":
        if is_return == "1":
            comprobante = frappe.get_doc("Tipos de Comprobante", "Nota de Crédito")
            if contingencia == "1":
                series = configuracion.serie_nota_credito_contingencia
                if codigo_tipo_documento == "6":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_credito_contingencia)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_credito_contingencia)
            else:
                series = configuracion.serie_nota_credito
                if codigo_tipo_documento == "6":
                    for serie in series:
                        if serie.comprobante == "Factura":
                            doc_series.append(serie.serie_nota_credito)
                else:
                    for serie in series:
                        if serie.comprobante == "Boleta":
                            doc_series.append(serie.serie_nota_credito)
        else:
            if codigo_tipo_documento == "6":
                comprobante = frappe.get_doc("Tipos de Comprobante", "Factura")
                if contingencia == "1":
                    series = configuracion.serie_factura_contingencia
                    for serie in series:
                        doc_series.append(serie.serie_factura_contingencia)
                else:
                    series = configuracion.serie_factura
                    for serie in series:
                        doc_series.append(serie.serie_factura)
            else:
                comprobante = frappe.get_doc("Tipos de Comprobante", "Boleta de Venta")
                if contingencia == "1":
                    series = configuracion.serie_boleta_contingencia
                    for serie in series:
                        doc_series.append(serie.serie_boleta_contingencia)
                else:
                    series = configuracion.serie_boleta
                    for serie in series:
                        doc_series.append(serie.serie_boleta)
    elif doctype == "Delivery Note":
        comprobante = frappe.get_doc("Tipos de Comprobante", "Guía de remisión - Remitente")
        series = configuracion.serie_guia_remision
        for serie in series:
            doc_series.append(serie.serie_guia_remision)
    return {"codigo": comprobante.codigo_tipo_comprobante, "descripcion": comprobante.name, "series": doc_series}
