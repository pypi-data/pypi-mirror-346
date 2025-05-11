**Overall Goal:** Refactor the `llm-fal` plugin to dynamically discover Fal.ai models and their specific input parameters using undocumented APIs, while providing robust fallbacks and caching mechanisms.

## Tasks

- [x] 1.0 Update Dependencies
  - [x] 1.1 Add `requests` library to `pyproject.toml`
    ```
    # In pyproject.toml
    # Add to [project.dependencies] list:
    "requests>=2.20,<3.0"
    ```
  - [x] 1.2 Add `PyYAML` library to `pyproject.toml` 
    ```
    # In pyproject.toml
    # Add to [project.dependencies] list:
    "PyYAML>=5.0,<7.0"
    ```
  - [x] 1.3 Run `llm install -e .` in development environment to install the new dependencies

- [x] 2.0 Implement Dynamic Model Discovery
  - [x] 2.1 Create `_fetch_all_models_from_api` function in `llm_fal.py` to fetch models from the Fal.ai API with caching
    ```python
    import requests
    import logging

    logger = logging.getLogger(__name__)
    FAL_MODELS_API_URL = "https://fal.ai/api/models"
    _model_list_cache = None # Replace existing _model_cache if only used for this

    def _fetch_all_models_from_api() -> List[Dict[str, Any]]:
        global _model_list_cache
        if _model_list_cache is not None:
            logger.debug("Returning cached model list.")
            return _model_list_cache

        logger.debug(f"Fetching model list from {FAL_MODELS_API_URL}")
        try:
            response = requests.get(FAL_MODELS_API_URL, timeout=10) # Add timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            models = response.json()
            if not isinstance(models, list):
                 logger.error("API response is not a list.")
                 return [] # Or raise? For now, return empty on bad format.
            _model_list_cache = models # Cache the result
            logger.debug(f"Successfully fetched and cached {len(models)} models.")
            return models
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching models from API: {e}")
            return [] # Return empty list on error
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from model API: {e}")
            return []
    ```
  - [x] 2.2 Refactor `get_all_models` function to use dynamic API fetching instead of hardcoded list
    ```python
    # Remove 'async' keyword if changing to sync
    def get_all_models() -> List[Dict[str, Any]]:
        """Fetch all available models from fal.ai API (cached)."""
        # The caching is now handled within _fetch_all_models_from_api
        return _fetch_all_models_from_api()
    ```
  - [x] 2.3 Refactor `get_models_by_category` function to use dynamically fetched models
    ```python
    def get_models_by_category() -> Dict[str, List[Dict[str, Any]]]:
        """Group all available models by category."""
        all_models = get_all_models() # Fetch dynamically
        result = {category: [] for category in MODEL_CATEGORIES.keys()}
        # Ensure 'other' category exists if not in MODEL_CATEGORIES
        if "other" not in result:
            result["other"] = []

        for model in all_models:
            category = get_model_category(model) # Existing categorization logic
            if category in result:
                result[category].append(model)
            else:
                logger.warning(f"Model {model.get('id')} has unknown category '{category}'. Placing in 'other'.")
                result["other"].append(model) # Fallback to 'other'

        # Remove empty categories for cleaner output (optional)
        result = {k: v for k, v in result.items() if v}
        return result
    ```
  - [x] 2.4 Refactor `search_models` function to use dynamically fetched models
    ```python
    def search_models(query: str) -> List[Dict[str, Any]]:
        """Search for models by keyword in ID, name, or description."""
        all_models = get_all_models() # Fetch dynamically
        query = query.lower()
        return [
            model for model in all_models
            if (
                query in model.get("id", "").lower() or
                query in model.get("name", "").lower() or
                query in model.get("description", "").lower() # Assuming description exists
            )
        ]
    ```
  - [x] 2.5 Refactor `register_models` to register models from the API
    ```python
    @llm.hookimpl
    def register_models(register):
        """Register models with LLM CLI."""
        all_models = get_all_models() # Fetch dynamically
        if not all_models:
             logger.warning("No models fetched from Fal.ai API. Cannot register models.")
             return

        logger.info(f"Registering {len(all_models)} models from Fal.ai...")
        for model_data in all_models:
            model_id = model_data.get("id")
            if model_id:
                # Pass the fetched model_data to the constructor
                register(FalModel(model_id=model_id, model_info=model_data))
            else:
                logger.warning(f"Skipping model registration due to missing ID: {model_data}")
    ```

