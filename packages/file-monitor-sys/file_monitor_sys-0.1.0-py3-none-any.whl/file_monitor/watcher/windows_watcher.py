import win32file  # type: ignore
import win32con   # type: ignore
import os
from integrity.verifier import verify_file
from alerts.notifier import log_event, send_email_alert
from access.user_finder import get_last_user_for_file

ACTIONS = {
    1: "CREATED",
    2: "DELETED",
    3: "UPDATED",
    4: "RENAMED_FROM",
    5: "RENAMED_TO"
}

# 🔐 Replace with your actual authorized usernames (lowercase recommended)
AUTHORIZED_USERS = ["john","desktop-ct77ebu\dell"]  # ← Keep these lowercase

def start_watch(path):
    print(f"Monitoring directory: {path}")
    
    FILE_LIST_DIRECTORY = 0x0001

    hDir = win32file.CreateFile(
        path,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    while True:
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )

        for action, filename in results:
            full_path = os.path.join(path, filename)

            # 🚫 Skip the alert log file itself to prevent infinite loops
            if "alerts.log" in full_path:
                continue

            event_type = ACTIONS.get(action, "UNKNOWN")
            #user = get_last_user_for_file(full_path)
            user = get_last_user_for_file(full_path)
            print(f"[DEBUG] Detected user: {user!r}")

            normalized_user = user.strip().lower()

            # 🐛 Debug print
            print(f"[DEBUG] Detected user: {normalized_user!r}")

            # 🛡️ Check if the user is unauthorized
            if normalized_user not in [u.lower() for u in AUTHORIZED_USERS]:
                msg = f"⚠️ Unauthorized {event_type} → {full_path} (by {user})"
                log_event("UNAUTHORIZED_ACCESS", msg)
                send_email_alert("⚠️ Unauthorized Access Detected", msg)
                continue

            # 🔍 Integrity check for updates
            if event_type == "UPDATED":
                if not verify_file(full_path):
                    log_event("INTEGRITY_FAIL", f"File updated: {full_path} (by {user})")
                else:
                    log_event("UPDATED", f"{event_type} → {full_path} (by {user})")
            else:
                log_event(event_type, f"{event_type} → {full_path} (by {user})")


#user = get_last_user_for_file(full_path)
#print(f"[DEBUG] Detected user: {user!r}")
