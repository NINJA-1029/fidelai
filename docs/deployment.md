# Native AWS EC2 Deployment Guide

## 1. Absolute Infrastructure Directives

- DO NOT USE DOCKER.
- DO NOT USE KUBERNETES.
- DO NOT USE ECS, EKS, OR CONTAINER REGISTRIES.
- All processes execute directly on Ubuntu 22.04 / 24.04 LTS host instances via native Linux binaries and Python virtual environments.

---

## 2. Infrastructure Topology

```
                          INTERNET
                             |
                             v
                    AWS Security Group (Ports 80, 443, 22)
                             |
                             v
                     EC2 Host (Ubuntu LTS)
                             |
             +---------------+---------------+
             |                               |
             v                               v
    Nginx Reverse Proxy           llama.cpp Native Binary
    (Port 80/443 -> 8000)         (Local Port 8080)
             |                               |
             v                               v
        FastAPI Daemon                 Qwen 3.8 27B GGUF
      (Systemd / Port 8000)            Model Weights
              |
              +---------------+
                              |
                              v
                     Supabase PostgreSQL
```

---

## 3. Host Provisioning Steps

### Step 1: Base Packages and Python Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git build-essential cmake nginx libopenblas-dev
```

### Step 2: Clone and Setup Virtual Environment
```bash
cd /opt
sudo git clone https://github.com/rakshithshakkthi/csi-origin.git fidel
sudo chown -R ubuntu:ubuntu /opt/fidel
cd /opt/fidel
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Step 3: Compile and Launch Native llama.cpp
```bash
cd /opt
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make LLAMA_OPENBLAS=1 -j$(nproc)

# Download GGUF Model weights into /opt/models/
mkdir -p /opt/models
# Place Qwen 3.8 27B GGUF model weights in /opt/models/
# Example: curl -L -o /opt/models/qwen-3.8-27b.gguf <HF_MODEL_URL>
```

### Step 4: Systemd Service Units

#### `/etc/systemd/system/llamacpp.service`
```ini
[Unit]
Description=Native llama.cpp Inference Server (Qwen 3.8 27B GGUF)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/llama.cpp
ExecStart=/opt/llama.cpp/llama-server -m /opt/models/qwen-3.8-27b.gguf --port 8080 --host 127.0.0.1 -c 4096 --n-gpu-layers 0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### `/etc/systemd/system/fastapi.service`
```ini
[Unit]
Description=FastAPI Financial Intelligence Daemon
After=network.target llamacpp.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/fidel
EnvironmentFile=/opt/fidel/.env
ExecStart=/opt/fidel/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Step 5: Enable and Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable llamacpp fastapi nginx
sudo systemctl start llamacpp
sudo systemctl start fastapi
```

### Step 6: Verify Deployment
```bash
curl -f http://localhost:8000/api/v1/health
```
