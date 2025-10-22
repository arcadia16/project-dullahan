import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routers import r_audit
from .models.audit_models import AuditRequest

"""
                                                 ,  ,
                                               / \/ \
                                              (/ //_ \_
     .-._                                      \||  .  \
      \  '-._                            _,:__.-"/---\_ \
 ______/___  '.    .--------------------'~-'--.)__( , )\ \
`'--.___  _\  /    |             Here        ,'    \)|\ `\|
     /_.-' _\ \ _:,_          Be Dragons           " ||   (
   .'__ _.' \'-/,`-~`                                |/
       '. ___.> /=,|  Abandon hope all ye who enter  |
        / .-'/_ )  '---------------------------------'
        )'  ( /(/
             \\ "
              '=='
"""

origins = [
     "http://localhost:5173",
     "http://127.0.0.1:5173"
]

app = FastAPI(title="NTLM Audit Tool", version="0.0.1")
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

"""
Somehow this (V) stopped working a day after.
app.mount("/static", StaticFiles(directory="static"), name="static")
"""
from pathlib import Path
parent_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(parent_dir)), name="static")

app.include_router(r_audit.router)

@app.get("/")
async def root():
     return {"message": "Hello from Dullahan!"}

def launch():
     uvicorn.run("backend.app:app", host="0.0.0.0", port=5000, reload=True)
