from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import uvicorn
from src.new_main import run_main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", response_class=PlainTextResponse)
async def upload(email: str = Form(...), files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    # Read files into memory
    file_data = [(f.filename, await f.read()) for f in files]

    try:
        run_main(file_data, email)  # call main script directly
        return "Done"
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Processing failed.")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