- [x] 3.0 Implement Schema Cache Management
  - [x] 3.1 Define cache and override paths constants in `llm_fal.py`
    ```python
    import llm # Ensure llm is imported
    from pathlib import Path

    # ... other imports ...

    FAL_SCHEMA_CACHE_DIR = Path(llm.user_dir()) / "cache" / "fal-schemas"
    FAL_OVERRIDES_FILE = Path(llm.user_dir()) / "fal-overrides.yaml"
    FAL_SCHEMA_TTL_SECONDS = 86400 # 24 hours
    ```
  - [x] 3.2 Implement override loading from YAML configuration
    ```python
    import yaml # Add import
    from typing import Dict, Any # Ensure these are imported

    _override_config_cache: Optional[Dict[str, Any]] = None

    def _load_override_config() -> Dict[str, Any]:
        """Loads the fal-overrides.yaml file."""
        global _override_config_cache
        if _override_config_cache is not None:
            return _override_config_cache

        if not FAL_OVERRIDES_FILE.exists():
            _override_config_cache = {}
            return {}

        logger.info(f"Loading schema overrides from {FAL_OVERRIDES_FILE}")
        try:
            with open(FAL_OVERRIDES_FILE, 'r') as f:
                overrides = yaml.safe_load(f)
                if not isinstance(overrides, dict):
                    logger.error(f"Override file {FAL_OVERRIDES_FILE} is not a valid dictionary. Ignoring.")
                    overrides = {}
                _override_config_cache = overrides
                return overrides
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML override file {FAL_OVERRIDES_FILE}: {e}. Ignoring overrides.")
            _override_config_cache = {}
            return {}
        except Exception as e:
            logger.error(f"Error reading override file {FAL_OVERRIDES_FILE}: {e}. Ignoring overrides.")
            _override_config_cache = {}
            return {}
    ```
  - [x] 3.3 Implement schema cache TTL mechanism to handle cache expiration
    ```python
    # Found existing implementation of cache validation functions already in the code:
    # _is_schema_cache_valid - Checks if a cache file exists and hasn't expired based on TTL
    # _get_schema_cache_path - Gets a Path for a schema cache file
    # _load_schema_from_cache - Loads schema from cache if valid
    # _save_schema_to_cache - Saves schema to cache

    # The existing functions check expiration based on file modification time:
    if (time.time() - cache_mtime) < FAL_SCHEMA_TTL_SECONDS:
        # Cache is valid
        return True
    else:
        # Cache has expired
        return False
    ```
  - [x] 3.4 Add cache clearing functionality to handle stale data
    ```python
    def _invalidate_schema_cache(model_id: Optional[str] = None) -> bool:
        """
        Invalidate schema cache for a specific model or all models.
        
        Args:
            model_id: Optional model ID to invalidate cache for. 
                     If None, invalidate all schema caches.
                     
        Returns:
            True if cache was invalidated, False if no action was taken
        """
        try:
            if model_id:
                # Invalidate cache for specific model
                cache_file = _get_schema_cache_path(model_id)
                if cache_file.exists():
                    cache_file.unlink()
                    logger.debug(f"Invalidated schema cache for model {model_id}")
                    return True
                else:
                    logger.debug(f"No cache file found for model {model_id}")
                    return False
            else:
                # Invalidate all caches if directory exists
                if FAL_SCHEMA_CACHE_DIR.exists():
                    # Check if directory has any schema files
                    cache_files = list(FAL_SCHEMA_CACHE_DIR.glob("*.json"))
                    if not cache_files:
                        logger.debug("Schema cache directory exists but contains no files")
                        return False
                        
                    # Delete all schema files
                    for file in cache_files:
                        file.unlink()
                    logger.debug(f"Invalidated {len(cache_files)} schema cache files")
                    return True
                else:
                    logger.debug("Schema cache directory does not exist")
                    return False
        except Exception as e:
            logger.error(f"Error invalidating schema cache: {e}")
            return False
            
    def _clear_all_caches() -> Tuple[bool, bool, str]:
        """
        Clear all caches (model list and schema caches).
        
        Returns:
            Tuple containing:
                - Boolean indicating if schema cache was cleared
                - Boolean indicating if model list cache was cleared
                - String with detailed status message
        """
        global _model_list_cache
        cleared_schemas = False
        cleared_list = False
        messages = []
        
        # Clear schema cache directory
        if FAL_SCHEMA_CACHE_DIR.exists():
            try:
                import shutil
                shutil.rmtree(FAL_SCHEMA_CACHE_DIR)
                messages.append(f"Cleared schema cache: {FAL_SCHEMA_CACHE_DIR}")
                cleared_schemas = True
            except Exception as e:
                messages.append(f"Error clearing schema cache {FAL_SCHEMA_CACHE_DIR}: {e}")
        else:
            messages.append("Schema cache directory not found.")
        
        # Clear in-memory model list cache
        if _model_list_cache is not None:
            _model_list_cache = None
            messages.append("Cleared in-memory model list cache.")
            cleared_list = True
        else:
            messages.append("In-memory model list cache was already empty.")
        
        # Also clear override cache if it exists
        global _override_config_cache
        if _override_config_cache is not None:
            _override_config_cache = None
            messages.append("Cleared in-memory override configuration cache.")
        
        # Generate summary message
        if not cleared_schemas and not cleared_list:
            summary = "No caches found to clear."
        else:
            summary = "Cache clearing complete."
        
        messages.append(summary)
        return cleared_schemas, cleared_list, "\n".join(messages)
    ```

