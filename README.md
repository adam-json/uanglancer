# Upwork Tracker

A Python tool for Indonesian Upwork freelancers. Reads your Upwork transaction report, calculates earnings, fees, and Connects spending, converts to IDR, and estimates tax.

Runs as both a command-line tool and a Streamlit web app.

![Dashboard](screenshot.png)

## Features

- Auto-detects newest report from Downloads
- Computes gross, fees, Connects, net
- Live USD → IDR rate
- Month-by-month net
- Tax estimate: UMKM 0.5% and NPPN
- Saves summary to `output/summary.txt`
- Web UI with charts

## How to run

Install once:

```
python -m pip install -r requirements.txt
```

Command line:

```
python tracker.py
```

Web app:

```
python -m streamlit run app.py
```

## How to get your CSV

Upwork → Reports → Transaction History → set dates → Export → CSV. It lands in Downloads.

## Project structure

```
upwork-tracker/
├── app.py
├── tracker.py
├── data/
├── output/
├── requirements.txt
└── README.md
```

## Tax note

Estimates only. Verify with a konsultan pajak before filing.

## License

MIT