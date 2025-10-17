import uvicorn
from fastapi import FastAPI

app = FastAPI(title="NTLM Audit Tool", version="0.0.1")

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

def launch():
     uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
