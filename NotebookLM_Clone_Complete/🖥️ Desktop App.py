#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add notebooklm_app to path
sys.path.insert(0, str(Path(__file__).parent / "notebooklm_app"))

# Run desktop app
from desktop_app import main
main()
