#
# AI-on-Rails: All rights reserved.
#

import sys
from .cli import cli
from .utils.ui import UI

# Create UI instance
ui = UI()


def main():
    """Entry point for the AOR CLI."""
    try:
        cli()
    except Exception as e:
        ui.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
