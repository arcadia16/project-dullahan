from fastapi import FastAPI
import subprocess

# Create FastAPI app instance
app = FastAPI()

# Define a simple GET endpoint
@app.get("/")
async def read_root():
    output = subprocess.run(["./runme.sh"],
        shell=True, capture_output=True, text=True).stdout
    return {"hello": output.rstrip("\n")}