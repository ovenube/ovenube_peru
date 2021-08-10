# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ovenube_peru"
app_title = "Ovenube Peru"
app_publisher = "OVENUBE"
app_description = "Ovenube Module App for Peru"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jespinoza@ovenube.com"
app_license = "MIT"

fixtures = [
    "Catalogo de Existencias",
    "Motivos de Traslado",
    "Tipos de Documento de Identidad",
    "Tipos de Transporte",
    "Unidades de Medida",
    "Tipos de Operaciones",
    "Tipos de Existencia",
    "Tipos de Transaccion Sunat",
    "Tipos de Notas de Credito",
    "Tipos de Notas de Debito",
    "Tipos de Pago",
    "Tipos de Comprobante",
    "Departamento",
    "Provincia",
    "Distrito",
    "Custom Field",
    "Custom Script"
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ovenube_peru/css/ovenube_peru.css"
# app_include_js = "/assets/ovenube_peru/js/ovenube_peru.js"

# include js, css files in header of web template
# web_include_css = "/assets/ovenube_peru/css/ovenube_peru.css"
# web_include_js = "/assets/ovenube_peru/js/ovenube_peru.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice" : "public/js/sales_invoice.js",
    "Sales Order": "public/js/sales_order.js",
    "Quotation": "public/js/quotation.js",
    "Company": "public/js/company.js",
    "Customer": "public/js/customer.js",
    "Supplier": "public/js/supplier.js",
    "Driver": "public/js/driver.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Fees": "public/js/fees.js",
    "Item": "public/js/item.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Purchase Order": "public/js/purchase_order.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Student": "public/js/student.js",
    "Supplier": "public/js/supplier.js",
    "UOM": "public/js/uom.js",
}

doctype_list_js = {
    "Currency Exchange" : "public/js/currency_exchange_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ovenube_peru.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ovenube_peru.install.before_install"
# after_install = "ovenube_peru.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ovenube_peru.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
        "before_insert": "ovenube_peru.nubefact_integration.facturacion_electronica.set_electronic_invoice_fields",
		"before_submit": "ovenube_peru.nubefact_integration.facturacion_electronica.send_electronic_invoice",
	},
    "Payment Entry": {
        "before_submit": "ovenube_peru.nubefact_integration.facturacion_electronica.send_fees_invoice"
    },
    "Sales Order": {
        "validate": "ovenube_peru.nubefact_integration.utils.set_amount_billed"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"nubefact_integration.tasks.all"
# 	],
#    "daily": [
#        "nubefact_integration.tasks.daily"
#    ],
# 	"hourly": [
# 		"nubefact_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nubefact_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"nubefact_integration.tasks.monthly"
# 	]
    "cron": {
        "30 0 * * *":[
            "ovenube_peru.tasks.daily"
        ],
        "30 12 * * *":[
            "ovenube_peru.tasks.daily"
        ],
        "0 8 * * *":[
            "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate"
        ],
        "30 8 * * *":[
            "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate"
        ],
        "0 9 * * *":[
            "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate"
        ],
        "30 9 * * *":[
            "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate"
        ],
        "0 10 * * *":[
            "ovenube_peru.nubefact_integration.doctype.api_consultas.api_consultas.get_exchange_rate"
        ]
    }
}

# Testing
# -------

# before_tests = "ovenube_peru.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ovenube_peru.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ovenube_peru.task.get_dashboard_data"
# }
