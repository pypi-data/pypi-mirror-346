import os
import shutil
from pathlib import Path

# Project structure and content
PROJECT_STRUCTURE = {
    "flock-ui": {
        "app": {
            "__init__.py": "",
            "main.py": """\
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil

from app.config import FLOCK_FILES_DIR
from app.services.flock_service import (
    get_current_flock_instance,
    load_flock_from_file_service,
    create_new_flock_service,
    save_current_flock_to_file_service,
    get_available_flock_files,
    set_current_flock_instance,
    set_current_flock_filename,
    get_current_flock_filename,
    clear_current_flock
)
from app.api import flock_management, agent_management, execution, registry_viewer

app = FastAPI(title="Flock UI")

# Mount static files
BASE_DIR = Path(__file__).resolve().parent.parent # Points to flock-ui/
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include API routers
app.include_router(flock_management.router, prefix="/api/flocks", tags=["Flock Management API"])
app.include_router(agent_management.router, prefix="/api/flocks", tags=["Agent Management API"])
app.include_router(execution.router, prefix="/api/flocks", tags=["Execution API"])
app.include_router(registry_viewer.router, prefix="/api/registry", tags=["Registry API"])


# --- Root and Main UI Routes ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, error: str = None, success: str = None):
    # Clear any loaded flock when returning to dashboard
    clear_current_flock()
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
                with open(upload_path, "wb") as buffer:
                    shutil.copyfileobj(flock_file_upload.file, buffer)
                filename_to_load = flock_file_upload.filename
                success_message = f"File '{filename_to_load}' uploaded successfully."
            except Exception as e:
                error_message = f"Failed to upload file: {str(e)}"
            finally:
                await flock_file_upload.close()
    elif flock_file_select:
        filename_to_load = flock_file_select

    if error_message:
        return RedirectResponse(url=f"/?error={error_message}", status_code=303)

    if filename_to_load:
        loaded_flock = load_flock_from_file_service(filename_to_load)
        if loaded_flock:
            return RedirectResponse(url=f"/ui/editor?success={success_message or 'Flock loaded'}", status_code=303)
        else:
            return RedirectResponse(url="/?error=Failed to load flock file.", status_code=303)

    return RedirectResponse(url="/?error=No file selected or uploaded.", status_code=303)


@app.post("/ui/create-flock", response_class=RedirectResponse)
async def ui_create_flock(request: Request, flock_name: str = Form(...), default_model: str = Form(None), description: str = Form(None)):
    if not flock_name.strip():
         return RedirectResponse(url="/?error=Flock name cannot be empty.", status_code=303)
    create_new_flock_service(flock_name, default_model, description)
    return RedirectResponse(url=f"/ui/editor?success=New flock '{flock_name}' created.", status_code=303)


@app.get("/ui/editor", response_class=HTMLResponse)
async def flock_editor_page(request: Request, success: str = None, error: str = None):
    flock_instance = get_current_flock_instance()
    if not flock_instance:
        return RedirectResponse(url="/?error=No flock loaded. Please load or create a flock first.", status_code=303)
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

# Note: HTMX partial routes are now in their respective api/*.py files
""",
            "api": {
                "__init__.py": "",
                "flock_management.py": """\
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.flock_service import (
    update_flock_properties_service,
    get_current_flock_instance,
    save_current_flock_to_file_service,
    set_current_flock_filename,
    get_current_flock_filename
)

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent.parent # Points to flock-ui/
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/htmx/flock-properties-form", response_class=HTMLResponse)
async def htmx_get_flock_properties_form(request: Request, update_message: str = None, success: bool = None):
    flock = get_current_flock_instance()
    if not flock:
        # This case should ideally not be reached if editor page properly redirects
        return HTMLResponse("<div class='error'>Error: No flock loaded. Please load or create one first.</div>")
    return templates.TemplateResponse("partials/_flock_properties_form.html", {
        "request": request,
        "flock": flock,
        "current_filename": get_current_flock_filename(),
        "update_message": update_message,
        "success": success
    })

@router.post("/htmx/flock-properties", response_class=HTMLResponse)
async def htmx_update_flock_properties(request: Request, flock_name: str = Form(...), default_model: str = Form(...), description: str = Form("")):
    success_update = update_flock_properties_service(flock_name, default_model, description)
    flock = get_current_flock_instance() # Get updated instance
    # Re-render the form with a message
    return templates.TemplateResponse("partials/_flock_properties_form.html", {
        "request": request,
        "flock": flock,
        "current_filename": get_current_flock_filename(),
        "update_message": "Flock properties updated!" if success_update else "Failed to update properties.",
        "success": success_update
    })

@router.post("/htmx/save-flock", response_class=HTMLResponse)
async def htmx_save_flock(request: Request, save_filename: str = Form(...)):
    if not save_filename.strip(): # Basic validation
        flock = get_current_flock_instance()
        return templates.TemplateResponse("partials/_flock_properties_form.html", {
            "request": request,
            "flock": flock,
            "current_filename": get_current_flock_filename(),
            "save_message": "Filename cannot be empty.",
            "success": False
        })

    if not (save_filename.endswith(".yaml") or save_filename.endswith(".yml") or save_filename.endswith(".flock")):
        save_filename += ".flock.yaml" # Add default extension

    success, message = save_current_flock_to_file_service(save_filename)
    flock = get_current_flock_instance()
    return templates.TemplateResponse("partials/_flock_properties_form.html", {
        "request": request,
        "flock": flock,
        "current_filename": get_current_flock_filename() if success else get_current_flock_filename(), # Update filename if save was successful
        "save_message": message,
        "success": success
    })
""",
                "agent_management.py": """\
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.flock_service import (
    get_current_flock_instance,
    add_agent_to_current_flock_service,
    update_agent_in_current_flock_service,
    remove_agent_from_current_flock_service,
    get_registered_items_service
)
from flock.core import FlockAgent # For type checking

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/htmx/agent-list", response_class=HTMLResponse)
async def htmx_get_agent_list(request: Request, message: str = None, success: bool = None):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")
    return templates.TemplateResponse("partials/_agent_list.html", {
        "request": request,
        "flock": flock,
        "message": message,
        "success": success
    })

@router.get("/htmx/agents/{agent_name}/details-form", response_class=HTMLResponse)
async def htmx_get_agent_details_form(request: Request, agent_name: str):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")
    agent = flock.agents.get(agent_name)
    if not agent: return HTMLResponse(f"<p class='error'>Agent '{agent_name}' not found.</p>")
    
    registered_tools = get_registered_items_service("tool")
    current_tools = [tool.__name__ for tool in agent.tools] if agent.tools else []

    return templates.TemplateResponse("partials/_agent_detail_form.html", {
        "request": request,
        "agent": agent,
        "is_new": False,
        "registered_tools": registered_tools,
        "current_tools": current_tools
    })

@router.get("/htmx/agents/new-agent-form", response_class=HTMLResponse)
async def htmx_get_new_agent_form(request: Request):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")
    registered_tools = get_registered_items_service("tool")
    return templates.TemplateResponse("partials/_agent_detail_form.html", {
        "request": request,
        "agent": None, # For new agent
        "is_new": True,
        "registered_tools": registered_tools,
        "current_tools": []
    })

@router.post("/htmx/agents", response_class=HTMLResponse) # For creating new agent
async def htmx_create_agent(request: Request,
                            agent_name: str = Form(...),
                            agent_description: str = Form(""),
                            agent_model: str = Form(None), # Can be empty to use Flock default
                            input_signature: str = Form(...),
                            output_signature: str = Form(...),
                            tools: list[str] = Form([])): # FastAPI handles list from multiple form fields with same name
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")

    if not agent_name.strip() or not input_signature.strip() or not output_signature.strip():
        # Render form again with error (or use a different target for error message)
        registered_tools = get_registered_items_service("tool")
        return templates.TemplateResponse("partials/_agent_detail_form.html", {
            "request": request, "agent": None, "is_new": True,
            "error_message": "Name, Input Signature, and Output Signature are required.",
            "registered_tools": registered_tools, "current_tools": tools # Pass back selected tools
        })
    
    agent_config = {
        "name": agent_name, "description": agent_description,
        "model": agent_model if agent_model else None, # Pass None if empty string for FlockFactory
        "input": input_signature, "output": output_signature,
        "tools_names": tools # Pass tool names
    }
    success = add_agent_to_current_flock_service(agent_config)
    
    # After action, re-render the agent list and clear the detail form
    # Set headers for HTMX to trigger multiple target updates
    response_headers = {}
    if success:
        response_headers["HX-Trigger"] = "agentListChanged" # Custom event to refresh list

    # Render an empty detail form or a success message for the detail panel
    empty_detail_form = templates.TemplateResponse("partials/_agent_detail_form.html", {
        "request": request, "agent": None, "is_new": True, "registered_tools": get_registered_items_service("tool"),
        "form_message": "Agent created successfully!" if success else "Failed to create agent.",
        "success": success
    }).body.decode()

    return HTMLResponse(content=empty_detail_form, headers=response_headers)


@router.put("/htmx/agents/{original_agent_name}", response_class=HTMLResponse) # For updating existing agent
async def htmx_update_agent(request: Request, original_agent_name: str,
                            agent_name: str = Form(...),
                            agent_description: str = Form(""),
                            agent_model: str = Form(None),
                            input_signature: str = Form(...),
                            output_signature: str = Form(...),
                            tools: list[str] = Form([])):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")

    agent_config = {
        "name": agent_name, "description": agent_description,
        "model": agent_model if agent_model else None,
        "input": input_signature, "output": output_signature,
        "tools_names": tools
    }
    success = update_agent_in_current_flock_service(original_agent_name, agent_config)

    response_headers = {}
    if success:
        response_headers["HX-Trigger"] = "agentListChanged"

    # Re-render the form with update message
    updated_agent = flock.agents.get(agent_name) # Get the potentially renamed agent
    registered_tools = get_registered_items_service("tool")
    current_tools = [tool.__name__ for tool in updated_agent.tools] if updated_agent and updated_agent.tools else []

    updated_form = templates.TemplateResponse("partials/_agent_detail_form.html", {
        "request": request,
        "agent": updated_agent, # Pass the updated agent
        "is_new": False,
        "form_message": "Agent updated successfully!" if success else "Failed to update agent.",
        "success": success,
        "registered_tools": registered_tools,
        "current_tools": current_tools
    }).body.decode()
    return HTMLResponse(content=updated_form, headers=response_headers)

@router.delete("/htmx/agents/{agent_name}", response_class=HTMLResponse)
async def htmx_delete_agent(request: Request, agent_name: str):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("") # Return empty to clear detail view

    success = remove_agent_from_current_flock_service(agent_name)
    
    response_headers = {}
    if success:
        response_headers["HX-Trigger"] = "agentListChanged"
        # Return an empty agent detail form to clear the panel
        # Also, the agent list will re-render due to HX-Trigger
        return HTMLResponse(
            templates.TemplateResponse("partials/_agent_detail_form.html", {
                "request": request, "agent": None, "is_new": True,
                "form_message": f"Agent '{agent_name}' removed.", "success": True,
                "registered_tools": get_registered_items_service("tool")
            }).body.decode(),
            headers=response_headers
        )
    else:
        # If deletion fails, re-render the agent detail form with an error
        # This scenario should be rare unless the agent was already removed
        agent = flock.agents.get(agent_name) # Should still exist if delete failed
        registered_tools = get_registered_items_service("tool")
        current_tools = [tool.__name__ for tool in agent.tools] if agent and agent.tools else []
        return templates.TemplateResponse("partials/_agent_detail_form.html", {
            "request": request, "agent": agent, "is_new": False,
            "form_message": f"Failed to remove agent '{agent_name}'.", "success": False,
            "registered_tools": registered_tools, "current_tools": current_tools
        })

""",
                "execution.py": """\
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json # For parsing inputs

from app.services.flock_service import get_current_flock_instance, run_current_flock_service

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/htmx/execution-form", response_class=HTMLResponse)
async def htmx_get_execution_form(request: Request):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded.</p>")
    return templates.TemplateResponse("partials/_execution_form.html", {"request": request, "flock": flock, "input_fields": []})

@router.get("/htmx/agents/{agent_name}/input-form", response_class=HTMLResponse)
async def htmx_get_agent_input_form(request: Request, agent_name: str):
    from flock.core.util.input_resolver import parse_schema # Using the more robust parser
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("") # Clear form if no flock
    agent = flock.agents.get(agent_name)
    if not agent: return HTMLResponse(f"<p class='error'>Agent '{agent_name}' not found.</p>")

    input_fields = []
    if agent.input:
        try:
            # Assuming agent.input is a string like "query: str | Description, count: int"
            # We need a robust way to parse this. Flock-core should provide a utility.
            # For MVP, a simple split, can be enhanced.
            parsed_spec = parse_schema(agent.input) # [(name, type_str, description), ...]
            for name, type_str, description in parsed_spec:
                field_info = {"name": name, "type": type_str.lower(), "description": description or ""}
                # Determine HTML input type
                if "bool" in field_info["type"]:
                    field_info["html_type"] = "checkbox"
                elif "int" in field_info["type"] or "float" in field_info["type"]:
                    field_info["html_type"] = "number"
                elif "list" in field_info["type"] or "dict" in field_info["type"]:
                     field_info["html_type"] = "textarea" # For JSON input for list/dict
                     field_info["placeholder"] = "Enter JSON for list/dict"
                else:
                    field_info["html_type"] = "text"
                input_fields.append(field_info)
        except Exception as e:
            return HTMLResponse(f"<p class='error'>Error parsing input signature for {agent_name}: {e}</p>")
            
    return templates.TemplateResponse("partials/_dynamic_input_form_content.html", {"request": request, "input_fields": input_fields})

@router.post("/htmx/run", response_class=HTMLResponse)
async def htmx_run_flock(request: Request):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded to run.</p>")

    form_data = await request.form()
    start_agent_name = form_data.get("start_agent_name")
    if not start_agent_name:
        return HTMLResponse("<p class='error'>Starting agent not selected.</p>")

    agent = flock.agents.get(start_agent_name)
    if not agent:
        return HTMLResponse(f"<p class='error'>Agent '{start_agent_name}' not found.</p>")

    inputs = {}
    if agent.input:
        from flock.core.util.input_resolver import parse_schema
        parsed_spec = parse_schema(agent.input)
        for name, type_str, _ in parsed_spec:
            raw_value = form_data.get(f"agent_input_{name}")
            if raw_value is None and "bool" in type_str.lower(): # Checkbox not sent if unchecked
                inputs[name] = False
                continue
            if raw_value is None:
                # Handle case where field might be optional or not provided
                # For MVP, we might assume all defined inputs are required or default to None/empty
                # A more robust solution would check Pydantic model defaults or use Optional
                inputs[name] = None # Or some default
                continue

            # Type conversion
            if "int" in type_str.lower():
                try: inputs[name] = int(raw_value)
                except ValueError: return HTMLResponse(f"<p class='error'>Invalid integer for '{name}'.</p>")
            elif "float" in type_str.lower():
                try: inputs[name] = float(raw_value)
                except ValueError: return HTMLResponse(f"<p class='error'>Invalid float for '{name}'.</p>")
            elif "bool" in type_str.lower():
                inputs[name] = raw_value.lower() in ['true', 'on', '1', 'yes']
            elif "list" in type_str.lower() or "dict" in type_str.lower():
                try:
                    inputs[name] = json.loads(raw_value)
                except json.JSONDecodeError:
                    return HTMLResponse(f"<p class='error'>Invalid JSON for '{name}'.</p>")
            else: # string
                inputs[name] = raw_value
    
    result_data = await run_current_flock_service(start_agent_name, inputs)

    return templates.TemplateResponse("partials/_results_display.html", {"request": request, "result_data": result_data})
""",
                "registry_viewer.py": """\
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.flock_service import get_registered_items_service

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/htmx/{item_type}/table", response_class=HTMLResponse)
async def htmx_get_registry_table(request: Request, item_type: str):
    valid_item_types = ["type", "tool", "component"]
    if item_type not in valid_item_types:
        return HTMLResponse("<p class='error'>Invalid item type requested.</p>", status_code=400)

    items = get_registered_items_service(item_type)
    return templates.TemplateResponse("partials/_registry_table.html", {
        "request": request,
        "item_type_display": item_type.capitalize() + "s",
        "items": items
    })
"""
            },
            "services": {
                "__init__.py": "",
                "flock_service.py": """\
from flock.core import Flock, FlockFactory, FlockAgent
from flock.core.flock_registry import get_registry
from pathlib import Path
import yaml # For parsing issues, if any, during load

from app.config import CURRENT_FLOCK_INSTANCE, FLOCK_FILES_DIR, CURRENT_FLOCK_FILENAME

def get_available_flock_files() -> list[str]:
    if not FLOCK_FILES_DIR.exists():
        return []
    return [f.name for f in FLOCK_FILES_DIR.iterdir() if f.is_file() and (f.suffix in [".yaml", ".yml", ".flock"])]

def load_flock_from_file_service(filename: str) -> Flock | None:
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    file_path = FLOCK_FILES_DIR / filename
    if not file_path.exists():
        print(f"Error: File not found {file_path}")
        CURRENT_FLOCK_INSTANCE = None
        CURRENT_FLOCK_FILENAME = None
        return None
    try:
        CURRENT_FLOCK_INSTANCE = Flock.load_from_file(str(file_path))
        CURRENT_FLOCK_FILENAME = filename
        print(f"Successfully loaded flock: {CURRENT_FLOCK_INSTANCE.name if CURRENT_FLOCK_INSTANCE else 'None'}")
        return CURRENT_FLOCK_INSTANCE
    except Exception as e:
        print(f"Error loading flock from {file_path}: {e}")
        CURRENT_FLOCK_INSTANCE = None
        CURRENT_FLOCK_FILENAME = None
        return None

def create_new_flock_service(name: str, model: str | None, description: str | None) -> Flock:
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    CURRENT_FLOCK_INSTANCE = Flock(name=name, model=model, description=description, show_flock_banner=False, enable_logging=False)
    # For a new flock, the filename is not set until saved
    CURRENT_FLOCK_FILENAME = f"{name}.flock.yaml" # Suggest a default filename
    print(f"Created new flock: {name}")
    return CURRENT_FLOCK_INSTANCE

def get_current_flock_instance() -> Flock | None:
    global CURRENT_FLOCK_INSTANCE
    return CURRENT_FLOCK_INSTANCE

def get_current_flock_filename() -> str | None:
    global CURRENT_FLOCK_FILENAME
    return CURRENT_FLOCK_FILENAME

def set_current_flock_instance(flock: Flock | None):
    global CURRENT_FLOCK_INSTANCE
    CURRENT_FLOCK_INSTANCE = flock

def set_current_flock_filename(filename: str | None):
    global CURRENT_FLOCK_FILENAME
    CURRENT_FLOCK_FILENAME = filename
    
def clear_current_flock():
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    CURRENT_FLOCK_INSTANCE = None
    CURRENT_FLOCK_FILENAME = None


def save_current_flock_to_file_service(new_filename: str) -> tuple[bool, str]:
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    if not CURRENT_FLOCK_INSTANCE:
        return False, "No flock loaded to save."
    
    if not new_filename.strip():
        return False, "Filename cannot be empty."

    save_path = FLOCK_FILES_DIR / new_filename
    try:
        CURRENT_FLOCK_INSTANCE.to_yaml_file(str(save_path))
        CURRENT_FLOCK_FILENAME = new_filename # Update current filename on successful save
        return True, f"Flock saved successfully to {new_filename}."
    except Exception as e:
        return False, f"Error saving flock: {e}"

def update_flock_properties_service(name: str, model: str | None, description: str | None) -> bool:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE:
        return False
    CURRENT_FLOCK_INSTANCE.name = name
    CURRENT_FLOCK_INSTANCE.model = model
    CURRENT_FLOCK_INSTANCE.description = description
    return True

def add_agent_to_current_flock_service(agent_config: dict) -> bool:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE:
        return False
    
    registry = get_registry()
    tools_instances = []
    if agent_config.get("tools_names"):
        for tool_name in agent_config["tools_names"]:
            try:
                tool_func = registry.get_callable(tool_name)
                tools_instances.append(tool_func)
            except KeyError:
                print(f"Warning: Tool '{tool_name}' not found in registry. Skipping.")
    
    try:
        # Use FlockFactory for consistency, even if it means passing more args
        agent = FlockFactory.create_default_agent(
            name=agent_config["name"],
            description=agent_config.get("description"),
            model=agent_config.get("model"), # Factory will use Flock's default if this is None
            input=agent_config["input"],
            output=agent_config["output"],
            tools=tools_instances if tools_instances else None
        )
        CURRENT_FLOCK_INSTANCE.add_agent(agent)
        return True
    except Exception as e:
        print(f"Error adding agent: {e}")
        return False

def update_agent_in_current_flock_service(original_agent_name: str, agent_config: dict) -> bool:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE: return False
    
    agent_to_update = CURRENT_FLOCK_INSTANCE.agents.get(original_agent_name)
    if not agent_to_update: return False

    registry = get_registry()
    tools_instances = []
    if agent_config.get("tools_names"):
        for tool_name in agent_config["tools_names"]:
            try:
                tool_func = registry.get_callable(tool_name)
                tools_instances.append(tool_func)
            except KeyError:
                print(f"Warning: Tool '{tool_name}' not found in registry for update. Skipping.")

    try:
        # Update properties
        agent_to_update.name = agent_config["name"] # Must update name first if it changed
        agent_to_update.description = agent_config.get("description")
        agent_to_update.model = agent_config.get("model")
        agent_to_update.input = agent_config["input"]
        agent_to_update.output = agent_config["output"]
        agent_to_update.tools = tools_instances if tools_instances else None
        
        # If name changed, need to update the key in the flock's agent dictionary
        if original_agent_name != agent_config["name"]:
            CURRENT_FLOCK_INSTANCE._agents[agent_config["name"]] = CURRENT_FLOCK_INSTANCE._agents.pop(original_agent_name)
            
        return True
    except Exception as e:
        print(f"Error updating agent: {e}")
        return False

def remove_agent_from_current_flock_service(agent_name: str) -> bool:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE: return False
    if agent_name in CURRENT_FLOCK_INSTANCE.agents:
        del CURRENT_FLOCK_INSTANCE._agents[agent_name]
        return True
    return False

async def run_current_flock_service(start_agent_name: str, inputs: dict) -> dict | str:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE:
        return "Error: No flock loaded."
    if not start_agent_name or start_agent_name not in CURRENT_FLOCK_INSTANCE.agents:
        return f"Error: Start agent '{start_agent_name}' not found in current flock."
    try:
        # Use the async run method for consistency with potential Temporal use later
        result = await CURRENT_FLOCK_INSTANCE.run_async(start_agent=start_agent_name, input=inputs, box_result=False)
        return result
    except Exception as e:
        return f"Error during flock execution: {e}"

def get_registered_items_service(item_type: str) -> list:
    registry = get_registry()
    items = []
    if item_type == "type":
        items_dict = registry._types
    elif item_type == "tool": # Tools are callables
        items_dict = registry._callables
    elif item_type == "component":
        items_dict = registry._components
    else:
        return []

    for name, item_obj in items_dict.items():
        module_path = "N/A"
        try:
            module_path = item_obj.__module__
        except AttributeError:
            pass
        items.append({"name": name, "module": module_path})
    return items

""",
            },
            "models_ui.py": """\
# Pydantic models specific to UI interactions, if needed.
# For MVP, we might not need many here, as we'll primarily pass basic dicts to flock_service.
# Example:
# from pydantic import BaseModel
# class SaveFlockRequest(BaseModel):
#     current_flock_json: str # Or a more structured model if preferred
#     new_filename: str
""",
            "config.py": """\
import os
from pathlib import Path

FLOCK_FILES_DIR = Path(os.getenv("FLOCK_FILES_DIR", "./.flock_ui_projects"))
FLOCK_FILES_DIR.mkdir(parents=True, exist_ok=True)

# Global state for MVP - NOT SUITABLE FOR PRODUCTION/MULTI-USER
CURRENT_FLOCK_INSTANCE = None
CURRENT_FLOCK_FILENAME = None
"""
        },
        "static": {
            "css": {
                "custom.css": """\
/* Minimal custom styles - Pico.CSS handles most */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
}
nav ul li strong {
    color: var(--pico-h1-color); /* Use Pico's heading color for brand */
}
.container {
    padding-bottom: 4rem; /* Space for footer */
}
.error {
    color: var(--pico-del-color);
    border: 1px solid var(--pico-del-color);
    padding: 0.5rem;
    margin-bottom: 1rem;
    border-radius: var(--pico-border-radius);
    background-color: color-mix(in srgb, var(--pico-del-color) 10%, transparent);
}
.success {
    color: var(--pico-ins-color);
    border: 1px solid var(--pico-ins-color);
    padding: 0.5rem;
    margin-bottom: 1rem;
    border-radius: var(--pico-border-radius);
    background-color: color-mix(in srgb, var(--pico-ins-color) 10%, transparent);
}
/* Style for form messages (can be success or error) */
.form-message {
    padding: 0.75rem;
    margin-top: 1rem;
    border-radius: var(--pico-border-radius);
    font-weight: bold;
}
.form-message.success {
    background-color: var(--pico-ins-color);
    color: var(--pico-primary-inverse); /* Light text on dark green */
    border: 1px solid var(--pico-ins-color);
}
.form-message.error {
    background-color: var(--pico-del-color);
    color: var(--pico-primary-inverse); /* Light text on dark red */
    border: 1px solid var(--pico-del-color);
}


/* Styles for editor layout */
.editor-grid {
    display: grid;
    grid-template-columns: 1fr 2fr; /* Sidebar and main content area */
    grid-template-rows: auto auto 1fr; /* Flock props, agent list/detail, execution */
    grid-template-areas:
        "flock-props flock-props"
        "agent-list agent-detail"
        "execution execution";
    gap: 1rem;
    min-height: 70vh; /* Ensure it takes up significant space */
}

#flock-properties-panel { grid-area: flock-props; }
#agent-list-panel { grid-area: agent-list; overflow-y: auto; max-height: 60vh; } /* Make agent list scrollable */
#agent-detail-panel { grid-area: agent-detail; overflow-y: auto; max-height: 60vh; } /* Make agent detail scrollable */
#execution-panel { grid-area: execution; }
#results-display-container { margin-top: 1rem; }


/* Simple list styling for agent list */
#agent-list-panel ul {
    list-style-type: none;
    padding: 0;
}
#agent-list-panel li {
    padding: 0.5rem;
    border: 1px solid var(--pico-muted-border-color);
    margin-bottom: 0.5rem;
    border-radius: var(--pico-border-radius);
    cursor: pointer;
}
#agent-list-panel li:hover {
    background-color: var(--pico-muted-background-color);
}
#agent-list-panel li.selected { /* For future use if needed */
    background-color: var(--pico-primary-background);
    color: var(--pico-primary-inverse);
}
#agent-list-panel button {
    margin-top: 1rem;
}

/* Agent detail form styling */
#agent-detail-panel form fieldset {
    margin-bottom: 1rem;
}
#agent-detail-panel form label {
    margin-bottom: 0.25rem;
}
#agent-detail-panel form input[type="text"],
#agent-detail-panel form textarea,
#agent-detail-panel form select {
    margin-bottom: 0.75rem;
}

/* Tool checklist styling */
.tool-checklist label {
    display: block; /* Each tool on a new line */
    margin-bottom: 0.25rem;
}
.tool-checklist input[type="checkbox"] {
    margin-right: 0.5rem;
}

.htmx-indicator{
    display: none;
}
.htmx-request .htmx-indicator{
    display: inline;
}
.htmx-request.htmx-indicator{
    display: inline;
}

/* For the loading message */
#loading-indicator {
    padding: 0.5em;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
}

#results-display {
    background-color: var(--pico-code-background-color);
    color: var(--pico-code-color);
    padding: 1rem;
    border-radius: var(--pico-border-radius);
    overflow-x: auto; /* Handle wide results */
    margin-top: 1rem;
}
#results-display pre {
    margin: 0;
    white-space: pre-wrap; /* Wrap long lines in pre */
    word-break: break-all; /* Break long words/strings */
}

/* Ensure button group in agent detail has some space */
#agent-detail-panel .grid { /* Pico's grid class for button group */
    margin-top: 1rem;
}

"""
            }
        },
        "templates": {
            "base.html": """\
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flock UI{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
    <link rel="stylesheet" href="{{ url_for('static', path='/css/custom.css') }}">
    <script src="https://unpkg.com/htmx.org@1.9.10" integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC" crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        /* Add a bit of margin to the top of the body to prevent nav overlap */
        body { padding-top: 3.5rem; }
        nav {
            position: fixed; /* Make nav fixed */
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000; /* Ensure nav is on top */
            background-color: var(--pico-card-background-color); /* Give nav a background */
            border-bottom: 1px solid var(--pico-muted-border-color);
        }
    </style>
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><strong><a href="/" style="text-decoration: none;">Flock UI 🐤</a></strong></li>
        </ul>
        <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/ui/editor" role="button" {% if not request.url.path.startswith('/ui/editor') %}class="outline"{% endif %}>Editor</a></li>
            <li><a href="/ui/registry" role="button" {% if not request.url.path.startswith('/ui/registry') %}class="outline"{% endif %}>Registry</a></li>
        </ul>
    </nav>
    <main class="container">
        {% if success_message %}
            <div class="success" role="alert">
                {{ success_message }}
                <button type="button" class="close" onclick="this.parentElement.style.display='none';" aria-label="Dismiss">×</button>
            </div>
        {% endif %}
        {% if error_message %}
            <div class="error" role="alert">
                {{ error_message }}
                <button type="button" class="close" onclick="this.parentElement.style.display='none';" aria-label="Dismiss">×</button>
            </div>
        {% endif %}
        {% block content %}{% endblock %}
    </main>
    <footer class="container">
        <small>Built with FastAPI, HTMX, Pico.CSS, and ❤️ for Flock</small>
    </footer>
</body>
</html>
""",
            "index.html": """\
{% extends "base.html" %}

{% block title %}Flock UI - Dashboard{% endblock %}

{% block content %}
<article>
    <header>
        <h2>Welcome to Flock UI!</h2>
        <p>Manage your Flock configurations and agents.</p>
    </header>

    <section id="create-flock-section">
        <h3>Create New Flock</h3>
        <form hx-post="/ui/create-flock" hx-target="body" hx-swap="innerHTML" hx-push-url="true">
            <label for="flock_name">Flock Name</label>
            <input type="text" id="flock_name" name="flock_name" placeholder="My Awesome Flock" required>

            <label for="default_model">Default Model (Optional)</label>
            <input type="text" id="default_model" name="default_model" placeholder="openai/gpt-4o">

            <label for="description">Description (Optional)</label>
            <textarea id="description" name="description" placeholder="A brief description of what this Flock does."></textarea>

            <button type="submit">Create Flock and Open Editor</button>
        </form>
    </section>

    <hr>

    <section id="load-flock-section">
        <h3>Load Existing Flock</h3>
        <form hx-post="/ui/load-flock" hx-target="body" hx-swap="innerHTML" hx-push-url="true" enctype="multipart/form-data">
            <fieldset>
                <legend>Load from server:</legend>
                {% if flock_files %}
                    <label for="flock_file_select">Select a Flock file:</label>
                    <select id="flock_file_select" name="flock_file_select">
                        <option value="" disabled selected>-- Choose a file --</option>
                        {% for file_name in flock_files %}
                            <option value="{{ file_name }}">{{ file_name }}</option>
                        {% endfor %}
                    </select>
                {% else %}
                    <p>No Flock files found on the server in <code>./.flock_ui_projects/</code> directory.</p>
                {% endif %}
            </fieldset>
            <fieldset>
                <legend>Or upload a file:</legend>
                <label for="flock_file_upload">Upload .flock.yaml, .yaml, or .yml file:</label>
                <input type="file" id="flock_file_upload" name="flock_file_upload" accept=".yaml,.yml,.flock">
            </fieldset>
            <button type="submit">Load Flock and Open Editor</button>
        </form>
    </section>
</article>
{% endblock %}
""",
            "flock_editor.html": """\
{% extends "base.html" %}

{% block title %}Flock Editor - {{ flock.name if flock else 'No Flock Loaded' }}{% endblock %}

{% block content %}
<div class="editor-grid">
    <section id="flock-properties-panel" hx-get="/api/flocks/htmx/flock-properties-form" hx-trigger="load, flockPropertiesUpdated from:body" hx-swap="innerHTML">
        <!-- Flock properties form will be loaded here -->
        <p>Loading Flock properties...</p>
        <progress></progress>
    </section>

    <section id="agent-list-panel" hx-get="/api/flocks/htmx/agent-list" hx-trigger="load, agentListChanged from:body" hx-swap="innerHTML">
        <!-- Agent list will be loaded here -->
        <p>Loading agents...</p>
        <progress></progress>
    </section>

    <section id="agent-detail-panel">
        <!-- Agent details/form will be loaded here when an agent is selected or "Add New" is clicked -->
        <article>
            <p>Select an agent from the list to view/edit its details, or click "Add New Agent".</p>
        </article>
    </section>

    <section id="execution-panel" hx-get="/api/flocks/htmx/execution-form" hx-trigger="load, executionFormNeedsUpdate from:body" hx-swap="innerHTML">
        <!-- Execution form will be loaded here -->
        <p>Loading execution controls...</p>
        <progress></progress>
    </section>
</div>

<section id="results-display-container">
    <h3>Execution Results</h3>
    <div id="results-display">
        <p>Results will appear here after running the Flock.</p>
    </div>
</section>

<!-- Future log display
<section id="log-display-container">
    <h3>Logs</h3>
    <div id="log-display">
        <p>Logs will appear here.</p>
    </div>
</section>
-->
{% endblock %}
""",
            "registry_viewer.html": """\
{% extends "base.html" %}

{% block title %}Flock UI - Registry Viewer{% endblock %}

{% block content %}
<article>
    <header>
        <h2>Flock Registry Viewer</h2>
        <p>Browse items registered with the Flock framework.</p>
    </header>

    <nav>
        <ul>
            <li><button role="button" hx-get="/api/registry/htmx/type/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Types</button></li>
            <li><button role="button" hx-get="/api/registry/htmx/tool/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Tools/Callables</button></li>
            <li><button role="button" hx-get="/api/registry/htmx/component/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Components</button></li>
        </ul>
    </nav>
    <div id="registry-loading" class="htmx-indicator">
        <progress></progress> Loading...
    </div>
    <div id="registry-table-container">
        <p>Select a category above to view registered items.</p>
    </div>
</article>
{% endblock %}
""",
            "partials": {
                "_flock_properties_form.html": """\
<article id="flock-properties-form-article">
    <header>
        <h4>Flock Properties {% if current_filename %}(Editing: {{ current_filename }}){% endif %}</h4>
    </header>
    {% if update_message %}
        <div class="form-message {{ 'success' if success else 'error' }}" role="alert">{{ update_message }}</div>
    {% endif %}
    <form hx-post="/api/flocks/htmx/flock-properties" hx-target="#flock-properties-form-article" hx-swap="outerHTML" hx-indicator="#flock-props-loading">
        <label for="flock_name">Flock Name</label>
        <input type="text" id="flock_name" name="flock_name" value="{{ flock.name if flock else '' }}" required>

        <label for="default_model">Default Model</label>
        <input type="text" id="default_model" name="default_model" value="{{ flock.model if flock and flock.model else '' }}" placeholder="e.g., openai/gpt-4o">

        <label for="description">Description</label>
        <textarea id="description" name="description">{{ flock.description if flock and flock.description else '' }}</textarea>
        <div class="grid">
            <button type="submit">Update Properties <span id="flock-props-loading" class="htmx-indicator"><progress indeterminate></progress></span></button>
        </div>
    </form>
    <hr>
     <form hx-post="/ui/save-flock" hx-target="#flock-properties-form-article" hx-swap="outerHTML" hx-indicator="#flock-save-loading">
        <label for="save_filename">Save Flock As:</label>
        <input type="text" id="save_filename" name="save_filename" value="{{ current_filename if current_filename else (flock.name + '.flock.yaml' if flock else 'my_flock.flock.yaml') }}" required
               placeholder="filename.flock.yaml">
        <small>Will save to <code>./.flock_ui_projects/</code>. Use <code>.flock.yaml</code>, <code>.yaml</code>, or <code>.yml</code>.</small>
        <div class="grid">
            <button type="submit">Save to File <span id="flock-save-loading" class="htmx-indicator"><progress indeterminate></progress></span></button>
        </div>
    </form>
    {% if save_message %}
        <div class="form-message {{ 'success' if success else 'error' }}" role="alert" style="margin-top: 1rem;">{{ save_message }}</div>
    {% endif %}
</article>
""",
                "_agent_list.html": """\
<article id="agent-list-content">
    <header class="grid">
        <h4>Agents ({{ flock.agents|length }})</h4>
        <div style="text-align: right;">
            <button role="button" class="outline" hx-get="/api/flocks/htmx/agents/new-agent-form" hx-target="#agent-detail-panel" hx-swap="innerHTML">Add New Agent</button>
        </div>
    </header>
    {% if message %}
        <div class="form-message {{ 'success' if success else 'error' }}">{{ message }}</div>
    {% endif %}
    {% if flock.agents %}
    <ul>
        {% for agent_name, agent in flock.agents.items() %}
        <li hx-get="/api/flocks/htmx/agents/{{ agent.name }}/details-form" hx-target="#agent-detail-panel" hx-swap="innerHTML" hx-indicator="#agent-detail-loading">
            <strong>{{ agent.name }}</strong><br>
            <small>{{ agent.description|truncate(80) if agent.description else 'No description' }}</small>
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No agents defined in this Flock yet. Click "Add New Agent" to create one.</p>
    {% endif %}
    <div id="agent-list-loading" class="htmx-indicator">Loading agents... <progress></progress></div>
</article>
""",
                "_agent_detail_form.html": """\
<article id="agent-detail-form-content">
    <header>
        <h4>{% if is_new %}Add New Agent{% else %}Edit Agent: {{ agent.name if agent else '' }}{% endif %}</h4>
    </header>
    {% if form_message %}
        <div class="form-message {{ 'success' if success else 'error' }}">{{ form_message }}</div>
    {% endif %}
    {% if error_message %} {# For direct error rendering on form, e.g. validation #}
        <div class="form-message error">{{ error_message }}</div>
    {% endif %}

    <form {% if is_new %}
              hx-post="/api/flocks/htmx/agents"
          {% else %}
              hx-put="/api/flocks/htmx/agents/{{ agent.name }}"
          {% endif %}
          hx-target="#agent-detail-form-content" {# Re-render this form with message #}
          hx-swap="innerHTML"
          hx-indicator="#agent-detail-loading-indicator">

        <fieldset>
            <label for="agent_name_field">Name *</label>
            <input type="text" id="agent_name_field" name="agent_name" value="{{ agent.name if agent else '' }}" required placeholder="my_processing_agent">

            <label for="agent_description_field">Description</label>
            <textarea id="agent_description_field" name="agent_description" placeholder="Briefly describe what this agent does.">{{ agent.description if agent else '' }}</textarea>

            <label for="agent_model_field">Model Override (Optional)</label>
            <input type="text" id="agent_model_field" name="agent_model" value="{{ agent.model if agent and agent.model else '' }}" placeholder="e.g., openai/gpt-3.5-turbo (uses Flock default if blank)">

            <label for="input_signature_field">Input Signature *</label>
            <input type="text" id="input_signature_field" name="input_signature" value="{{ agent.input if agent else '' }}" required placeholder="e.g., query: str | The user's question, context: list[str]">
            <small>Format: `name1: type1 | desc1, name2: type2 | desc2`</small>

            <label for="output_signature_field">Output Signature *</label>
            <input type="text" id="output_signature_field" name="output_signature" value="{{ agent.output if agent else '' }}" required placeholder="e.g., answer: str | The final answer, sources: list[str]">
            <small>Format: `name1: type1 | desc1, name2: type2 | desc2`</small>
        </fieldset>

        <fieldset>
            <legend>Tools (Optional)</legend>
            <div class="tool-checklist">
            {% if registered_tools %}
                {% for tool in registered_tools %}
                <label for="tool_{{ tool.name }}">
                    <input type="checkbox" id="tool_{{ tool.name }}" name="tools" value="{{ tool.name }}"
                           {% if tool.name in current_tools %}checked{% endif %}>
                    {{ tool.name }} <small>({{ tool.module }})</small>
                </label>
                {% endfor %}
            {% else %}
                <p>No tools registered. Add tools via the Registry.</p>
            {% endif %}
            </div>
        </fieldset>
        
        <!-- MVP: Simplified Router Config - just DefaultRouter hand_off target -->
        <fieldset>
            <legend>Routing (Default Handoff)</legend>
            <label for="agent_handoff_field">Next Agent Name (Optional)</label>
            <input type="text" id="agent_handoff_field" name="default_router_handoff" 
                   value="{{ agent.handoff_router.config.hand_off if agent and agent.handoff_router and agent.handoff_router.config and agent.handoff_router.config.hand_off is string else '' }}" 
                   placeholder="Enter name of next agent to call">
            <small>If set, this agent will hand off to the specified agent by default.</small>
        </fieldset>


        <div class="grid">
            <button type="submit">
                {% if is_new %}Create Agent{% else %}Save Changes{% endif %}
            </button>
            {% if not is_new and agent %}
            <button type="button" role="button" class="secondary outline"
                    hx-delete="/api/flocks/htmx/agents/{{ agent.name }}"
                    hx-target="#agent-detail-form-content" {# Clears form on success, re-renders list via trigger #}
                    hx-confirm="Are you sure you want to delete agent '{{ agent.name }}'?"
                    hx-indicator="#agent-detail-loading-indicator">
                Delete Agent
            </button>
            {% endif %}
            <button type="button" class="outline" hx-get="/api/flocks/htmx/agents/new-agent-form" hx-target="#agent-detail-panel" hx-swap="innerHTML">
                Cancel / New
            </button>
        </div>
        <div id="agent-detail-loading-indicator" class="htmx-indicator">
            <progress indeterminate></progress> Processing...
        </div>
    </form>
</article>
""",
                "_agent_tools_checklist.html": """\
<!-- This partial might be used if tool selection becomes more complex -->
<!-- For MVP, it's integrated into _agent_detail_form.html -->
<fieldset>
    <legend>Select Tools</legend>
    {% for tool in registered_tools %}
    <label for="tool_{{ tool.name }}_{{ context_id }}"> <!-- context_id for uniqueness if form is loaded multiple times -->
        <input type="checkbox" id="tool_{{ tool.name }}_{{ context_id }}" name="tools" value="{{ tool.name }}"
               {% if tool.name in current_tools %}checked{% endif %}>
        {{ tool.name }} <small>({{ tool.module }})</small>
    </label>
    {% else %}
    <p>No tools available in registry.</p>
    {% endfor %}
</fieldset>
""",
                "_execution_form.html": """\
<article id="execution-form-content">
    <header>
        <h4>Run Flock</h4>
    </header>
    {% if flock and flock.agents %}
    <form hx-post="/api/flocks/htmx/run" hx-target="#results-display" hx-swap="innerHTML" hx-indicator="#run-loading-indicator">
        <label for="start_agent_name">Select Start Agent:</label>
        <select id="start_agent_name" name="start_agent_name" required
                hx-get="/api/flocks/htmx/agents/" <!-- Base URL part -->
                hx-vars="'agent_name': this.value" <!-- Current selected value -->
                hx-trigger="change"
                hx-target="#dynamic-input-form-fields"
                hx-swap="innerHTML"
                hx-indicator="#input-form-loading-indicator">
            <option value="" disabled selected>-- Choose an agent --</option>
            {% for agent_name in flock.agents.keys() %}
            <option value="{{ agent_name }}">{{ agent_name }}</option>
            {% endfor %}
        </select>

        <div id="dynamic-input-form-fields">
            <!-- Input fields for the selected agent will be loaded here -->
            <p><small>Select an agent to see its input fields.</small></p>
        </div>
        <div id="input-form-loading-indicator" class="htmx-indicator">
            <progress indeterminate></progress> Loading input form...
        </div>

        <button type="submit">Run Flock</button>
        <span id="run-loading-indicator" class="htmx-indicator">
            <progress indeterminate></progress> Running...
        </span>
    </form>
    {% else %}
    <p>No agents available in the current Flock. Add agents to run.</p>
    {% endif %}
</article>
""",
                "_dynamic_input_form_content.html": """\
{% if input_fields %}
    {% for field in input_fields %}
    <fieldset> {# Group each field #}
        <label for="agent_input_{{ field.name }}">{{ field.name }} ({{ field.type }})</label>
        {% if field.description %}
            <small>{{ field.description }}</small>
        {% endif %}
        {% if field.html_type == 'textarea' %}
            <textarea id="agent_input_{{ field.name }}" name="agent_input_{{ field.name }}" rows="3" placeholder="{{ field.placeholder if field.placeholder else ('Enter ' + field.type) }}"></textarea>
        {% elif field.html_type == 'checkbox' %}
            <label for="agent_input_{{ field.name }}_cb">
                <input type="checkbox" id="agent_input_{{ field.name }}_cb" name="agent_input_{{ field.name }}" value="true">
                Enabled
            </label>
        {% else %}
            <input type="{{ field.html_type }}" id="agent_input_{{ field.name }}" name="agent_input_{{ field.name }}" placeholder="{{ field.placeholder if field.placeholder else ('Enter ' + field.type) }}">
        {% endif %}
    </fieldset>
    {% endfor %}
{% else %}
    <p><small>This agent requires no specific inputs, or input signature could not be parsed.</small></p>
{% endif %}
""",
                "_results_display.html": """\
{% if result_data is string %}
    <p class="error">{{ result_data }}</p>
{% elif result_data %}
    <pre><code>{{ result_data | tojson(indent=2) }}</code></pre>
{% else %}
    <p>No results to display yet.</p>
{% endif %}
""",
                "_registry_table.html": """\
<header><h5>{{ item_type_display }}</h5></header>
{% if items %}
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Module Path</th>
        </tr>
    </thead>
    <tbody>
        {% for item in items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.module }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>No {{ item_type_display.lower() }} found in the registry.</p>
{% endif %}
"""
            }
        },
        ".env.example": """\
# LLM API Keys (replace with your actual keys)
# OPENAI_API_KEY="sk-..."
# ANTHROPIC_API_KEY="sk-ant-..."
# TAVILY_API_KEY="tvly-..."

# Directory for storing .flock.yaml files (default is ./.flock_ui_projects)
# FLOCK_FILES_DIR="./my_flocks"
""",
        "requirements.txt": """\
fastapi
uvicorn[standard]
jinja2
python-multipart
# flock-core (install separately or via editable install if developing)
# PyYAML (likely a flock-core dependency)
# python-dotenv (if you want to load .env automatically without FastAPI's built-in, usually not needed)
""",
        "run.py": """\
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8008, reload=True)
"""
    }
}