- [x] 4.0 Implement Dynamic Schema Fetching
  - [x] 4.1 Create `_get_processed_schema` function to fetch schemas from API
    ```python
    import time
    import json # Ensure json is imported

    FAL_SCHEMA_API_URL_TEMPLATE = "https://fal.ai/api/openapi/queue/openapi.json?endpoint_id={model_id}"

    def _get_processed_schema(model_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches schema from API or cache, validates (basic), applies overrides.
        Returns the processed input schema dictionary or None on failure.
        """
        FAL_SCHEMA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Sanitize model_id for filename
        safe_filename = model_id.replace('/', '_').replace(':', '_') + ".json"
        cache_file = FAL_SCHEMA_CACHE_DIR / safe_filename

        # 1. Check Cache
        if cache_file.exists():
            try:
                cache_mtime = cache_file.stat().st_mtime
                if (time.time() - cache_mtime) < FAL_SCHEMA_TTL_SECONDS:
                    logger.debug(f"Using cached schema for {model_id}")
                    with open(cache_file, 'r') as f:
                        schema_data = json.load(f)
                    # Apply overrides even to cached data
                    return _apply_overrides_to_schema(model_id, schema_data)
                else:
                    logger.debug(f"Cache expired for {model_id}")
            except Exception as e:
                logger.warning(f"Could not read cache file {cache_file}: {e}. Refetching.")

        # 2. Fetch from API
        schema_url = FAL_SCHEMA_API_URL_TEMPLATE.format(model_id=model_id)
        logger.debug(f"Fetching schema for {model_id} from {schema_url}")
        try:
            response = requests.get(schema_url, timeout=10)
            response.raise_for_status()
            raw_schema = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API error fetching schema for {model_id}: {e}")
            return None # Indicate failure
        except json.JSONDecodeError as e:
            logger.error(f"API error decoding schema JSON for {model_id}: {e}")
            return None # Indicate failure

        # 3. Basic Validation & Extraction (Adapt based on actual schema structure)
        try:
            # Example: Adjust path based on actual schema structure found via inspection
            # Need to sanitize the model ID key used within the schema components
            schema_model_key = model_id.replace('/', '').replace('-', '').replace('.', '') + "Input" # Heuristic, might need refinement
            input_schema = raw_schema["components"]["schemas"][schema_model_key]
            if not isinstance(input_schema.get("properties"), dict):
                 raise ValueError("Schema missing 'properties' dictionary.")
            # Add more checks as needed (e.g., presence of 'required' list)
            logger.debug(f"Schema validation passed (basic) for {model_id}")

            # 4. Save to Cache
            try:
                with open(cache_file, 'w') as f:
                    json.dump(input_schema, f, indent=2) # Save only the extracted input part
                logger.debug(f"Saved schema to cache for {model_id}")
            except Exception as e:
                logger.warning(f"Could not write schema cache file {cache_file}: {e}")

            # 5. Apply Overrides
            return _apply_overrides_to_schema(model_id, input_schema)

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Invalid schema structure for {model_id}: {e}. Raw schema: {raw_schema}")
            # Optionally save the broken schema for debugging
            # broken_cache_file = cache_file.with_suffix(".broken.json")
            # with open(broken_cache_file, 'w') as f: json.dump(raw_schema, f, indent=2)
            return None # Indicate failure
    ```
  - [x] 4.2 Implement basic schema validation and extraction logic based on model_id
  - [x] 4.3 Build caching mechanism for schemas with expiration based on TTL
  - [x] 4.4 Implement `_apply_overrides_to_schema` function to handle customizations
    ```python
    def _apply_overrides_to_schema(model_id: str, schema_data: Dict[str, Any]) -> Dict[str, Any]:
         """Applies overrides from the YAML file to the schema data."""
         overrides = _load_override_config()
         model_override = overrides.get(model_id)

         if model_override:
             logger.info(f"Applying overrides for model {model_id}")
             # Example: Override 'required', 'properties', 'defaults'
             if "required" in model_override:
                 schema_data["required"] = model_override["required"]
             if "properties" in model_override:
                 # Could merge or replace properties based on needs
                 schema_data["properties"].update(model_override["properties"])
             # Store defaults separately if needed, or merge into properties
             if "defaults" in model_override:
                 schema_data["_defaults_override"] = model_override["defaults"]
             # Add more override logic as needed
         return schema_data
    ```

