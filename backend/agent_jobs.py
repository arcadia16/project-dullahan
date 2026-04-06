import shutil
import asyncio
import uuid
from pathlib import Path
from typing import Optional
import aiofiles

from config import JOBS_BASE_DIR, HASHCAT_BIN, WORDLIST_PATH

jobs = {}
jobs_lock = asyncio.Lock()


# TODO: add --username functionality to hashcat job
async def create_job(
    hash_file_content: str,
    hash_type: int = 1000,
    attack_mode: int = 0,
    extra_flags: str = "-O",
) -> str:
    job_id = str(uuid.uuid4())
    async with jobs_lock:
        jobs[job_id] = {
            "id": job_id,
            "hash_file_content": hash_file_content,
            "hash_type": hash_type,
            "attack_mode": attack_mode,
            "extra_flags": extra_flags,
            "status": "created",
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "potfile_content": None,
            "process": None,
            "workdir": None,
        }
    return job_id


async def get_job(job_id: str) -> Optional[dict]:
    async with jobs_lock:
        return jobs.get(job_id)


async def update_job(job_id: str, **kwargs):
    async with jobs_lock:
        if job_id in jobs:
            jobs[job_id].update(kwargs)


async def run_hashcat_agent(job_id: str):
    job = await get_job(job_id)
    if not job:
        return

    workdir = Path(JOBS_BASE_DIR) / job_id
    workdir.mkdir(parents=True, exist_ok=True)
    hash_file = workdir / "hashes.txt"
    potfile = workdir / "hashcat.potfile"

    async with aiofiles.open(hash_file, "w") as f:
        await f.write(job["hash_file_content"])

    cmd = (
        f"{HASHCAT_BIN} -m {job['hash_type']} -a {job['attack_mode']} "
        f"{hash_file} {WORDLIST_PATH} {job['extra_flags']} "
        f"--potfile-path {potfile}"
    )

    await update_job(job_id, status="running", workdir=str(workdir))

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
        cwd=str(workdir),
    )
    await update_job(job_id, process=process)
    exit_code = await process.wait()

    pot_content = ""
    if potfile.exists():
        async with aiofiles.open(potfile, "r") as pf:
            pot_content = await pf.read()

    final_status = "done" if pot_content.strip() else "failed"

    await update_job(
        job_id,
        status=final_status,
        exit_code=exit_code,
        potfile_content=pot_content,
        # TODO: remove stdout/stderr from here and from dataclass
        stdout="",
        stderr="",
    )
    try:
        shutil.rmtree(workdir)
        print(f"[INFO] Removed workdir {workdir}")
    except Exception as e:
        print(f"[WARN] Failed to remove workdir {workdir}: {e}")
