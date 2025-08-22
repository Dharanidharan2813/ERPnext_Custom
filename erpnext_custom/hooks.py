app_name = "erpnext_custom"
app_title = "Erpnext Custom"
app_publisher = "Dharanidharan-velmurugan"
app_description = "Customization "
app_email = "dharanidharans1328@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "erpnext_custom",
# 		"logo": "/assets/erpnext_custom/logo.png",
# 		"title": "Erpnext Custom",
# 		"route": "/erpnext_custom",
# 		"has_permission": "erpnext_custom.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_custom/css/erpnext_custom.css"
# app_include_js = "/assets/erpnext_custom/js/erpnext_custom.js"

app_include_js = "/assets/your_app/js/sales_invoice.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_custom/css/erpnext_custom.css"
# web_include_js = "/assets/erpnext_custom/js/erpnext_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "erpnext_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "erpnext_custom.utils.jinja_methods",
# 	"filters": "erpnext_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnext_custom.install.before_install"
# after_install = "erpnext_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpnext_custom.uninstall.before_uninstall"
# after_uninstall = "erpnext_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "erpnext_custom.utils.before_app_install"
# after_app_install = "erpnext_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "erpnext_custom.utils.before_app_uninstall"
# after_app_uninstall = "erpnext_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_custom.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

doc_events = {
    "Sales Order": {
        "on_submit": "erpnext_custom.sales_order_custom.handle_vip_sales_order",
        "on_update": "erpnext_custom.erpnext_custom.doc_event.sales_order.validate_sales_order"
    },
    "Sales Invoice": {
        "before_insert": "erpnext_custom.erpnext_custom.doc_event.sales_order.validate_sales_invoice",
        "on_submit": "erpnext_custom.utils.check_vip_customer"
        
    }
}


# Scheduled Tasks
# ---------------


# scheduler_events = {
# 	"all": [
# 		"erpnext_custom.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"erpnext_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "erpnext_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["erpnext_custom.utils.before_request"]
# after_request = ["erpnext_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["erpnext_custom.utils.before_job"]
# after_job = ["erpnext_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpnext_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

after_migrate = [
    "erpnext_custom.i.load_workflows_from_fixtures",
    "erpnext_custom.install.load_workflows_from_fixtures"

]