def create_project_structure(base_path, structure):
    """
    Recursively creates directories and files based on the structure.
    """
    for name, content in structure.items():
        path = base_path / name
        if isinstance(content, dict):  # It's a directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {path}")
            create_project_structure(path, content)
        else:  # It's a file
            try:
                path.write_text(content, encoding='utf-8')
                print(f"Created file:      {path}")
            except Exception as e:
                print(f"Error creating file {path}: {e}")

if __name__ == "__main__":
    # current_working_dir = Path(os.getcwd())
    # Set the root to 'flock-ui' within the current working directory
    project_root_name = list(PROJECT_STRUCTURE.keys())[0] # Should be "flock-ui"
    project_base_path = Path(os.getcwd()) / project_root_name

    if project_base_path.exists():
        print(f"Directory '{project_base_path}' already exists.")
        override = input("Do you want to override it? (yes/no): ").lower()
        if override == 'yes':
            print(f"Removing existing directory: {project_base_path}")
            shutil.rmtree(project_base_path)
        else:
            print("Generation cancelled.")
            exit()

    print(f"Generating project structure in: {project_base_path}")
    create_project_structure(Path(os.getcwd()), PROJECT_STRUCTURE) # Pass CWD as base, structure has "flock-ui" root
    print("\nProject structure generated successfully!")
    print(f"To run the application:")
    print(f"1. cd {project_root_name}")
    print(f"2. Create a virtual environment and install requirements: ")
    print(f"   python -m venv venv")
    print(f"   source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows")
    print(f"   pip install -r requirements.txt")
    print(f"   pip install flock-core # or your local editable install if developing flock-core")
    print(f"3. Create a '.env' file in '{project_root_name}/' if you need API keys for flock-core execution.")
    print(f"4. Ensure the directory '{project_root_name}/app/config.py' points FLOCK_FILES_DIR to './.flock_ui_projects/' or your desired location inside 'flock-ui'.")
    print(f"5. Run the FastAPI server: python run.py")
    print(f"6. Open your browser to http://127.0.0.1:8008")