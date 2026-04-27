#!/usr/bin/env python3

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
last_pool = None
last_oi = None


def run_job(mode, log_name):
    with open(BASE_DIR / log_name, "a", encoding="utf-8") as f:
        subprocess.run(
            [sys.executable, "accumulation_radar.py", mode],
            cwd=BASE_DIR,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=False,
        )


while True:
    now = datetime.now()

    pool_key = now.strftime("%Y-%m-%d")
    if now.hour == 10 and now.minute == 0 and last_pool != pool_key:
        run_job("pool", "accumulation.log")
        last_pool = pool_key

    oi_key = now.strftime("%Y-%m-%d %H")
    if now.minute == 30 and last_oi != oi_key:
        run_job("oi", "accumulation_oi.log")
        last_oi = oi_key

    time.sleep(20)
