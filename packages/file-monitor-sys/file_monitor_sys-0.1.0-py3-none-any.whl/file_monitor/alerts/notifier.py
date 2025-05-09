# alerts/notifier.py

from datetime import datetime
from utils.config import EMAIL_CONFIG
import yagmail
from colorama import Fore, Style, init

init(autoreset=True)

ICONS = {
    "CREATED": "📁",
    "DELETED": "🗑️",
    "MODIFIED": "✏️",
    "INTEGRITY_FAIL": "⚠️",
    "DEFAULT": "ℹ️"
}

def send_email_alert(event_type, message):
    try:
        yag = yagmail.SMTP(EMAIL_CONFIG["sender"], EMAIL_CONFIG["app_password"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"⚠️ Alert: {event_type}"
        body = f"{message}\n\nTimestamp: {timestamp}"
        yag.send(to=EMAIL_CONFIG["recipient"], subject=subject, contents=body)
        print(f"{Fore.GREEN}✅ Email alert sent.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to send email: {e}{Style.RESET_ALL}")

def colorize_event(event_type):
    if event_type == "CREATED":
        return f"{Fore.GREEN}{event_type}{Style.RESET_ALL}"
    elif event_type == "DELETED":
        return f"{Fore.RED}{event_type}{Style.RESET_ALL}"
    elif event_type == "MODIFIED":
        return f"{Fore.YELLOW}{event_type}{Style.RESET_ALL}"
    elif event_type == "INTEGRITY_FAIL":
        return f"{Fore.MAGENTA}{event_type}{Style.RESET_ALL}"
    else:
        return f"{Fore.CYAN}{event_type}{Style.RESET_ALL}"

def style_timestamp(ts):
    return f"{Fore.CYAN}{Style.DIM}{ts}{Style.RESET_ALL}"

def style_path(path):
    return f"{Style.BRIGHT}{Fore.WHITE}{path}{Style.RESET_ALL}"

def log_event(event_type, message, alert=False):
    """
    Logs the event to console and file. Sends email if alert=True.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colored_type = colorize_event(event_type)
    icon = ICONS.get(event_type, ICONS["DEFAULT"])

    # Extract path from message for pretty output
    if ":" in message:
        prefix, raw_path = message.split(":", 1)
        styled_message = f"{prefix.strip()}: {style_path(raw_path.strip())}"
    else:
        styled_message = message

    log_line = f"[{style_timestamp(timestamp)}] {icon} {colored_type}: {styled_message}"
    print(log_line)

    # Log plain text to file
    with open("alerts.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {event_type}: {message}\n")

    if alert:
        send_email_alert(event_type, message)


#previous code
# # alerts/notifier.py

# from datetime import datetime
# from utils.config import EMAIL_CONFIG
# import yagmail
# from colorama import Fore, Style, init

# init(autoreset=True)

# ICONS = {
#     "CREATED": "📁",
#     "DELETED": "🗑️",
#     "MODIFIED": "✏️",
#     "INTEGRITY_FAIL": "⚠️",
#     "DEFAULT": "ℹ️"
# }

# def send_email_alert(event_type, message):
#     try:
#         yag = yagmail.SMTP(EMAIL_CONFIG["sender"], EMAIL_CONFIG["app_password"])
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         subject = f"⚠️ Alert: {event_type}"
#         body = f"{message}\n\nTimestamp: {timestamp}"
#         yag.send(to=EMAIL_CONFIG["recipient"], subject=subject, contents=body)
#         print(f"{Fore.GREEN}✅ Email alert sent.{Style.RESET_ALL}")
#     except Exception as e:
#         print(f"{Fore.RED}❌ Failed to send email: {e}{Style.RESET_ALL}")

# def colorize_event(event_type):
#     if event_type == "CREATED":
#         return f"{Fore.GREEN}{event_type}{Style.RESET_ALL}"
#     elif event_type == "DELETED":
#         return f"{Fore.RED}{event_type}{Style.RESET_ALL}"
#     elif event_type == "MODIFIED":
#         return f"{Fore.YELLOW}{event_type}{Style.RESET_ALL}"
#     elif event_type == "INTEGRITY_FAIL":
#         return f"{Fore.MAGENTA}{event_type}{Style.RESET_ALL}"
#     else:
#         return f"{Fore.CYAN}{event_type}{Style.RESET_ALL}"

# def style_timestamp(ts):
#     return f"{Fore.CYAN}{Style.DIM}{ts}{Style.RESET_ALL}"

# def style_path(path):
#     return f"{Style.BRIGHT}{Fore.WHITE}{path}{Style.RESET_ALL}"

# def log_event(event_type, message):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     colored_type = colorize_event(event_type)
#     icon = ICONS.get(event_type, ICONS["DEFAULT"])

#     # Extract path for styling
#     if ":" in message:
#         prefix, raw_path = message.split(":", 1)
#         styled_message = f"{prefix.strip()}: {style_path(raw_path.strip())}"
#     else:
#         styled_message = message

#     log_line = f"[{style_timestamp(timestamp)}] {icon} {colored_type}: {styled_message}"
#     print(log_line)

#     # Log plain version to file
#     with open("alerts.log", "a", encoding="utf-8") as f:
#         f.write(f"[{timestamp}] {event_type}: {message}\n")

#     if event_type in ["CREATED", "DELETED"]:
#         send_email_alert(event_type, message)