- [ ] 5.0 Integrate Schema Loading with Model Class
  - [x] 5.1 Modify `FalModel.__init__` to store model info
    ```python
    class FalModel(llm.KeyModel):
        # ... existing attributes ...
        input_schema: Optional[Dict[str, Any]] = None
        schema_load_attempted: bool = False

        def __init__(self, model_id: str, model_info: Optional[Dict[str, Any]] = None):
            # ... existing init ...
            self.model_info = model_info or {} # Ensure model_info is stored
            self.category = get_model_category(self.model_info or {"id": model_id})
            # Don't load schema here, do it lazily
    ```
  - [x] 5.2 Add schema loading capability to `FalModel`
  - [x] 5.3 Create `_ensure_schema_loaded` method for lazy loading
    ```python
    def _ensure_schema_loaded(self):
        if not self.schema_load_attempted:
            logger.debug(f"Attempting to load schema for {self.model_id}")
            self.input_schema = _get_processed_schema(self.model_id)
            self.schema_load_attempted = True
            if self.input_schema:
                logger.info(f"Successfully loaded processed schema for {self.model_id}")
            else:
                logger.warning(f"Failed to load schema for {self.model_id}. Will use fallback parameter handling.")
    ```
  - [x] 5.4 Update `execute` method to ensure schema is loaded before processing
    ```python
    def execute(self, prompt, stream, response, conversation, key):
        self._ensure_schema_loaded() # Load schema before proceeding
        # ... rest of execute method ...
    ```

