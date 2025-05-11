## PLAN: Refactor `llm_fal.py` to several files

## Tasks

- [ ] 1.0 Create Package Structure and Migrate Core Infrastructure (Using `src/` Layout)
    - [ ] 1.1 Create the `src/` directory in the project root (`llm-fal/`).
    - [ ] 1.2 Create the `src/llm_fal/` directory inside `src/`.
    - [ ] 1.3 Move the existing `llm_fal.py` file into a temporary location (e.g., project root) and rename it (e.g., `old_llm_fal.py`) for reference during migration.
    - [ ] 1.4 Create the file `src/llm_fal/__init__.py`.
    - [ ] 1.5 Create the file `src/llm_fal/constants.py`.
    - [ ] 1.6 Create the file `src/llm_fal/utils.py`.
    - [ ] 1.7 Populate `src/llm_fal/constants.py` by moving all constant definitions (e.g., `PROVIDER_NAME`, `KEY_ENV_VAR`, API URLs, cache paths, `MODEL_CATEGORIES`) from `old_llm_fal.py`.
    - [ ] 1.8 Populate `src/llm_fal/utils.py` by moving utility functions (e.g., `get_api_key`, `_get_example_value`) from `old_llm_fal.py`.
    - [ ] 1.9 Set up the basic hook implementations (e.g., `register_models`, `register_commands`, `process_response`) in `src/llm_fal/__init__.py`, importing necessary components as placeholders for now.
    - [ ] 1.10 Update `pyproject.toml` to specify the `src` layout. Add or modify the build tool configuration (e.g., for `setuptools`):
        ```toml
        [tool.setuptools]
        package-dir = {"" = "src"}
        # Ensure packages = ["llm_fal"] is also present or use find:
        # packages = find:{where=["src"]}
        ```
        *(Adjust based on the specific build backend being used, e.g., `hatchling`)*.
    - [ ] 1.11 Ensure `requests`, `PyYAML`, and `fal_client` are listed as dependencies in `pyproject.toml`.

- [ ] 2.0 Migrate Core Data Handling Logic (Models & Schemas)
    - [ ] 2.1 Create the file `src/llm_fal/models.py`.
    - [ ] 2.2 Move model discovery and management functions (`_fetch_all_models_from_api`, `get_all_models`, `get_model_category`, `get_models_by_category`, `search_models`) from `old_llm_fal.py` to `src/llm_fal/models.py`.
    - [ ] 2.3 Move the `_model_list_cache` variable to be a module-level variable within `src/llm_fal/models.py`.
    - [ ] 2.4 Create the file `src/llm_fal/schemas.py`.
    - [ ] 2.5 Move schema management functions (`_load_override_config`, `_is_schema_cache_valid`, `_invalidate_schema_cache`, `_get_schema_cache_path`, `_load_schema_from_cache`, `_save_schema_to_cache`, `_clear_schema_cache`, `_get_processed_schema`, `_apply_overrides_to_schema`) from `old_llm_fal.py` to `src/llm_fal/schemas.py`.
    - [ ] 2.6 Move the `_override_config_cache` variable to be a module-level variable within `src/llm_fal/schemas.py`.
    - [ ] 2.7 Update import statements within `src/llm_fal/models.py` and `src/llm_fal/schemas.py` to use relative imports from `.constants` and `.utils`.
    - [ ] 2.8 Update the `register_models` hook implementation in `src/llm_fal/__init__.py` to correctly import `get_all_models` from `.models`.

