import os
from pathlib import Path

# --- Files to Update ---
# Structure: "relative_path_to_file_in_flock_ui": """New content"""
FILES_TO_UPDATE = {
    "app/main.py": """\
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import urllib.parse # For encoding messages in URL

from app.config import FLOCK_FILES_DIR
from app.services.flock_service import (
    get_current_flock_instance,
    load_flock_from_file_service,
    create_new_flock_service,
    get_available_flock_files,
    clear_current_flock, # New service function
    get_current_flock_filename
)
from app.api import flock_management, agent_management, execution, registry_viewer

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
""",
    "app/api/execution.py": """\
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

from app.services.flock_service import get_current_flock_instance, run_current_flock_service
from flock.core.util.spliter import parse_schema # Corrected import location

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/htmx/execution-form", response_class=HTMLResponse)
async def htmx_get_execution_form(request: Request):
    flock = get_current_flock_instance()
    # Template will handle None flock or no agents
    return templates.TemplateResponse(
        "partials/_execution_form.html", 
        {"request": request, "flock": flock, "input_fields": [], "selected_agent_name": None}
    )

@router.get("/htmx/agents/{agent_name}/input-form", response_class=HTMLResponse)
async def htmx_get_agent_input_form(request: Request, agent_name: str):
    flock = get_current_flock_instance()
    if not flock: return HTMLResponse("<p class='error'>No Flock loaded to get agent inputs.</p>") 
    agent = flock.agents.get(agent_name)
    if not agent: return HTMLResponse(f"<p class='error'>Agent '{agent_name}' not found.</p>")

    input_fields = []
    if agent.input and isinstance(agent.input, str):
        try:
            parsed_spec = parse_schema(agent.input) # [(name, type_str, description), ...]
            for name, type_str, description in parsed_spec:
                field_info = {"name": name, "type": type_str.lower(), "description": description or ""}
                if "bool" in field_info["type"]: field_info["html_type"] = "checkbox"
                elif "int" in field_info["type"] or "float" in field_info["type"]: field_info["html_type"] = "number"
                elif "list" in field_info["type"] or "dict" in field_info["type"]:
                     field_info["html_type"] = "textarea"
                     field_info["placeholder"] = f"Enter JSON for {field_info['type']}"
                else: field_info["html_type"] = "text"
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
    # Ensure agent.input is a string before parsing
    if agent.input and isinstance(agent.input, str):
        try:
            parsed_spec = parse_schema(agent.input)
            for name, type_str, _ in parsed_spec:
                # Input names in form are "agent_input_{name}"
                form_field_name = f"agent_input_{name}"
                raw_value = form_data.get(form_field_name)

                if raw_value is None and "bool" in type_str.lower():
                    inputs[name] = False # Checkbox not sent if unchecked
                    continue
                if raw_value is None:
                    # For MVP, if a field defined in signature is not in form, treat as error or None
                    # Or ensure all fields are always rendered, even if empty
                    # For now, let's assume if it's not in form data, it's not provided (becomes None or default in Flock core)
                    inputs[name] = None 
                    continue

                # Type conversion logic
                if "int" in type_str.lower():
                    try: inputs[name] = int(raw_value)
                    except ValueError: return HTMLResponse(f"<p class='error'>Invalid integer for '{name}': '{raw_value}'.</p>")
                elif "float" in type_str.lower():
                    try: inputs[name] = float(raw_value)
                    except ValueError: return HTMLResponse(f"<p class='error'>Invalid float for '{name}': '{raw_value}'.</p>")
                elif "bool" in type_str.lower():
                    # Checkboxes send 'on' or 'true' when checked. Or might be missing.
                    # If it's from a checkbox, 'value' might be 'true' or the actual value set on the input
                    inputs[name] = raw_value.lower() in ['true', 'on', '1', 'yes']
                elif "list" in type_str.lower() or "dict" in type_str.lower():
                    try:
                        inputs[name] = json.loads(raw_value)
                    except json.JSONDecodeError:
                        return HTMLResponse(f"<p class='error'>Invalid JSON for '{name}': '{raw_value}'.</p>")
                else: # string
                    inputs[name] = raw_value
        except Exception as e:
            return HTMLResponse(f"<p class='error'>Error processing inputs for {start_agent_name}: {e}</p>")
    
    result_data = await run_current_flock_service(start_agent_name, inputs)

    return templates.TemplateResponse("partials/_results_display.html", {"request": request, "result_data": result_data})

""",
    "app/services/flock_service.py": """\
from flock.core import Flock, FlockFactory, FlockAgent
from flock.core.flock_registry import get_registry
from pathlib import Path
import yaml # For parsing issues, if any, during load

from app.config import CURRENT_FLOCK_INSTANCE, FLOCK_FILES_DIR, CURRENT_FLOCK_FILENAME

def get_available_flock_files() -> list[str]:
    if not FLOCK_FILES_DIR.exists():
        return []
    return sorted([f.name for f in FLOCK_FILES_DIR.iterdir() if f.is_file() and (f.suffix in [".yaml", ".yml", ".flock"])])

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
    # Ensure model is None if empty string, so FlockFactory uses its default or Flock's default
    effective_model = model.strip() if model and model.strip() else None
    CURRENT_FLOCK_INSTANCE = Flock(name=name, model=effective_model, description=description, show_flock_banner=False, enable_logging=False)
    CURRENT_FLOCK_FILENAME = f"{name.replace(' ', '_').lower()}.flock.yaml" # Default filename suggestion
    print(f"Created new flock: {name}")
    return CURRENT_FLOCK_INSTANCE

def get_current_flock_instance() -> Flock | None:
    global CURRENT_FLOCK_INSTANCE
    return CURRENT_FLOCK_INSTANCE

def get_current_flock_filename() -> str | None:
    global CURRENT_FLOCK_FILENAME
    return CURRENT_FLOCK_FILENAME

def set_current_flock_instance(flock: Flock | None): # Not typically called directly by UI
    global CURRENT_FLOCK_INSTANCE
    CURRENT_FLOCK_INSTANCE = flock

def set_current_flock_filename(filename: str | None): # Called by save service
    global CURRENT_FLOCK_FILENAME
    CURRENT_FLOCK_FILENAME = filename
    
def clear_current_flock():
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    CURRENT_FLOCK_INSTANCE = None
    CURRENT_FLOCK_FILENAME = None
    print("Current flock cleared.")

def save_current_flock_to_file_service(new_filename: str) -> tuple[bool, str]:
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    if not CURRENT_FLOCK_INSTANCE:
        return False, "No flock loaded to save."
    
    if not new_filename.strip():
        return False, "Filename cannot be empty."

    save_path = FLOCK_FILES_DIR / new_filename
    try:
        CURRENT_FLOCK_INSTANCE.to_yaml_file(str(save_path))
        CURRENT_FLOCK_FILENAME = new_filename 
        return True, f"Flock saved successfully to {new_filename}."
    except Exception as e:
        return False, f"Error saving flock: {e}"

def update_flock_properties_service(name: str, model: str | None, description: str | None) -> bool:
    global CURRENT_FLOCK_INSTANCE, CURRENT_FLOCK_FILENAME
    if not CURRENT_FLOCK_INSTANCE:
        return False
    
    # Update filename if flock name changes and it was the default derived name
    old_name_default_filename = f"{CURRENT_FLOCK_INSTANCE.name.replace(' ', '_').lower()}.flock.yaml"
    if CURRENT_FLOCK_FILENAME == old_name_default_filename and CURRENT_FLOCK_INSTANCE.name != name:
        CURRENT_FLOCK_FILENAME = f"{name.replace(' ', '_').lower()}.flock.yaml"

    CURRENT_FLOCK_INSTANCE.name = name
    CURRENT_FLOCK_INSTANCE.model = model.strip() if model and model.strip() else None
    CURRENT_FLOCK_INSTANCE.description = description
    return True

def add_agent_to_current_flock_service(agent_config: dict) -> bool:
    global CURRENT_FLOCK_INSTANCE
    if not CURRENT_FLOCK_INSTANCE: return False
    
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
        agent = FlockFactory.create_default_agent(
            name=agent_config["name"],
            description=agent_config.get("description"),
            model=agent_config.get("model"),
            input=agent_config["input"],
            output=agent_config["output"],
            tools=tools_instances if tools_instances else None
        )
        # Handle DefaultRouter handoff if provided
        handoff_target = agent_config.get("default_router_handoff")
        if handoff_target:
            from flock.routers.default.default_router import DefaultRouter, DefaultRouterConfig
            agent.add_component(DefaultRouterConfig(hand_off=handoff_target))

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
        new_name = agent_config["name"]
        agent_to_update.description = agent_config.get("description")
        agent_to_update.model = agent_config.get("model")
        agent_to_update.input = agent_config["input"]
        agent_to_update.output = agent_config["output"]
        agent_to_update.tools = tools_instances if tools_instances else None

        # Handle DefaultRouter handoff
        handoff_target = agent_config.get("default_router_handoff")
        if handoff_target:
            from flock.routers.default.default_router import DefaultRouter, DefaultRouterConfig
            # This will replace existing router or add new one
            agent_to_update.add_component(DefaultRouterConfig(hand_off=handoff_target))
        elif agent_to_update.handoff_router: # If handoff target is empty, remove existing router
            agent_to_update.handoff_router = None


        if original_agent_name != new_name:
            # If name changed, update the key in the flock's agent dictionary
            CURRENT_FLOCK_INSTANCE._agents[new_name] = CURRENT_FLOCK_INSTANCE._agents.pop(original_agent_name)
        agent_to_update.name = new_name # Set new name after pop/re-add if name changed
            
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
        result = await CURRENT_FLOCK_INSTANCE.run_async(start_agent=start_agent_name, input=inputs, box_result=False)
        return result
    except Exception as e:
        print(f"Error during flock execution: {e}") # Log to server console
        return f"Error during flock execution: {str(e)}" # Return user-friendly error

def get_registered_items_service(item_type: str) -> list:
    registry = get_registry()
    items = []
    if item_type == "type": items_dict = registry._types
    elif item_type == "tool": items_dict = registry._callables
    elif item_type == "component": items_dict = registry._components
    else: return []

    for name, item_obj in items_dict.items():
        module_path = "N/A"
        try: module_path = item_obj.__module__
        except AttributeError: pass
        items.append({"name": name, "module": module_path})
    return sorted(items, key=lambda x: x['name']) # Sort for consistent display
""",
    "templates/base.html": """\
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
        body { padding-top: 4.5rem; /* Increased to avoid overlap with potentially taller nav */ }
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background-color: var(--pico-card-background-color);
            border-bottom: 1px solid var(--pico-muted-border-color);
            padding-top: 0.5rem; /* Add some padding inside nav */
            padding-bottom: 0.5rem;
        }
        .message-container {
            position: fixed;
            top: 4.5rem; /* Below the nav */
            left: 50%;
            transform: translateX(-50%);
            z-index: 1001; /* Above content, below modals if any */
            width: auto;
            max-width: 80%;
            padding: 0; margin: 0;
        }
        .message-container > div { /* Style for the actual message div */
            margin-top: 0.5rem;
            box-shadow: var(--pico-card-box-shadow);
        }
    </style>
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><strong><a href="/" style="text-decoration: none;">Flock UI 🐤</a></strong></li>
        </ul>
        <ul>
            <li><a href="/" role="button" {% if request.url.path == '/' %}aria-current="page"{% else %}class="outline"{% endif %}>Dashboard</a></li>
            <li><a href="/ui/editor" role="button" {% if request.url.path.startswith('/ui/editor') %}aria-current="page"{% else %}class="outline"{% endif %}>Editor</a></li>
            <li><a href="/ui/registry" role="button" {% if request.url.path.startswith('/ui/registry') %}aria-current="page"{% else %}class="outline"{% endif %}>Registry</a></li>
        </ul>
    </nav>

    <div class="message-container" 
         x-data="{ showSuccess: {{ 'true' if success_message else 'false' }}, showError: {{ 'true' if error_message else 'false' }}, successMsg: '{{ success_message }}', errorMsg: '{{ error_message }}' }"
         x-init="
            if (successMsg) { setTimeout(() => showSuccess = false, 5000); }
            if (errorMsg) { setTimeout(() => showError = false, 7000); }
         "
         @notify.window="
            if ($event.detail.type === 'success') { successMsg = $event.detail.message; showSuccess = true; setTimeout(() => showSuccess = false, 5000); }
            if ($event.detail.type === 'error') { errorMsg = $event.detail.message; showError = true; setTimeout(() => showError = false, 7000); }
         ">
        <template x-if="showSuccess">
            <div class="success" role="alert" x-text="successMsg" @click="showSuccess = false" style="cursor: pointer;"></div>
        </template>
        <template x-if="showError">
            <div class="error" role="alert" x-text="errorMsg" @click="showError = false" style="cursor: pointer;"></div>
        </template>
    </div>

    <main class="container">
        {% block content %}{% endblock %}
    </main>
    <footer class="container">
        <small>Built with FastAPI, HTMX, Pico.CSS, and ❤️ for Flock</small>
    </footer>
</body>
</html>
""",
    "templates/flock_editor.html": """\
{% extends "base.html" %}

{% block title %}Flock Editor - {{ flock.name if flock else 'No Flock Loaded' }}{% endblock %}

{% block content %}
<div class="editor-layout-grid">
    <aside class="editor-sidebar">
        <section id="flock-properties-panel" 
                 hx-get="/api/flocks/htmx/flock-properties-form" 
                 hx-trigger="load, flockPropertiesUpdated from:body" 
                 hx-swap="innerHTML">
            <article><p>Loading Flock properties...</p><progress></progress></article>
        </section>

        <section id="agent-list-panel" 
                 hx-get="/api/flocks/htmx/agent-list" 
                 hx-trigger="load, agentListChanged from:body" 
                 hx-swap="innerHTML">
            <article><p>Loading agents...</p><progress></progress></article>
        </section>

        <section id="execution-panel" 
                 hx-get="/api/flocks/htmx/execution-form" 
                 hx-trigger="load, executionFormNeedsUpdate from:body" 
                 hx-swap="innerHTML">
            <article><p>Loading execution controls...</p><progress></progress></article>
        </section>
    </aside>

    <main class="editor-main-content">
        <section id="agent-detail-panel">
            <article>
                <header><h4>Agent Details</h4></header>
                <p>Select an agent from the list to view/edit its details, or click "Add New Agent" in the agent list.</p>
            </article>
        </section>

        <section id="results-display-container">
            <header><h4>Execution Results</h4></header>
            <div id="results-display">
                <p>Results will appear here after running the Flock.</p>
            </div>
        </section>
    </main>
</div>
{% endblock %}
""",
    "templates/registry_viewer.html": """\
{% extends "base.html" %}

{% block title %}Flock UI - Registry Viewer{% endblock %}

{% block content %}
<article>
    <header>
        <h2>Flock Registry Viewer</h2>
        <p>Browse items registered with the Flock framework.</p>
    </header>

    <nav>
      <ul class="grid">
        <li><button role="button" class="outline" hx-get="/api/registry/htmx/type/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Types</button></li>
        <li><button role="button" class="outline" hx-get="/api/registry/htmx/tool/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Tools/Callables</button></li>
        <li><button role="button" class="outline" hx-get="/api/registry/htmx/component/table" hx-target="#registry-table-container" hx-indicator="#registry-loading">View Components</button></li>
      </ul>
    </nav>
    <div id="registry-loading" class="htmx-indicator" style="text-align: center;">
        <progress></progress> Loading...
    </div>
    <div id="registry-table-container">
        <p>Select a category above to view registered items.</p>
    </div>
    <footer style="margin-top: 2rem;">
        <a href="/ui/editor" role="button" class="secondary">Back to Editor</a>
    </footer>
</article>
{% endblock %}
""",
    "static/css/custom.css": """\
/* Global styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    padding-bottom: 4rem; /* Space for footer */
}

/* Navigation */
nav ul li strong a { /* For the brand link */
    color: var(--pico-h1-color);
    text-decoration: none;
}
nav ul li a[role="button"][aria-current="page"] { /* Active nav button */
    /* Pico handles this by default with aria-current, but we can override */
}


/* Messages (success/error) */
.message-container > div {
    padding: 0.75rem;
    margin-bottom: 1rem; /* Spacing between multiple messages if they appear */
    border-radius: var(--pico-border-radius);
    font-weight: 500;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.message-container .success {
    background-color: var(--pico-ins-color);
    color: var(--pico-primary-inverse);
    border: 1px solid var(--pico-ins-color);
}
.message-container .error {
    background-color: var(--pico-del-color);
    color: var(--pico-primary-inverse);
    border: 1px solid var(--pico-del-color);
}
.message-container .close { /* Simple close button for messages */
    background: none;
    border: none;
    color: inherit;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0 0.5rem;
}


/* Editor Layout - Two Column */
.editor-layout-grid {
    display: grid;
    grid-template-columns: minmax(300px, 1fr) 2fr; /* Sidebar fixed-ish, main content flexible */
    gap: var(--pico-spacing);
    margin-top: var(--pico-spacing);
}

.editor-sidebar > section,
.editor-main-content > section {
    margin-bottom: var(--pico-spacing);
}
.editor-sidebar article, .editor-main-content article { /* Ensure articles within sections don't add extra margins unless needed */
    margin-bottom: 0; 
}


/* Styling for panels/articles within the editor */
#flock-properties-panel article,
#agent-list-panel article,
#agent-detail-panel article,
#execution-panel article,
#results-display-container article { /* If results are wrapped in article */
    padding: var(--pico-block-spacing-vertical) var(--pico-block-spacing-horizontal);
}
#flock-properties-panel header h4,
#agent-list-panel header h4,
#agent-detail-panel header h4,
#execution-panel header h4,
#results-display-container header h4 {
    margin-bottom: var(--pico-typography-spacing-vertical);
}


/* Agent List Styling */
#agent-list-panel ul {
    list-style-type: none;
    padding: 0;
    max-height: 50vh; /* Allow scrolling for long lists */
    overflow-y: auto;
}
#agent-list-panel li {
    padding: 0.75rem;
    border: 1px solid var(--pico-muted-border-color);
    margin-bottom: 0.5rem;
    border-radius: var(--pico-border-radius);
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
}
#agent-list-panel li:hover, #agent-list-panel li.htmx-settling {
    background-color: var(--pico-muted-hover-background-color);
}
#agent-list-panel li.selected-agent { /* Add a class for selected agent if you implement that client-side */
    background-color: var(--pico-primary-focus);
    border-color: var(--pico-primary);
    color: var(--pico-primary-inverse);
}
#agent-list-panel li small {
    color: var(--pico-muted-color);
}


/* Agent Detail Form */
#agent-detail-form-content fieldset {
    margin-bottom: 1rem;
    padding-bottom: 0.5rem; /* Space before next fieldset or buttons */
    border-bottom: 1px solid var(--pico-muted-border-color);
}
#agent-detail-form-content fieldset:last-of-type {
    border-bottom: none; /* No border for the last fieldset */
    margin-bottom: 0;
}
#agent_detail_form_content .grid { /* For button groups */
    margin-top: 1rem;
}


/* Tool Checklist */
.tool-checklist {
    max-height: 150px; /* Example max height */
    overflow-y: auto;
    border: 1px solid var(--pico-muted-border-color);
    padding: 0.5rem;
    margin-bottom: 0.75rem;
    border-radius: var(--pico-border-radius);
}
.tool-checklist label {
    display: block;
    margin-bottom: 0.25rem;
    font-weight: normal; /* Make tool labels normal weight */
}
.tool-checklist input[type="checkbox"] {
    margin-right: 0.5rem;
}
.tool-checklist label small {
    color: var(--pico-muted-color);
}

/* Execution & Results */
#dynamic-input-form-fields fieldset {
    margin-bottom: 1rem;
    border: 1px solid var(--pico-form-element-border-color);
    padding: 1rem;
    border-radius: var(--pico-border-radius);
}
#dynamic-input-form-fields fieldset legend { /* Style legend if you use it */
    font-weight: bold;
    padding: 0 0.5rem;
}

#results-display {
    background-color: var(--pico-code-background-color);
    color: var(--pico-code-color);
    padding: 1rem;
    border-radius: var(--pico-border-radius);
    overflow-x: auto;
    margin-top: 1rem;
    min-height: 100px; /* Ensure it has some height even when empty */
    border: 1px solid var(--pico-muted-border-color);
}
#results-display pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-all;
}


/* HTMX Indicators */
.htmx-indicator {
    display: none;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
}
.htmx-request .htmx-indicator {
    display: inline-block; /* Or block, depending on context */
    opacity: 1;
    margin-left: 0.5em;
}
.htmx-request.htmx-indicator { /* For elements that become indicators themselves */
    display: inline-block;
    opacity: 1;
}

/* Registry Viewer */
#registry-viewer-page nav ul.grid li button {
    width: 100%; /* Make buttons take full width of grid cell */
}
#registry-table-container table {
    margin-top: 1rem;
}

/* Small utility for form field errors */
.field-error {
    color: var(--pico-del-color);
    font-size: var(--pico-font-size-small);
    margin-top: -0.5rem; /* Pull it closer to the input */
    margin-bottom: 0.5rem;
}
""",
            }
        
# --- Helper to get current working directory ---
BASE_PROJECT_DIR = Path(os.getcwd()) / "flock_ui"

def update_file(relative_path_str: str, new_content: str):
    """
    Overwrites a specific file within the BASE_PROJECT_DIR.
    """
    file_path = BASE_PROJECT_DIR / relative_path_str
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure parent directory exists
        file_path.write_text(new_content, encoding='utf-8')
        print(f"Updated file:      {file_path}")
    except Exception as e:
        print(f"Error updating file {file_path}: {e}")

if __name__ == "__main__":
    if not BASE_PROJECT_DIR.exists():
        print(f"Project directory '{BASE_PROJECT_DIR}' does not exist.")
        print("Please run the initial generation script first if you haven't.")
        exit()

    print(f"Updating files in project: {BASE_PROJECT_DIR}")
    for rel_path, content in FILES_TO_UPDATE.items():
        update_file(rel_path, content)

    print("\nSpecified files updated successfully!")
    print("If the server was running, you might need to restart it for all changes to take effect.")
    print(f"Remember to check the `flock.core.util.spliter` import in `app/api/execution.py` if `parse_schema` is defined there.")