from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import urllib.parse # For encoding messages in URL

from flock_ui.app.config import FLOCK_FILES_DIR
from flock_ui.app.services.flock_service import (
    get_current_flock_instance,
    load_flock_from_file_service,
    create_new_flock_service,
    get_available_flock_files,
    clear_current_flock, # New service function
    get_current_flock_filename
)
from flock_ui.app.api import flock_management, agent_management, execution, registry_viewer

app = FastAPI(title="Flock UI")

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(flock_management.router, prefix="/api/flocks", tags=["Flock Management API"])
app.include_router(agent_management.router, prefix="/api/flocks", tags=["Agent Management API"])
app.include_router(execution.router, prefix="/api/flocks", tags=["Execution API"])
app.include_router(registry_viewer.router, prefix="/api/registry", tags=["Registry API"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, error: str = None, success: str = None):
    clear_current_flock() # Ensure no flock is active when on dashboard
    return templates.TemplateResponse("index.html", {
        "request": request,
        "flock_files": get_available_flock_files(),
        "error_message": error,
        "success_message": success
    })

@app.post("/ui/load-flock", response_class=RedirectResponse)
async def ui_load_flock_from_file(request: Request, flock_file_select: str = Form(None), flock_file_upload: UploadFile = File(None)):
    filename_to_load = None
    error_message = None
    success_message = None

    if flock_file_upload and flock_file_upload.filename:
        if not flock_file_upload.filename.endswith((".yaml", ".yml", ".flock")):
            error_message = "Invalid file type. Please upload a .yaml, .yml, or .flock file."
        else:
            upload_path = FLOCK_FILES_DIR / flock_file_upload.filename
            try:
                with upload_path.open("wb") as buffer:
                    shutil.copyfileobj(flock_file_upload.file, buffer)
                filename_to_load = flock_file_upload.filename
                success_message = f"File '{filename_to_load}' uploaded."
            except Exception as e:
                error_message = f"Failed to upload file: {str(e)}"
            finally:
                await flock_file_upload.close()
    elif flock_file_select:
        filename_to_load = flock_file_select
        # success_message = f"Selected '{filename_to_load}'." # Removed to avoid double success message

    if error_message:
        return RedirectResponse(url=f"/?error={urllib.parse.quote(error_message)}", status_code=303)

    if filename_to_load:
        loaded_flock = load_flock_from_file_service(filename_to_load)
        if loaded_flock:
            final_success_message = f"{success_message if success_message else ''} Flock '{loaded_flock.name}' loaded.".strip()
            return RedirectResponse(url=f"/ui/editor?success={urllib.parse.quote(final_success_message)}", status_code=303)
        else:
            err_msg = f"Failed to load flock file '{filename_to_load}'. Check server logs for details."
            return RedirectResponse(url=f"/?error={urllib.parse.quote(err_msg)}", status_code=303)

    # If neither select nor upload provided a file
    if not filename_to_load and not error_message:
         error_message = "No file selected or uploaded."

    return RedirectResponse(url=f"/?error={urllib.parse.quote(error_message if error_message else 'An unknown error occurred during load.')}", status_code=303)


@app.post("/ui/create-flock", response_class=RedirectResponse)
async def ui_create_flock(request: Request, flock_name: str = Form(...), default_model: str = Form(None), description: str = Form(None)):
    if not flock_name.strip():
         return RedirectResponse(url=f"/?error={urllib.parse.quote('Flock name cannot be empty.')}", status_code=303)
    new_flock = create_new_flock_service(flock_name, default_model, description)
    success_msg = f"New flock '{new_flock.name}' created. Don't forget to save!"
    return RedirectResponse(url=f"/ui/editor?success={urllib.parse.quote(success_msg)}", status_code=303)

@app.get("/ui/editor", response_class=HTMLResponse)
async def flock_editor_page(request: Request, success: str = None, error: str = None):
    flock_instance = get_current_flock_instance()
    if not flock_instance:
        err_msg = "No flock loaded. Please load or create a flock first."
        return RedirectResponse(url=f"/?error={urllib.parse.quote(err_msg)}", status_code=303)
    return templates.TemplateResponse("flock_editor.html", {
        "request": request,
        "flock": flock_instance,
        "current_filename": get_current_flock_filename(),
        "success_message": success,
        "error_message": error
    })

@app.get("/ui/registry", response_class=HTMLResponse)
async def registry_viewer_page(request: Request):
    return templates.TemplateResponse("registry_viewer.html", {"request": request})
