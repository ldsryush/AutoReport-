$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
  & $venvPython -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
} else {
  py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
}
