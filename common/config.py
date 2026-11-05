"""
config.py -- Credentials and endpoint selection (Component: config_secrets)

Loads cTrader Open API credentials from the project-root `.env` file
into an immutable Settings object, and resolves which Open API host
(demo or live) the scripts should connect to.

Invariants:
    - Secrets come only from the environment / `.env`; never hard-coded.
    - Demo is the default host. Live must be opted into explicitly via
      CTRADER_HOST=live so a sandbox script cannot touch real money by
      accident.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Project root is one level above this package; `.env` sits there.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

_REQUIRED_VARS = (
    "CTRADER_CLIENT_ID",
    "CTRADER_CLIENT_SECRET",
    "CTRADER_ACCESS_TOKEN",
    "CTRADER_ACCOUNT_ID",
)


@dataclass(frozen=True)
class Settings:
    """
    Immutable snapshot of the credentials a script needs to connect.

    The custom __repr__ keeps secrets out of tracebacks and accidental
    print() calls.
    """

    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    account_id: int
    host_type: str  # 'demo' | 'live'

    def __repr__(self) -> str:
        return (
            f"Settings(client_id={self.client_id[:6]}..., "
            f"account_id={self.account_id}, host_type={self.host_type!r})"
        )

    @property
    def host(self) -> str:
        """
        Return the Open API protobuf host for the selected environment.

        Returns
        -------
        str
            Demo or live hostname from the SDK's EndPoints constants.
        """
        # Imported lazily so config can be loaded without Twisted set up.
        from ctrader_open_api import EndPoints

        if self.host_type == "live":
            return EndPoints.PROTOBUF_LIVE_HOST
        return EndPoints.PROTOBUF_DEMO_HOST

    @property
    def port(self) -> int:
        """Return the Open API protobuf port (same for demo and live)."""
        from ctrader_open_api import EndPoints

        return EndPoints.PROTOBUF_PORT


def load_settings(env_file: Path | None = None) -> Settings:
    """
    Load credentials from `.env` (or the process environment).

    Parameters
    ----------
    env_file : Path, optional
        Alternative dotenv file. Defaults to `<project root>/.env`.

    Returns
    -------
    Settings
        Validated credentials and host selection.

    Raises
    ------
    RuntimeError
        If any required variable is missing or CTRADER_HOST is invalid.
    """
    load_dotenv(env_file or PROJECT_ROOT / ".env")

    missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

    host_type = os.getenv("CTRADER_HOST", "demo").lower()
    if host_type not in {"demo", "live"}:
        raise RuntimeError("CTRADER_HOST must be 'demo' or 'live'")

    return Settings(
        client_id=os.environ["CTRADER_CLIENT_ID"],
        client_secret=os.environ["CTRADER_CLIENT_SECRET"],
        access_token=os.environ["CTRADER_ACCESS_TOKEN"],
        # Optional: only needed once the access token expires.
        refresh_token=os.getenv("CTRADER_REFRESH_TOKEN", ""),
        account_id=int(os.environ["CTRADER_ACCOUNT_ID"]),
        host_type=host_type,
    )
