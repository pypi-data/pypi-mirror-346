#
# AI-on-Rails: All rights reserved.
#

import os


def get_credentials() -> tuple[str, str]:
    """
    Get the credentials from the home folder.
    """
    try:
        home = os.path.expanduser("~")
        credentials_file = os.path.join(home, ".aor", "credentials")
        with open(credentials_file, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None, None


def save_credentials(email: str, password: str):
    """
    Save the credentials in the home folder.
    """
    home = os.path.expanduser("~")
    credentials_file = os.path.join(home, ".aor", "credentials")
    os.makedirs(os.path.dirname(credentials_file), exist_ok=True)
    with open(credentials_file, "w") as f:
        f.write(f"{email}\n{password}")
