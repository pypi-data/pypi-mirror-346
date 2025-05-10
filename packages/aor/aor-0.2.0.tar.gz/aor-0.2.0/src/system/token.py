#
# AI-on-Rails: All rights reserved.
#

import os


def get_token() -> str | None:
    """
    Get the token from the home folder.
    """
    try:
        home = os.path.expanduser("~")
        token_file = os.path.join(home, ".aor", "token")
        with open(token_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_token(token: str):
    """
    Save the token in the home folder.
    """
    try:
        home = os.path.expanduser("~")
        token_file = os.path.join(home, ".aor", "token")
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, "w") as f:
            f.write(token)
    except Exception as e:
        raise RuntimeError(f"Failed to save token: {token_file}: {e}")
