import asyncio
import tempfile
import shutil
import gzip
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles
import httpx

from config import AGENT_BASE_URL, AGENT_API_KEY
from routers.shared import JobStatusResponse, PotfileResponse

router = APIRouter(prefix="", tags=["orchestrator"])


async def extract_hashes(dit_path: Path, system_path: Path) -> str:
    """Runs secretsdump and returns NTLM hashes as string."""
    proc = await asyncio.create_subprocess_exec(
        "impacket-secretsdump",
        "-system",
        str(system_path),
        "-ntds",
        str(dit_path),
        "LOCAL",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"secretsdump failed: {stderr.decode()}")

    hashes = []
    for line in stdout.decode(errors="replace").splitlines():
        if ":::" in line and ":" in line:
            hashes.append(line)
    return "\n".join(hashes)


@router.post("/upload")
async def upload_files(
    dit_file: UploadFile = File(...), system_file: UploadFile = File(...)
):
    """
    Receives NTDS.dit and SYSTEM hive from Vue frontend.
    Extracts hashes, compresses them with gzip, forwards to agent.
    """
    temp_dir = Path(tempfile.mkdtemp())
    dit_path = temp_dir / str(dit_file.filename)
    system_path = temp_dir / str(system_file.filename)

    # Save uploaded files
    async with aiofiles.open(dit_path, "wb") as f:
        content = await dit_file.read()
        await f.write(content)
    async with aiofiles.open(system_path, "wb") as f:
        content = await system_file.read()
        await f.write(content)

    try:
        hashes_content = await extract_hashes(dit_path, system_path)
        if not hashes_content.strip():
            raise HTTPException(400, "No NTLM hashes found")
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(500, f"Hash extraction failed: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    # Compress the hash content
    compressed_data = gzip.compress(hashes_content.encode())

    # Forward to agent as multipart file upload
    async with httpx.AsyncClient() as client:
        files = {"hash_file": ("hashes.txt.gz", compressed_data, "application/gzip")}
        data = {"hash_type": 1000, "attack_mode": 0, "extra_flags": "-O -w 4"}
        try:
            resp = await client.post(
                f"{AGENT_BASE_URL}/agent/run",
                files=files,
                data=data,
                headers={"X-API-Key": AGENT_API_KEY},
                timeout=30.0,
            )
            resp.raise_for_status()
            agent_response = resp.json()
        except Exception as e:
            raise HTTPException(502, f"Agent communication failed: {str(e)}")

    return {"job_id": agent_response["job_id"], "status": "sent_to_agent"}


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_status(job_id: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{AGENT_BASE_URL}/agent/status/{job_id}",
                headers={"X-API-Key": AGENT_API_KEY},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(404, "Job not found on agent")
            raise HTTPException(502, f"Agent error: {e.response.text}")
        except Exception as e:
            raise HTTPException(502, f"Agent unreachable: {str(e)}")


@router.get("/results/{job_id}", response_model=PotfileResponse)
async def get_results(job_id: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{AGENT_BASE_URL}/agent/potfile/{job_id}",
                headers={"X-API-Key": AGENT_API_KEY},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(404, "Potfile not ready or job not found")
            raise HTTPException(502, f"Agent error: {e.response.text}")
        except Exception as e:
            raise HTTPException(502, f"Agent unreachable: {str(e)}")


@router.post("/kill/{job_id}")
async def kill_job(job_id: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{AGENT_BASE_URL}/agent/kill/{job_id}",
                headers={"X-API-Key": AGENT_API_KEY},
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(502, f"Agent unreachable: {str(e)}")
