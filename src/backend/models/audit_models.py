from pydantic import BaseModel
from typing import Optional

class AuditRequest(BaseModel):
     domain: str
     controller_ip: str
     username: str
     hash: str
     wordlist_path: str