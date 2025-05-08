from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

from flock_ui.app.services.flock_service import get_current_flock_instance, run_current_flock_service
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

