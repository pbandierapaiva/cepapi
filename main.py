from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn


# Load data into a dictionary on startup for speed
cep_dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load CEP data at startup
    with open("ceps.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                cep = parts[0].strip()
                cidade = parts[1].strip()
                bairro = parts[2].strip()
                logradouro = parts[3].strip()
                cep_dict[cep] = {
                    "cidade": cidade,
                    "bairro": bairro,
                    "logradouro": logradouro
                }
    yield  # continue running app


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://redcap.unifesp.br",
        "https://redcap.unifesp.br:8000",
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/{cep}")
def get_address(cep: str):
    if len(cep) != 8 or not cep.isdigit():
        raise HTTPException(status_code=400, detail="CEP must be 8 numeric digits")
    
    if cep in cep_dict:
        return JSONResponse(content=cep_dict[cep])
    else:
        raise HTTPException(status_code=404, detail="CEP não enconttrado")


## Uncomment if running directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