- [x] 6.0 Refactor Request Data Building
  - [x] 6.1 Rewrite `_build_request_data` to use schema for parameter handling
    ```python
    def _build_request_data(self, prompt) -> Dict[str, Any]:
        """Build request data using schema, overrides, and fallbacks."""
        data = {}
        options = prompt.options

        # Ensure schema is loaded (it should be by execute, but double-check)
        self._ensure_schema_loaded()

        if self.input_schema:
            # --- Schema-Driven Parameter Building ---
            logger.debug(f"Building request data using schema for {self.model_id}")
            schema_props = self.input_schema.get("properties", {})
            schema_required = self.input_schema.get("required", [])
            schema_defaults = self.input_schema.get("_defaults_override", {}) # Get potential overrides

            # ... detailed parameter building logic ...

        else:
            # --- Fallback Parameter Building (Schema Failed) ---
            logger.warning(f"Building request data using FALLBACK logic for {self.model_id}")
            # Re-implement the *original* logic here
            # ... fallback logic ...

        logger.debug(f"Final request data for {self.model_id}: {data}")
        return data
    ```
  - [x] 6.2 Implement schema-driven parameter handling for prompt text
    ```python
    # 1. Handle Prompt Text
    # Determine target field (e.g., 'prompt', 'input') - needs heuristics or schema inspection
    prompt_field = "prompt" # Default assumption
    if "input" in schema_props and "prompt" not in schema_props:
         prompt_field = "input"
    # Add more specific checks if needed (e.g., based on category or model_id)
    if prompt.prompt is not None:
        data[prompt_field] = prompt.prompt
    elif prompt_field in schema_required:
        # This case should ideally be caught later by required field check
        logger.warning(f"Required field '{prompt_field}' is missing prompt text.")
    ```
  - [x] 6.3 Implement schema-driven parameter handling for attachments
    ```python
    # 2. Handle Attachments
    if prompt.attachments:
        # Determine target field (e.g., 'image_url', 'audio_url')
        attachment_field = None
        if "image_url" in schema_props: attachment_field = "image_url"
        elif "audio_url" in schema_props: attachment_field = "audio_url"
        # Add more specific checks if needed

        if attachment_field:
            # (Use your existing attachment upload logic here)
            # ... upload logic ...
            # Assuming upload_url is the result:
            # data[attachment_field] = upload_url
            pass # Placeholder for existing logic
        elif attachment_field in schema_required:
             logger.warning(f"Required attachment field '{attachment_field}' could not be populated.")
        else:
             logger.warning("Attachments provided but no matching schema field (e.g., image_url) found.")
    ```
  - [x] 6.4 Implement schema-driven parameter handling for model options
    ```python
    # 3. Handle Options (-o key value)
    provided_options = options.model_dump(exclude_unset=True) # Pydantic v2
    # For Pydantic v1: provided_options = options.dict(exclude_unset=True)

    handled_option_keys = set()

    # Handle common/aliased options first
    if 'seed' in provided_options and 'seed' in schema_props:
        data['seed'] = provided_options['seed']
        handled_option_keys.add('seed')
    if 'temperature' in provided_options and 'temperature' in schema_props:
        data['temperature'] = provided_options['temperature']
        handled_option_keys.add('temperature')
    # Add mappings like steps -> num_inference_steps if needed
    if 'steps' in provided_options:
        target_step_field = "num_inference_steps" # Example mapping
        if target_step_field in schema_props:
             data[target_step_field] = provided_options['steps']
             handled_option_keys.add('steps')
        elif 'steps' in schema_props: # If schema uses 'steps' directly
             data['steps'] = provided_options['steps']
             handled_option_keys.add('steps')

    # Handle remaining options based on schema properties
    for key, value in provided_options.items():
        if key not in handled_option_keys:
            if key in schema_props:
                # TODO: Add basic type coercion based on schema_props[key].get('type')
                data[key] = value
                handled_option_keys.add(key)
            else:
                logger.warning(f"Option '{key}' not found in schema for {self.model_id}. Ignoring (unless pass-through enabled).")
                # If you keep FalOptions with extra='allow', you could add it here as fallback
    ```
  - [x] 6.5 Apply defaults from schema and overrides
    ```python
    # 4. Apply Defaults from Schema/Overrides
    for key, prop_details in schema_props.items():
        if key not in data: # Only apply if not provided by user
            default_value = schema_defaults.get(key, prop_details.get("default"))
            if default_value is not None:
                data[key] = default_value
                logger.debug(f"Applied default value for '{key}': {default_value}")

    # 5. Final Check for Required Fields (Optional but Recommended)
    missing_required = [req for req in schema_required if req not in data]
    if missing_required:
        # Decide whether to raise error or just warn
        logger.error(f"Missing required parameters for {self.model_id}: {missing_required}. Request might fail.")
        # raise ValueError(f"Missing required parameters: {missing_required}")
    ```
  - [x] 6.6 Implement fallback logic when schema is unavailable
    ```python
    # --- Fallback Parameter Building (Schema Failed) ---
    logger.warning(f"Building request data using FALLBACK logic for {self.model_id}")
    # Re-implement the *original* logic here:
    # - Handle prompt based on category (e.g., 'input' for TTS)
    # - Handle attachments based on category
    # - Handle explicit FalOptions fields (width, height, steps, voice etc.) based on category
    # - Implement arbitrary pass-through for any remaining -o options
    # Example (incomplete):
    if "playai/tts" in self.fal_model_id.lower():
         if prompt.prompt is not None: data["input"] = prompt.prompt
         if options.voice is not None: data["voice"] = options.voice # Use original FalOptions field
         # ... etc ...
    else:
         if prompt.prompt is not None: data["prompt"] = prompt.prompt

    if self.category == "image":
         if options.width is not None: data["width"] = options.width
         # ... etc for height, steps, prompt_strength ...

    # Add arbitrary pass-through logic here if needed for fallback
    ```

