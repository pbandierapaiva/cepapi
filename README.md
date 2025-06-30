# cepapi
API para consulta de CEP brasileiro

Implementação de busca de CEP utilizando FASTAPI

No diretório clonado:

python3 -m venv ambiente
source venv/bin/activate
pip install fastapi uvicorn

Coloque arquivo ceps.txt no formato:

$ head ceps.txt
01001000        São Paulo/SP    Sé      Praça da Sé - lado ímpar
01001001        São Paulo/SP    Sé      Praça da Sé - lado par
01001010        São Paulo/SP    Sé      Rua Filipe de Oliveira
01001900        São Paulo/SP    Sé      Praça da Sé, 108

Crie o arquivo /etc/systemd/system/cepapi.service:
[Unit]
Description=FastAPI CEP Lookup Service
After=network.target

[Service]
User=paiva
WorkingDirectory=/XXXX/cepapi
ExecStart=/XXXX/cepapi/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

# Habilite o serviço:
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now cepapi.service


