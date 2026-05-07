from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import io
import base64
import zlib
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Fallback obfuscate function
def fallback_obfuscate(code: str) -> str:
    compressed = zlib.compress(code.encode())
    encoded = base64.b64encode(compressed).decode()
    return f"import base64,zlib\nexec(zlib.decompress(base64.b64decode('{encoded}')))"

# Thử import PYMEO nếu có
try:
    from pymeo import obfuscate
    print("[OK] PYMEO loaded", flush=True)
except ImportError:
    obfuscate = fallback_obfuscate
    print("[WARN] Using fallback obfuscator", flush=True)

@app.get("/")
async def root():
    return {"status": "ok", "message": "PYMEO Obfuscator API on FastAPI"}

@app.post("/obfuscate")
async def obfuscate_endpoint(
    file: UploadFile = File(...),
    mode: int = Form(2),
    more_obf: bool = Form(False),
    antidebug: bool = Form(True),
    anticrack: bool = Form(True),
    username: str = Form("API_USER")
):
    try:
        code = (await file.read()).decode('utf-8', errors='ignore')
        
        # Gọi obfuscate (PYMEO hoặc fallback)
        result = obfuscate(code, mode, more_obf, antidebug, anticrack, username)
        
        # Trả về file
        return StreamingResponse(
            io.BytesIO(result.encode('utf-8')),
            media_type="text/x-python",
            headers={"Content-Disposition": f"attachment; filename=obfuscated_{file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel handler
handler = app