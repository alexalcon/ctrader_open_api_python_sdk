"""
verify_auth.py -- Credential check for the cTrader Open API (Stage 01)

cTrader Open API setup verification. Confirms that the registered 
application and the access token work against the cTrader demo 
environment. Runs three steps in order and then exits:

    1. Application auth  (ProtoOAApplicationAuthReq)
    2. List accounts     (ProtoOAGetAccountListByAccessTokenReq)
    3. Account auth      (ProtoOAAccountAuthReq), only if
       CTRADER_DEMO_ACCOUNT_ID is set

Invariants:
    - Connects to the DEMO host only. Never points at live.
    - Secrets are read from the .env file, never hardcoded.
    - Read-only: no orders or account changes are sent.
"""

import os
import sys

from dotenv import load_dotenv
from twisted.internet import reactor

from ctrader_open_api import Client, EndPoints, Protobuf, TcpProtocol
from ctrader_open_api.messages.OpenApiMessages_pb2 import (
    ProtoOAAccountAuthReq,
    ProtoOAApplicationAuthReq,
    ProtoOAErrorRes,
    ProtoOAGetAccountListByAccessTokenReq,
)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration -- all values come from the .env file
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()

# Application credentials from the Open API portal (Credentials > View).
CLIENT_ID: str = os.environ["CTRADER_CLIENT_ID"]
CLIENT_SECRET: str = os.environ["CTRADER_CLIENT_SECRET"]

# Access token from the application Playground (Get Token).
ACCESS_TOKEN: str = os.environ["CTRADER_ACCESS_TOKEN"]

# Optional. ctidTraderAccountId of the demo or live accounts; differs 
# from the login number shown in the cTrader app. Leave empty on the 
# first run and copy it from the account list this script prints.
ACCOUNT_ID: str = os.environ.get("CTRADER_DEMO_ACCOUNT_ID", "").strip()
# ACCOUNT_ID: str = os.environ.get("CTRADER_LIVE_ACCOUNT_ID", "").strip()

client = Client(
    EndPoints.PROTOBUF_DEMO_HOST,  # demo only for this stage
    EndPoints.PROTOBUF_PORT,
    TcpProtocol,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def stop(exit_message: str) -> None:
    """
    Print a final message and shut down the Twisted reactor.

    Parameters
    ----------
    exit_message : str
        Summary line shown before the script exits.
    """
    print(exit_message)
    client.stopService()
    if reactor.running:
        reactor.stop()


def raise_if_error(message) -> object:
    """
    Unpack a raw Protobuf response and stop on an API error.

    Parameters
    ----------
    message : ProtoMessage
        Raw envelope delivered to a Deferred callback.

    Returns
    -------
    object
        The typed response message (e.g. ProtoOAApplicationAuthRes).
    """
    response = Protobuf.extract(message)
    if isinstance(response, ProtoOAErrorRes):
        # Common causes: CH_CLIENT_AUTH_FAILURE (bad ID/secret),
        # CH_ACCESS_TOKEN_INVALID (expired or wrong token).
        stop(f"API error {response.errorCode}: {response.description}")
        return None
    return response


def on_failure(failure) -> None:
    """
    Errback for any request that times out or fails at transport level.

    Parameters
    ----------
    failure : twisted.python.failure.Failure
        Twisted failure wrapper describing the error.
    """
    stop(f"Request failed: {failure.getErrorMessage()}")


# ─────────────────────────────────────────────────────────────────────────────
# Authentication chain -- each step fires the next one on success
# ─────────────────────────────────────────────────────────────────────────────

def on_connected(_client) -> None:
    """Send application auth as soon as the TCP connection opens."""
    print("Connected to demo host.")
    request = ProtoOAApplicationAuthReq()
    request.clientId = CLIENT_ID
    request.clientSecret = CLIENT_SECRET
    deferred = client.send(request)
    deferred.addCallbacks(on_app_auth, on_failure)


# step 1: application authentication (ProtoOAApplicationAuthReq)
def on_app_auth(message) -> None:
    """Application accepted; request accounts linked to the token."""
    if raise_if_error(message) is None:
        return
    print("Step 1 OK: application authenticated.")
    request = ProtoOAGetAccountListByAccessTokenReq()
    request.accessToken = ACCESS_TOKEN
    deferred = client.send(request)
    deferred.addCallbacks(on_account_list, on_failure)


# step 2: get account list by access token (ProtoOAGetAccountListByAccessTokenReq)
def on_account_list(message) -> None:
    """Print every account the token can access, then auth one of them."""
    response = raise_if_error(message)
    if response is None:
        return
    print("Step 2 OK: accounts linked to this access token:")
    for account in response.ctidTraderAccount:
        kind = "LIVE" if account.isLive else "DEMO"
        print(
            f"  ctidTraderAccountId={account.ctidTraderAccountId}  "
            f"login={account.traderLogin}  type={kind}"
        )

    if not ACCOUNT_ID:
        stop(
            "Set CTRADER_DEMO_ACCOUNT_ID and CTRADER_LIVE_ACCOUNT_ID "
            "in .env to a DEMO and LIVE respectively matching the "
            "ctidTraderAccountId above, then run again."
        )
        return

    request = ProtoOAAccountAuthReq()
    request.ctidTraderAccountId = int(ACCOUNT_ID)
    request.accessToken = ACCESS_TOKEN
    deferred = client.send(request)
    deferred.addCallbacks(on_account_auth, on_failure)

# step 3: account authentication (ProtoOAAccountAuthReq)
def on_account_auth(message) -> None:
    """Account accepted; credentials are fully verified."""
    if raise_if_error(message) is None:
        return
    stop(f"Step 3 OK: account {ACCOUNT_ID} authenticated. Setup complete.")


def on_disconnected(_client, reason) -> None:
    """Report unexpected disconnects (normal shutdown also lands here)."""
    if reactor.running:
        stop(f"Disconnected: {reason.getErrorMessage()}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client.setConnectedCallback(on_connected)
    client.setDisconnectedCallback(on_disconnected)
    client.startService()
    reactor.run()
    sys.exit(0)
    