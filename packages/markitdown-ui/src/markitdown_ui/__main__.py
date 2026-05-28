# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path

from streamlit.web import cli as stcli

APP_PATH = Path(__file__).resolve().parent / "app.py"


def main() -> None:
    sys.argv = ["streamlit", "run", str(APP_PATH), *sys.argv[1:]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
