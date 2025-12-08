# Ensure that the `src` directory is on sys.path when running tests.
# This allows imports like `from prompt_lab...` to work under pytest.

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
