
docker compose up -d


Write-Host "Waiting for Postgres..."

while ($true) {

    try {
        docker exec rag-postgres pg_isready -U postgres > $null 2>&1
        if ($LASTEXITCODE -eq 0) { break }
    }
    catch {}

    Start-Sleep -Seconds 2
}

Write-Host "Postgres ready"


Write-Host "Waiting for Ollama..."

while ($true) {

    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) { break }
    }
    catch {}

    Start-Sleep -Seconds 2
}

Write-Host "Ollama ready"


Write-Host "Waiting for Gremlin..."

while ($true) {

    try {
        $tcp = Test-NetConnection -ComputerName localhost -Port 8182 -WarningAction SilentlyContinue
        if ($tcp.TcpTestSucceeded) { break }
    }
    catch {}

    Start-Sleep -Seconds 2
}

Write-Host "Gremlin ready"


if (!(Test-Path ".venv")) {

    Write-Host "Creating virtual environment..."

    python -m venv .venv
}

Write-Host "Activating virtual environment..."

. .\.venv\Scripts\Activate.ps1


Write-Host "Installing requirements..."

pip install --upgrade pip
pip install -r requirements.txt


# -------------------------
# Install Ollama models
# -------------------------

Write-Host "Installing Ollama models..."

Invoke-RestMethod `
  -Uri "http://localhost:11434/api/pull" `
  -Method POST `
  -Body '{"name":"nomic-embed-text"}' `
  -ContentType "application/json"

Invoke-RestMethod `
  -Uri "http://localhost:11434/api/pull" `
  -Method POST `
  -Body '{"name":"llama3"}' `
  -ContentType "application/json"


# -------------------------
# Initialize Database
# -------------------------

Write-Host "Initializing database..."

docker exec -i rag-postgres psql -U postgres -d rag < sql/init.sql


# -------------------------
# Run ingestion
# -------------------------

Write-Host "Running ingestion..."

python -m ingestion.ingest_documents


# -------------------------
# Start API
# -------------------------

Write-Host "Starting API..."

python app.py
