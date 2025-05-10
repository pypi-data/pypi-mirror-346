from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Determine base directory of this script (document_generator_ui/server)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Document Generator UI",
    description="Static SPA backend for Document Generator",
)

# Mount the SPA static files at the root URL
app.mount(
    "/",
    StaticFiles(directory=str(STATIC_DIR), html=True),
    name="static",
)

# No additional endpoints yet; SPA will display console message for verification