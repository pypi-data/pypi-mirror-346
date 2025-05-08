from datetime import datetime
from typing import Literal
from fastapi import APIRouter, Request

router = APIRouter(tags=["Status"], prefix="")


@router.get("/", operation_id="ping")
async def ping(request: Request) -> dict:
    """
    Returns 'OK' if the API is running.
    """
    return "OK"


@router.get("/time", operation_id="getTime")
async def time(type: Literal["iso", "unix"] = "iso") -> str:
    """
    Returns the current time in either ISO or Unix timestamp (seconds) format.
    """
    if type == "iso":
        return datetime.now().isoformat()
    elif type == "unix":
        return str(int(datetime.now().timestamp()))
