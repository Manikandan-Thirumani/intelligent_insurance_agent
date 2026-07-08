from __future__ import annotations

import os
from pathlib import Path

UPLOAD_DIR = Path(os.getenv("INSURANCE_UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