- [ ] 3.0 Refactor `FalModel` and Extract Specialized Logic (Request/Response)
    - [ ] 3.1 Create the file `src/llm_fal/fal_model.py`.
    - [ ] 3.2 Move the `FalOptions` and `FalModel` class definitions from `old_llm_fal.py` to `src/llm_fal/fal_model.py`.
    - [ ] 3.3 Ensure `FalModel.__init__`, `FalModel.execute`, and `FalModel._ensure_schema_loaded` remain within the class structure.
    - [ ] 3.4 Create the file `src/llm_fal/request_builder.py`.
    - [ ] 3.5 Move the logic from `FalModel._build_request_data`, `_handle_attachments_with_schema`, `_handle_attachments_without_schema`, `_get_attachment_content`, and `_upload_attachment` into `src/llm_fal/request_builder.py` as standalone functions (e.g., `build_request_data(model_instance, prompt)`, `upload_attachment(...)`). Adjust function signatures to accept necessary context.
    - [ ] 3.6 Create the file `src/llm_fal/response_processor.py`.
    - [ ] 3.7 Move the logic from `FalModel._stream_response` and `FalModel._process_response` into `src/llm_fal/response_processor.py` as standalone functions (e.g., `stream_response(model_id, data, category)`, `process_api_result(result, category)`).
    - [ ] 3.8 Create the standalone `process_response` hook implementation function within `src/llm_fal/response_processor.py` (refactoring the logic previously in the hook in `old_llm_fal.py`).
    - [ ] 3.9 Update `FalModel.execute` to call the refactored functions from `request_builder` and `response_processor`.
    - [ ] 3.10 Update `FalModel._ensure_schema_loaded` to import and call `_get_processed_schema` from `.schemas`.
    - [ ] 3.11 Update import statements within `src/llm_fal/fal_model.py`, `src/llm_fal/request_builder.py`, and `src/llm_fal/response_processor.py` to use relative imports (`.constants`, `.utils`, `.schemas`, etc.) where appropriate.
    - [ ] 3.12 Update the `register_models` hook in `src/llm_fal/__init__.py` to import `FalModel` from `.fal_model`.
    - [ ] 3.13 Update the `process_response` hook in `src/llm_fal/__init__.py` to import and call the implementation from `.response_processor`.

- [ ] 4.0 Migrate CLI Commands and Finalize Implementation
    - [ ] 4.1 Create the file `src/llm_fal/cli_commands.py`.
    - [ ] 4.2 Move the Click command group definition (`fal_command_group`) and individual command functions (`auth_command`, `clear_cache_command`, `list_models_command`) from `old_llm_fal.py` to `src/llm_fal/cli_commands.py`.
    - [ ] 4.3 Move cache clearing helper functions (`_clear_model_list_cache`, `_clear_all_caches`) from `old_llm_fal.py` to `src/llm_fal/cli_commands.py` (or potentially `.utils` if deemed more general).
    - [ ] 4.4 Ensure `clear_cache_command` correctly imports and calls necessary cache management functions from `.models` (`_clear_model_list_cache`) and `.schemas` (`_clear_schema_cache`).
    - [ ] 4.5 Update import statements within `src/llm_fal/cli_commands.py` to use relative imports (`.models`, `.schemas`, `.utils`, `.constants`).
    - [ ] 4.6 Update the `register_commands` hook in `src/llm_fal/__init__.py` to import `fal_command_group` from `.cli_commands` and add it to the `cli` object.
    - [ ] 4.7 Perform a final review of all import statements across all files in the `src/llm_fal/` package to ensure correctness and resolve any circular dependencies.
    - [ ] 4.8 Delete the temporary `old_llm_fal.py` file from the project root.
    - [ ] 4.9 Update test files (`tests/test_fal.py`, `tests/test_models.py`) to use the new import paths (e.g., `from llm_fal.models import get_all_models`). Note: The import path remains `llm_fal` because that's the *installed package name*, regardless of the `src` layout in the source tree.
    - [ ] 4.10 Run `pytest` and ensure all tests pass with the new structure.
    - [ ] 4.11 Perform manual testing of core CLI functionality: `llm plugins`, `llm fal models`, `llm fal models --schema <model_id>`, `llm fal auth`, `llm fal clear-cache`, and running a prompt with a fal model (`llm -m fal-ai/...`).

### Relevant Files

- `src/llm_fal/__init__.py` - Main plugin entry point, registers hooks with LLM CLI.
- `src/llm_fal/constants.py` - Stores all shared constants (API URLs, cache paths, categories).
- `src/llm_fal/utils.py` - Contains general utility functions (API key retrieval, example value generation).
- `src/llm_fal/models.py` - Handles fetching, caching, searching, and categorizing Fal.ai models from the API.
- `src/llm_fal/schemas.py` - Manages fetching, caching, validation, overriding, and processing of model input schemas.
- `src/llm_fal/fal_model.py` - Defines the core `FalModel` class (including `FalOptions`) and its main execution flow.
- `src/llm_fal/request_builder.py` - Contains standalone functions for constructing the API request payload, including attachment handling.
- `src/llm_fal/response_processor.py` - Contains standalone functions for processing synchronous and streaming API responses, and the `process_response` hook logic.
- `src/llm_fal/cli_commands.py` - Defines the `llm fal ...` subcommands using Click.
- `pyproject.toml` - Project build configuration; needs updates for the `src` layout (e.g., `package-dir = {"" = "src"}`).
- `tests/test_fal.py` - Core functional tests; import paths likely remain `from llm_fal...`.
- `tests/test_models.py` - Model/schema related tests; import paths likely remain `from llm_fal...`.