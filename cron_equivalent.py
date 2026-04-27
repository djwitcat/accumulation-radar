#!/usr/bin/env python3

import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run_job(mode, log_name):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] run {mode}")
    with open(BASE_DIR / log_name, "a", encoding="utf-8") as f:
        subprocess.run(
            [sys.executable, "accumulation_radar.py", mode],
            cwd=BASE_DIR,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=False,
        )
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] done {mode}")


def next_pool_run(now):
    target = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return target


def next_oi_run(now):
    target = now.replace(minute=30, second=0, microsecond=0)
    if now >= target:
        target += timedelta(hours=1)
    return target


next_pool = next_pool_run(datetime.now())
next_oi = next_oi_run(datetime.now())

print(f"next pool: {next_pool.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"next oi:   {next_oi.strftime('%Y-%m-%d %H:%M:%S')}")


while True:
    now = datetime.now()

    if now >= next_pool:
        run_job("pool", "accumulation.log")
        next_pool = next_pool_run(datetime.now())
        print(f"next pool: {next_pool.strftime('%Y-%m-%d %H:%M:%S')}")

    if now >= next_oi:
        run_job("oi", "accumulation_oi.log")
        next_oi = next_oi_run(datetime.now())
        print(f"next oi:   {next_oi.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(5)
