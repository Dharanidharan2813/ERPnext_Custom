import frappe
import requests
from frappe import _
def send_telegram_message(chat_id, text, parse_mode="HTML", buttons=None):
    token = frappe.get_conf().get("telegram_bot_token")
    if not token:
        frappe.throw("Telegram Bot Token is not configured")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }

    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        frappe.log_error(response.text, "Telegram Send Error")

    return response.json()
