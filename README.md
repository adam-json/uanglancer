# Upwork Tracker

A personal Python tool that reads my Upwork transaction report, calculates earnings, fees, and Connects spending, and converts everything to IDR.

## Features

- Auto-detects the newest report from Downloads
- Computes gross, fees, Connects, and net earnings
- Fetches live USD → IDR exchange rate
- Saves a summary to `output/summary.txt`

## How to run

- python -m pip install pandas requests
- python tracker.py
