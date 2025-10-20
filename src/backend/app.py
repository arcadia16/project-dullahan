import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="NTLM Audit Tool", version="0.0.1")
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

class DataTest(BaseModel):
     msg: int

# poetry run main, look at pyproject.toml
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

@app.get("/")
async def root():
     return {"message": "Hello from Dullahan!"}

@app.post("/start/")
async def get_post_data(data: DataTest):
     print(data.msg)
     return {"msg": "api accepted data"}

def launch():
     uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
