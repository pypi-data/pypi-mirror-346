import subprocess
import re

def get_last_user_for_file(path):
    """
    Attempts to fetch the username of the last user who accessed or modified the file,
    using Windows Event Logs. Requires administrative privileges.
    """
    try:
        cmd = (
            'wevtutil qe Security /q:"*[System[Provider[@Name=\'Microsoft-Windows-Security-Auditing\']]]" '
            '/f:text /c:20'
        )
        output = subprocess.check_output(cmd, shell=True).decode(errors="ignore")

        # Extract usernames from event log lines like: "Account Name: dell"
        matches = re.findall(r'Account Name:\s+([^\s]+)', output)

        # Filter out SYSTEM, LOCAL SERVICE, etc. Keep likely real usernames
        valid_users = [u for u in matches if u.lower() not in ['system', 'localservice', 'networkservice']]

        if valid_users:
            return valid_users[-1].strip()  # return the last real user

    except subprocess.CalledProcessError as e:
        return f"Error retrieving user: {e}"

    return "Unknown"
