# cTrader Open API — Python SDK sandbox

Fast learning playground for [`ctrader-open-api`](https://github.com/spotware/OpenApiPy).
Scripts here are small, self-contained experiments; what proves useful is
later ported into forex algorithmic trading systems.

## Layout

```

├── common/                 # shared helpers imported by every script
│   └── config.py           # loads .env -> Settings (host, port, creds)
├── data/                   # local dumps (gitignored)
├── notebooks/              # exploratory analysis of downloaded data
├── notes/                  # learnings, gotchas, message-flow notes
├── scripts/                # one folder per Open API topic, in learning order
│   ├── 01_auth/            # app + account auth, token refresh
│   ├── 02_accounts/        # account list, trader info, balance
│   ├── 03_symbols/         # symbol list, symbol details, asset classes
│   ├── 04_market_data/     # trendbars (OHLC), tick data history
│   ├── 05_trading/         # market/limit/stop orders, SL/TP, close, reconcile
│   └── 06_streaming/       # live spot subscriptions, execution events
├── environment.yml         # conda env (also installs `common` in editable mode)
└── .env                    # credentials (gitignored)
```

Script naming: `<topic>/<verb>_<thing>.py`, e.g. `04_market_data/fetch_trendbars.py`.

## Setup

```bash
conda env create -f environment.yml     # first time
conda env update -f environment.yml     # after dependency changes
conda activate ctrader_open_api_python_sdk
```

`.env` must define `CTRADER_CLIENT_ID`, `CTRADER_CLIENT_SECRET`,
`CTRADER_ACCESS_TOKEN`, `CTRADER_REFRESH_TOKEN`, `CTRADER_ACCOUNT_ID`.
Optional: `CTRADER_HOST=demo|live` (defaults to `demo`).

## Running a script

Always from the project root:

```bash
python scripts/01_auth/verify_auth.py
```

Inside a script:

```python
from common import load_settings

settings = load_settings()
client = Client(settings.host, settings.port, TcpProtocol)
```
