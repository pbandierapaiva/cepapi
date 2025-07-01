from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://redcap.unifesp.br"],  # Explicitly allow your domain
    allow_methods=["GET", "POST"],
    allow_credentials=True,
)


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
    # no cleanup necessary on shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/{cep}")
def get_address(cep: str):
    if len(cep) != 8 or not cep.isdigit():
        raise HTTPException(status_code=400, detail="CEP must be 8 numeric digits")
    
    if cep in cep_dict:
        return JSONResponse(content=cep_dict[cep])
    else:
        raise HTTPException(status_code=404, detail="CEP not found")


## Uncomment if running directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
