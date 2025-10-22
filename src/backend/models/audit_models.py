from pydantic import BaseModel
from typing import Optional

class AuditRequest(BaseModel):
     domain: str
     controller_ip: str
     username: str
     hash: str
     wordlist_path: str

class HashcatResult(BaseModel):
     cracked_count: int
     output_file: Optional[str] = None

class AuditStatus(BaseModel):
     job_id: str
     status: str
     message: Optional[str] = None
     results: Optional[HashcatResult] = None