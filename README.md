# AsCO2

AsCO2 is a web project to help non-profit organizations (associations) build simple, understandable carbon footprints.

The stack is intentionally lightweight:
- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript (no heavy framework required)
- Data: ADEME-backed public data sources and APIs (including Impact CO2 ecosystem endpoints when relevant)

## Why this project

Most associations need climate reporting tools that are:
- easy to use,
- transparent about assumptions,
- affordable,
- adaptable to French context data.

AsCO2 aims to provide a practical first step toward carbon accounting, not a black-box expert system.

## Environment Variables

Use a .env file for local development:

No required variables for the minimalist placeholder.

## Local Setup

Target Python version: 3.12

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the API with the helper script:

```bash
bash launchapi.sh
```

This script activates `.venv`, prints the Python interpreter path, starts the API from `backend/main.py` with `fastapi dev`, then deactivates the virtual environment when the server stops.

Run the API (dev mode):

```bash
fastapi dev
```

In development mode, frontend files (`frontend/templates`, `frontend/style`, `frontend/js`) are now auto-refreshed in the browser when they change.

Run the API (production mode):

```bash
fastapi run
```

Run tests:

```bash
pytest
```


## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a detailed overview of the project structure and backend design.

## Copilot Agent Configuration

This repository includes workspace-level Copilot configuration files in .github/:
- .github/copilot-instructions.md: global coding instructions for the project.
- .github/agents/ademe-data.agent.md: specialized for ADEME/Impact CO2 data integration.
- .github/agents/fastapi-backend.agent.md: specialized for FastAPI backend design and implementation.
- .github/agents/frontend-vanilla.agent.md: specialized for HTML/CSS/JS frontend work.


## License

MIT. See LICENSE.