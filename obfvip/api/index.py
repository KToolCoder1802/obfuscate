from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import io
import base64
import zlib

app = FastAPI()

def obfuscate_code(code: str) -> str:
    compressed = zlib.compress(code.encode())
    encoded = base64.b64encode(compressed).decode()
    return f"import base64,zlib\nexec(zlib.decompress(base64.b64decode('{encoded}')))"

@app.get("/")
async def root():
    return {"status": "ok", "message": "API is working"}

@app.post("/obfuscate")
async def obfuscate(file: UploadFile = File(...)):
    try:
        code = (await file.read()).decode('utf-8', errors='ignore')
        result = obfuscate_code(code)
        return StreamingResponse(
            io.BytesIO(result.encode('utf-8')),
            media_type="text/x-python",
            headers={"Content-Disposition": f"attachment; filename=obfuscated_{file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))