- [x] 7.0 Enhance CLI Commands
  - [x] 7.1 Update `list_models_command` to add `--schema` option for detailed schema information
    ```python
    @fal_command_group.command(name="models")
    @click.option("--schema", metavar="MODEL_ID", help="Display input schema for a specific model ID.")
    def list_models_command(schema):
        """List available fal.ai models or display schema for one."""
        if schema:
            # Display schema for the specified model ID
            model_id = schema
            click.echo(f"Fetching schema for model: {model_id}")
            processed_schema = _get_processed_schema(model_id) # Fetch the schema
            if processed_schema:
                click.echo(f"\nInput Schema for {model_id}:")
                # Format and print the schema details nicely
                props = processed_schema.get("properties", {})
                required = processed_schema.get("required", [])
                defaults = processed_schema.get("_defaults_override", {}) # Check overrides first

                click.echo("\nRequired Parameters:")
                for req in required:
                    prop_info = props.get(req, {})
                    desc = prop_info.get('description', 'No description')
                    p_type = prop_info.get('type', 'any')
                    click.echo(f"  - {req} ({p_type}): {desc}")

                click.echo("\nOptional Parameters:")
                for key, prop_info in props.items():
                    if key not in required:
                         desc = prop_info.get('description', 'No description')
                         p_type = prop_info.get('type', 'any')
                         default_val = defaults.get(key, prop_info.get('default'))
                         default_str = f" (default: {default_val})" if default_val is not None else ""
                         click.echo(f"  - {key} ({p_type}): {desc}{default_str}")
                click.echo("") # Newline at end
            else:
                click.echo(f"Could not retrieve or process schema for {model_id}.", err=True)
        else:
            # List all models (existing logic, but using dynamic fetch)
            models_by_category = get_models_by_category() # Uses dynamic fetch now
            # ... (rest of your existing model listing loop) ...
    ```
  - [x] 7.2 Create schema display formatting logic for CLI output
  - [x] 7.3 Add `clear-cache` command for maintenance
    ```python
    import shutil # Add import

    @fal_command_group.command(name="clear-cache")
    def clear_cache_command():
        """Clear cached Fal.ai model lists and schemas."""
        global _model_list_cache
        cleared_schemas = False
        cleared_list = False

        # Clear schema cache directory
        if FAL_SCHEMA_CACHE_DIR.exists():
            try:
                shutil.rmtree(FAL_SCHEMA_CACHE_DIR)
                click.echo(f"Cleared schema cache: {FAL_SCHEMA_CACHE_DIR}")
                cleared_schemas = True
            except Exception as e:
                click.echo(f"Error clearing schema cache {FAL_SCHEMA_CACHE_DIR}: {e}", err=True)
        else:
            click.echo("Schema cache directory not found.")

        # Clear in-memory model list cache
        if _model_list_cache is not None:
            _model_list_cache = None
            click.echo("Cleared in-memory model list cache.")
            cleared_list = True

        if not cleared_schemas and not cleared_list:
             click.echo("No caches found to clear.")
        elif cleared_schemas or cleared_list:
             click.echo("Cache clearing complete.")
    ```
  - [x] 7.4 Implement cache clearing functionality for both model list and schema caches

### Relevant Files

- `llm_fal.py` - Main plugin file updated with:
  - Dynamic model discovery from Fal.ai API
  - New API constants and caching mechanisms
  - Refactored functions: `get_all_models`, `get_models_by_category`, `search_models`, `register_models`
- `pyproject.toml` - Updated with new dependencies (requests and PyYAML)
- `~/.llm/cache/fal-schemas/` - Cache directory for schema files (automatically created)
- `~/.llm/fal-overrides.yaml` - Override configuration file for user customizations of model schemas