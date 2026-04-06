from fastapi import Header, HTTPException
from pydantic import BaseModel
from typing import Optional

# These will be set from config at runtime
AGENT_API_KEY = None


def set_api_keys(agent_key: str):
    global AGENT_API_KEY
    AGENT_API_KEY = agent_key


async def verify_agent_key(x_api_key: str = Header(...)):
    if x_api_key != AGENT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True


# Shared response models
class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    exit_code: Optional[int] = None
    potfile_ready: bool = False


class PotfileResponse(BaseModel):
    potfile: str
