Write-Host "Starting containers..."

docker compose up -d

Write-Host "Waiting for services..."
Start-Sleep -Seconds 10



if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."

. .\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."

pip install --upgrade pip
pip install -r requirements.txt


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


Write-Host "Initializing database..."

docker exec -i rag-postgres psql -U postgres -d rag < sql/init.sql


Write-Host "Running ingestion..."

python -m ingestion.ingest_documents


Write-Host "Starting API..."

python app.py
