# watcher/cross_platform_watcher.py

import time
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alerts.notifier import log_event

AUTHORIZED_USERS = ["balaji", "mounikanagapuri"]  # Add authorized usernames here

class WatcherHandler(FileSystemEventHandler):
    # def dispatch(self, event):
    #     event_type = None

    #     if event.event_type == "created":
    #         event_type = "CREATED"
    #     elif event.event_type == "deleted":
    #         event_type = "DELETED"
    #     elif event.event_type == "modified":
    #         event_type = "MODIFIED"

    #     if event_type:
    #         username = getpass.getuser()
    #         auth_status = ("authorized user" if username in AUTHORIZED_USERS else "UNAUTHORIZED user")
    #         message = f"{event_type.capitalize()}: {event.src_path} by {auth_status}: {username}"
    #         log_event(event_type, message)
        
    def dispatch(self, event):
        event_type = None

        if event.event_type == "created":
            event_type = "CREATED"
        elif event.event_type == "deleted":
            event_type = "DELETED"
        elif event.event_type == "modified":
            event_type = "MODIFIED"

        if event_type:
            username = getpass.getuser()
            auth_status = ("authorized user" if username in AUTHORIZED_USERS else "UNAUTHORIZED user")
            message = f"{event_type.capitalize()}: {event.src_path} by {auth_status}: {username}"

            # Send email only for critical changes
            alert = event_type in ["CREATED", "DELETED"]
            log_event(event_type, message, alert=alert)


def start_watch(path="."):
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"\U0001F441️  Watching {path}... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()





#previous code
#  # watcher/cross_platform_watcher.py

# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from alerts.notifier import log_event  # ✅ Use central logging + email alerts

# class WatcherHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         log_event("MODIFIED", f"Modified: {event.src_path}")

#     def on_created(self, event):
#         log_event("CREATED", f"Created: {event.src_path}")

#     def on_deleted(self, event):
#         log_event("DELETED", f"Deleted: {event.src_path}")

# def start_watch(path="."):
#     event_handler = WatcherHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     print(f"👁️  Watching {path}... Press Ctrl+C to stop.")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()


# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from alerts.notifier import log_event  # ✅ Import the logging and email alert function


# class WatcherHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         log_event("MODIFIED", f"Modified: {event.src_path}")  # ✅ Log and optionally email

#     def on_created(self, event):
#         log_event("CREATED", f"Created: {event.src_path}")  # ✅ Log

#     def on_deleted(self, event):
#         log_event("DELETED", f"Deleted: {event.src_path}")  # ✅ Log + Email


# def start_watch(path="."):
#     event_handler = WatcherHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     print(f"Watching {path}... Press Ctrl+C to stop.")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
