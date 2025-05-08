"""API Implemenation for the Customizer to start and control the payload processing."""

import logging
import os
import signal
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from pyxecm.customizer.api.auth.functions import get_authorized_user
from pyxecm.customizer.api.auth.models import User
from pyxecm.customizer.api.common.functions import PAYLOAD_LIST
from pyxecm.customizer.api.common.models import CustomizerStatus

router = APIRouter(tags=["default"])

logger = logging.getLogger("pyxecm.customizer.api.common")


@router.get("/", include_in_schema=False)
async def redirect_to_api() -> RedirectResponse:
    """Redirect from / to /api.

    Returns:
        None

    """
    return RedirectResponse(url="/api")


@router.get(path="/status", name="Get Status")
async def get_status() -> CustomizerStatus:
    """Get the status of the Customizer."""

    df = PAYLOAD_LIST.get_payload_items()

    if df is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Payload list is empty.",
        )

    all_status = df["status"].value_counts().to_dict()

    return CustomizerStatus(
        version=2,
        customizer_duration=(all_status.get("running", None)),
        customizer_end_time=None,
        customizer_start_time=None,
        status_details=all_status,
        status="Running" if "running" in all_status else "Stopped",
        debug=df["log_debug"].sum(),
        info=df["log_info"].sum(),
        warning=df["log_warning"].sum(),
        error=df["log_error"].sum(),
        critical=df["log_critical"].sum(),
    )


@router.get("/api/shutdown", include_in_schema=False)
def shutdown(user: Annotated[User, Depends(get_authorized_user)]) -> JSONResponse:
    """Endpoint to end the application."""

    logger.warning(
        "Shutting down the API - Requested via api by user -> %s",
        user.id,
    )
    os.kill(os.getpid(), signal.SIGTERM)

    return JSONResponse({"status": "shutdown"}, status_code=HTTPStatus.ACCEPTED)
