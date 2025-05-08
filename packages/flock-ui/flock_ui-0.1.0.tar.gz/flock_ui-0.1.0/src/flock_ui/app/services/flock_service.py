from flock.core import Flock, FlockFactory, FlockAgent
from flock.core.flock_registry import get_registry
from pathlib import Path
import yaml # For parsing issues, if any, during load

from flock_ui.app.config import CURRENT_FLOCK_INSTANCE, FLOCK_FILES_DIR, CURRENT_FLOCK_FILENAME

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
