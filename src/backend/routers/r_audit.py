import uuid
from fastapi import APIRouter, BackgroundTasks

from ..models.audit_models import AuditRequest, HashcatResult, AuditStatus

router = APIRouter(
    prefix="/api"
)

jobs = {}

@router.get("/")
async def index():
    return {}

@router.get("/status/{id}")
async def test(id: str):
    print(f"Got GET with {id}")
    return {"msg": id, "status": "finished"}

@router.post("/start/")
async def get_post_data(data: AuditRequest):
    print(f"[*] Audit start: {data.domain}/{data.username}:{data.hash} on {data.controller_ip} with {data.wordlist_path} wordlist.")
    return { "job_id": str(uuid.uuid4()) }