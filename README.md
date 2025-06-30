# 📮 CEP Lookup API

A FastAPI-based microservice that provides address information for Brazilian CEPs using a local `ceps.txt` file.

## 🚀 Features

- Accepts 8-digit CEPs via URL (e.g. `/01002010`)
- Returns address data: `cidade`, `bairro`, and `logradouro`
- Fast in-memory lookup
- Runs as a systemd service on Linux

---

## 🗂️ File Format (`ceps.txt`)

Each line must be tab-separated (`\t`), with at least 4 fields:

```
CEP         Cidade/UF       Bairro      Logradouro
01002010    São Paulo/SP    Sé          Praça do Patriarca
```

> Use `tr -s ' ' '\t'` to convert space-aligned text to tab-delimited if needed.

---

## 🐍 main.py (FastAPI App)

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

cep_dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    with open("ceps.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                cep, cidade, bairro, logradouro = map(str.strip, parts[:4])
                cep_dict[cep] = {
                    "cidade": cidade,
                    "bairro": bairro,
                    "logradouro": logradouro
                }
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/{cep}")
def get_address(cep: str):
    if len(cep) != 8 or not cep.isdigit():
        raise HTTPException(status_code=400, detail="CEP must be 8 numeric digits")
    if cep in cep_dict:
        return JSONResponse(content=cep_dict[cep])
    else:
        raise HTTPException(status_code=404, detail="CEP not found")
```

---

## 🔧 Systemd Service Setup

1. Create a service file:

```ini
# /etc/systemd/system/cepapi.service
[Unit]
Description=FastAPI CEP Lookup Service
After=network.target

[Service]
User=paiva
WorkingDirectory=/________________/cepapi
ExecStart=/________________/cepapi/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

2. Reload and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now cepapi.service
```

3. Monitor logs:

```bash
journalctl -u cepapi.service -f
```

---

## 🔍 Example Usage

```bash
curl http://localhost:8000/01002010
```

Response:

```json
{
  "cidade": "São Paulo/SP",
  "bairro": "Sé",
  "logradouro": "Praça do Patriarca"
}
```

---

## 📦 Requirements

- Python 3.9+
- FastAPI
- Uvicorn

Install with:

```bash
pip install fastapi uvicorn
```

---

## 📄 License

MIT License — use freely, modify responsibly.