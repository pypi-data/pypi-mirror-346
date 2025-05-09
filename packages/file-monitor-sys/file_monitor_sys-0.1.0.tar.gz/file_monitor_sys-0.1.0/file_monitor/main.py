import platform
import os
from watcher.cross_platform_watcher import start_watch

#  Update this to any folder you want to monitor
path_to_monitor = "C:\\Users\\DELL\\Documents"


import platform

# Optional: print OS info
print(f"OS Detected: {platform.system()}")

# Dynamically choose watcher based on OS
if platform.system() == "Windows":
    from watcher.windows_watcher import start_watch
else:
    from watcher.cross_platform_watcher import start_watch

if __name__ == "__main__":
    start_watch("/Users/balaji/Documents/temp")  # Watch current directory
