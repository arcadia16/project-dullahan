import gzip
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from agent_jobs import create_job, get_job, update_job, run_hashcat_agent
from routers.shared import verify_agent_key, JobStatusResponse, PotfileResponse

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run")
async def agent_run(
    background_tasks: BackgroundTasks,
    hash_file: UploadFile = File(...),
    hash_type: int = Form(1000),
    attack_mode: int = Form(0),
    extra_flags: str = Form("-O -w 4"),
    _: bool = Depends(verify_agent_key),
):
    """
    Agent endpoint to receive a gzipped or plain hash file.
    """
    raw_data = await hash_file.read()

    # Check for gzip magic bytes
    is_gzipped = len(raw_data) >= 2 and raw_data[:2] == b"\x1f\x8b"
    if is_gzipped:
        try:
            decompressed = gzip.decompress(raw_data)
            hash_content = decompressed.decode()
        except Exception as e:
            raise HTTPException(400, f"Failed to decompress gzip data: {str(e)}")
    else:
        hash_content = raw_data.decode()

    # Create job in memory
    job_id = await create_job(hash_content, hash_type, attack_mode, extra_flags)

    # Launch background task to run hashcat
    background_tasks.add_task(run_hashcat_agent, job_id)

    return {"job_id": job_id, "status": "started"}


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def agent_status(job_id: str, _: bool = Depends(verify_agent_key)):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    pot_content = job.get("potfile_content")
    potfile_ready = bool(pot_content and pot_content.strip())

    return {
        "job_id": job_id,
        "status": job.get("status"),
        "exit_code": job.get("exit_code"),
        "potfile_ready": potfile_ready,
    }


@router.get("/potfile/{job_id}", response_model=PotfileResponse)
async def agent_potfile(job_id: str, _: bool = Depends(verify_agent_key)):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.get("status") != "done":
        raise HTTPException(400, f"Job not finished, status: {job.get('status')}")
    pot_content = job.get("potfile_content")
    if pot_content is None:
        raise HTTPException(404, "Potfile not found")
    return {"potfile": pot_content}


@router.post("/kill/{job_id}")
async def agent_kill(job_id: str, _: bool = Depends(verify_agent_key)):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    proc = job.get("process")
    if proc and job.get("status") == "running":
        proc.terminate()
        await update_job(job_id, status="killed")
        return {"message": "SIGTERM sent"}
    raise HTTPException(400, "Job not running or no process")
