PRISM

A small Streamlit application that converts documents (PDF, DOCX, PPTX, XLSX, CSV, TXT, images, etc.) into clean Markdown using the MarkItDown library.

---

## Overview

PRISM is a developer-focused, single-file web app that exposes a minimal Streamlit UI for converting uploaded documents into Markdown text. It is intended for users who need quick, reproducible document → Markdown conversions locally or in containers.

Why this project exists

- Removes manual copy‑paste and formatting work when migrating documentation from binary formats.
- Provides an easy local/dev environment and a Docker image for simple deployment.

Who it's for

- Developers, technical writers, and small teams who need one-off or light-weight bulk conversions of documents to Markdown.

---

## Features

- Web UI for drag-and-drop file upload and Markdown conversion.
- Supports common document formats: PDF, DOCX, PPTX, XLSX, CSV, TXT, JPG, PNG (via MarkItDown).
- Preview converted Markdown (source + rendered).
- Download converted Markdown file.
- Simple conversion metrics (word/character counts and duration).
- Dockerfile and docker-compose for containerized deployment.
- Simple start/stop scripts for macOS/Linux and Windows.

---

## Tech Stack

- Language: Python 3.12+ (project declares `requires-python = ">=3.12"`)
- Web UI: Streamlit
- Conversion engine: markitdown (MarkItDown)
- Packaging/build: pyproject.toml + hatchling backend
- Utilities: python-dotenv, werkzeug (for `secure_filename`)
- Container tooling: Docker, docker-compose

Key dependencies (from `pyproject.toml`):

- `streamlit>=1.35.0`
- `markitdown[all]>=0.0.1`
- `python-dotenv>=1.0.1`
- `werkzeug>=3.0.3`

---

## Project Structure

Top-level layout:

- `app.py` — Streamlit application entrypoint and main UI logic.
- `pyproject.toml` — project metadata & dependencies.
- `Dockerfile` — image build instructions.
- `docker-compose.yaml` — compose service for local container run.
- `.env.example` — sample environment variables.
- `start.sh` / `stop.sh` — convenience scripts (macOS / Linux).
- `start.bat` / `stop.bat` — convenience scripts (Windows).
- `assets/`
  - `style.css` — custom styling for Streamlit
- `uploads/` — runtime uploads directory (created automatically).
- `outputs/` — runtime outputs directory (created automatically).
- `src/`
  - `config.py` — app configuration and environment variables.
  - `converter.py` — conversion wrapper around MarkItDown.
  - `ui.py` — Streamlit UI helper functions.
  - `utils.py` — helper utilities (filename sanitization, stats, cleanup).

Clean tree-like view (root):

```
.
├─ app.py
├─ pyproject.toml
├─ Dockerfile
├─ docker-compose.yaml
├─ .env.example
├─ start.sh / stop.sh
├─ start.bat / stop.bat
├─ assets/
│  └─ style.css
├─ uploads/
├─ outputs/
└─ src/
   ├─ config.py
   ├─ converter.py
   ├─ ui.py
   └─ utils.py
```

Relevant source entrypoints:

- Application entry: `app.py`
- Conversion logic: `src/converter.py`
- Configuration: `src/config.py`
- UI helpers: `src/ui.py`
- Utilities: `src/utils.py`

---

## Installation

Prerequisites

- Python 3.12+
- Git (optional, for cloning)
- Docker & docker-compose (optional, for containerized runs)

Local (recommended for development)

1. Clone the repo:

```bash
git clone <repo-url>
cd PRISM
```

2. Create & activate a virtual environment:

- macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install the package and dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install .
# or for editable install:
python -m pip install -e .
```

Notes:

- The project uses `pyproject.toml` and `hatchling` as the build backend. Installing via `pip` will pull the declared dependencies.
- The project expects directories `uploads` and `outputs`. These are created automatically by `src/config.py` at runtime.

Containerized (Docker)

1. Build and run with docker-compose:

```bash
docker-compose up -d --build
```

2. The app will be available at:

```
http://localhost:8501
```

Scripts

- macOS / Linux: `./start.sh`, `./stop.sh`
- Windows: `start.bat`, `stop.bat`

The start scripts will attempt to copy `.env.example` to `.env` if `.env` is missing.

---

## Usage

Run locally (dev)

```bash
# With venv activated (see Installation)
streamlit run app.py
```

Then open: http://localhost:8501

Run in Docker

```bash
docker-compose up --build
# or with convenience script
./start.sh
# On Windows
start.bat
```

How to use the UI

- Visit the Streamlit page.
- Drag and drop or select a supported document file.
- Optionally provide an output filename (without .md).
- Click "Convert to Markdown".
- Use "Download Markdown" to save, or view the source/preview tabs.

Notes about CLI/API

- This project does not expose a documented HTTP API beyond the Streamlit UI.
- The Dockerfile provides a healthcheck that uses Streamlit's internal health endpoint at `/_stcore/health` for container health probes.

---

## Configuration

Environment variables (see `.env.example`)

- APP_NAME — application display name (default: `PRISM`)
- STREAMLIT_SERVER_PORT — port to serve Streamlit on (default: `8501`)
- UPLOAD_FOLDER — path for uploaded files (default: `uploads`)
- OUTPUT_FOLDER — path for generated files (default: `outputs`)
- MAX_FILE_SIZE_MB — maximum file size in MB (default: `100`)

Where to put the variables

- Create `.env` in project root (scripts may copy from `.env.example` if missing).
- `docker-compose` uses `.env` and also mounts it into the container.

Configuration files

- `src/config.py` reads `.env` and prepares runtime directories.

Notes

- `MAX_FILE_SIZE_MB` is now enforced in the UI before saving uploads.

---

## API Documentation

Not applicable — this project is a Streamlit UI app rather than a public REST API.

Notes:

- Health probe: `GET /_stcore/health` (used by Dockerfile HEALTHCHECK)
- All conversion activity happens via the UI and a synchronous call into `src/converter.py`.

---

## Examples / Screenshots

- The app presents two primary result tabs after conversion:
  - "Markdown Source" — the raw converted Markdown.
  - "Rendered Preview" — Streamlit-rendered Markdown preview.

(There are no screenshots included in this repo. You can add images under `assets/` and embed them in this README or the app UI.)

---

## Deployment

Containerized (recommended for production-like setups)

- Ensure Docker & docker-compose are available
- Create `.env` (copy from `.env.example` unless you have different values)
- Start stack:

```bash
docker-compose up -d --build
```

- The Dockerfile runs `streamlit run app.py` as the container entrypoint and exposes port 8501.

Production considerations

- This app includes an open file upload UI with no authentication — do not expose it to the public internet without adding access controls (authentication & authorization).
- Use reverse proxy (Nginx) and TLS in front of the app when exposing externally.
- Configure resource limits in Docker/compose for production.
- Consider persisting `uploads` and `outputs` to a secured data volume or external storage for durability.

---

## Contributing

Guidelines

- Fork the repository -> create feature branch -> open a PR.
- Keep changes small and focused.
- Adhere to PEP 8 and use type hints where helpful.
- Add tests for new logic if appropriate (there are currently no test files in repo).

Local dev workflow

1. Create branch:

```bash
git checkout -b feat/your-feature
```

2. Run and test locally:

```bash
python -m pip install -e .
streamlit run app.py
```

3. Commit, push, and open a PR.

Suggested improvements (good first contributions)

- Add server-side file-size enforcement before saving uploads (implemented in this commit).
- Add automated tests & a CI workflow.
- Add rate-limiting / authentication for deployed instances.

---

## Security Considerations

Identified risks and recommendations (evidence-based)

- Open file upload endpoint with no authentication:
  - Risk: Arbitrary users could upload arbitrary files.
  - Mitigation: Add authentication (OAuth, simple token, or reverse proxy auth) before exposing to public networks.

- File size is enforced via `MAX_FILE_SIZE_MB` in `src/config.py` and checked in the Streamlit UI before saving uploads.

- Temporary files and cleanup:
  - The app writes uploads to `uploads/` and uses `cleanup_file()` in error/clear flows. Ensure proper lifecycle and permissions in production.

- Conversion engine (MarkItDown) executes complex parsing:
  - Treat conversion input untrusted; consider sandboxing or resource limits for conversion processes.

- Filenames are sanitized using `werkzeug.utils.secure_filename`, which protects against path traversal.

---

## Known Notes

- The CSS asset is `assets/style.css` and is loaded by the app (fixed).
- No license file found in repository. Add a `LICENSE` file if you plan to publish under an open-source license.
- No automated tests or CI configured in repository.

---

## License

Not found in repo.

- There is no `LICENSE` file detected. If you intend to open-source this project, add a LICENSE (for example MIT, Apache 2.0) to the repository root.

---

If you want, I can:

- Add a basic `LICENSE` (MIT) draft and a minimal GitHub Actions CI workflow to run static checks.
- Add tests or extend conversion error handling.

---
