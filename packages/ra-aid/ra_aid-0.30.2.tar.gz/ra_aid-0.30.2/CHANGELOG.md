## [0.30.2] - 2025-05-06

- Handle list response from LLM API

## [0.30.1] - 2025-05-06

- Switch to CIAYN backend for `gemini-2.5-pro-preview-05-06`

## [0.30.0] - 2025-05-06

### Added
- **Agent Thread Management:** Introduced a new system (`ra_aid/utils/agent_thread_manager.py`) for managing the lifecycle of agent threads, allowing for better control and monitoring of running agents. Includes functions to register, unregister, stop, and check the status of agent threads.
- **Session Deletion API:** Added a `DELETE /v1/session/{session_id}` endpoint to allow for stopping an active agent session and marking it as "halting" (`ra_aid/server/api_v1_sessions.py`).
- **Session ID in Agent Creation:** The `create_agent` function and its callers now utilize a `session_id` for improved agent tracking and context management (`ra_aid/agent_utils.py`, `ra_aid/agents/research_agent.py`, `ra_aid/server/api_v1_spawn_agent.py`).
- **User Query Trajectory in UI:** Added a new `UserQueryTrajectory.tsx` component to display the initial user query in the frontend timeline.
- **Copy to Clipboard Button in UI:** Implemented a `CopyToClipboardButton.tsx` component and integrated it into various UI parts (e.g., `MarkdownCodeBlock.tsx`, Task and Expert Response trajectories) for easy content copying.
- **Persistent CLI Configuration:** Users can now set and persist default LLM provider and model via CLI (`--set-default-provider`, `--set-default-model`), stored in `config.json` in the `.ra-aid` directory (`ra_aid/config.py`).
- **Tests for Agent Thread Manager:** Added new unit tests for the agent thread management module (`tests/ra_aid/utils/test_agent_thread_manager.py`).
- **Tests for Session Deletion API:** Added new tests for the session deletion API endpoint (`tests/ra_aid/server/test_api_v1_sessions.py`).

### Changed
- **Default Gemini Model:** Updated the default Google Gemini model to `gemini-2.5-pro-preview-05-06` (from `gemini-2.5-pro-preview-03-25`) in `ra_aid/__main__.py`, `ra_aid/models_params.py`, `docs/docs/quickstart/recommended.md`, and related tests.
- **Async Tool Wrapper Optimization:** Refined the creation of synchronous wrappers for asynchronous tools to only pass necessary (non-default or required) arguments to the underlying coroutine, improving efficiency (`ra_aid/tool_configs.py`).
- **Agent Creation Tests:** Updated tests for `create_agent` to reflect the new `session_id` parameter (`tests/ra_aid/test_agent_utils.py`).
- **Session Statuses:** The `Session` model now includes 'halting' and 'halted' statuses to support the new session termination API.
- **User Query Storage:** The initial `user_query` is now stored with session and trajectory data.
- **`DEFAULT_SHOW_COST`:** Changed to `True` by default.

### Fixed
- **Tool Name Sanitization:** Corrected an issue where tool names with special characters (`.` or `-`) could cause errors during the creation of synchronous wrappers for async tools. These characters are now consistently replaced with `_` (`ra_aid/tool_configs.py`).
- **Token Limiter Model Name Handling:** Improved `get_model_token_limit` in `ra_aid/anthropic_token_limiter.py` to better handle model name variations for token limit lookups.

## [0.29.0] 2025-04-24

### Changed
- **Frontend Port Configuration:**
    - Frontend development server port is now configurable via `VITE_FRONTEND_PORT` environment variable (defaults to 5173) (`frontend/web/vite.config.js`).
    - Frontend now dynamically determines the backend port using `VITE_BACKEND_PORT` in dev (default 1818) and `window.location.port` in production (`frontend/common/src/store/clientConfigStore.ts`).
- **Expert Model Temperature Handling:** The backend (`ra_aid/llm.py`) now checks if an expert model supports the `temperature` parameter before passing it, preventing errors with models like newer OpenAI versions that don't. It continues to set `reasoning_effort` to `"high"` where supported.
- **OpenAI Model Definitions:** Updated definitions for `o4-mini` and `o3` in `ra_aid/models_params.py` to set `supports_temperature=False` and `supports_reasoning_effort=True`.

### Added
- **Frontend Development Documentation:** Added instructions to `docs/docs/contributing.md` on running the frontend dev server and configuring ports using environment variables.
- **New OpenAI Model Definitions:** Added definitions for `o4-mini-2025-04-16`, `o3-2025-04-16`, and `o3-mini-2025-01-31` to `ra_aid/models_params.py`.

### Fixed
- **Custom Tool Result Handling:** Ensured results from custom tools are always wrapped in a Langchain `BaseMessage` (`AIMessage`) to maintain consistency (`ra_aid/agent_backends/ciayn_agent.py`).
- **Custom Tool Console Output:** Corrected minor formatting issues (escaped newlines) in the console output message when executing custom tools (`ra_aid/agent_backends/ciayn_agent.py`).


## [0.28.1] 2025-04-17

- Update web prebuilt assets

## [0.28.0] 2025-04-17

### Documentation
- Updated expert model API key environment variables (`EXPERT_GEMINI_API_KEY`, `EXPERT_DEEPSEEK_API_KEY`) and clarified selection priority in `docs/docs/configuration/expert-model.md`.
- Updated recommendation to Google Gemini 1.5 Pro as the primary default model in `docs/docs/intro.md` & `docs/docs/quickstart/recommended.md`, explaining automatic detection via `GEMINI_API_KEY`.

### Frontend
- Improved autoscroll logic in `frontend/common/src/components/DefaultAgentScreen.tsx`.
- Added new trajectory visualization components for file modifications: `FileStrReplaceTrajectory.tsx` and `FileWriteTrajectory.tsx` in `frontend/common/src/components/trajectories/`.
- Integrated new trajectory components into `frontend/common/src/components/TrajectoryPanel.tsx` and `frontend/common/src/components/trajectories/index.ts`.

### Backend Core & Configuration
- Refined expert model provider selection logic in `ra_aid/__main__.py` with updated priority order based on API keys.
- Minor cleanup in `ra_aid/agent_backends/ciayn_agent.py` (removed unused import, refined fallback warning).
- Set default backend for `o4-mini` to `CIAYN` in `ra_aid/models_params.py`.

### Tools & Prompts
- Added `file_str_replace` tool (`ra_aid/tools/file_str_replace.py`) for replacing strings in files.
- Replaced `write_file_tool` with `put_complete_file_contents` tool (`ra_aid/tools/write_file.py`) for writing complete file content.
- Updated `read_file_tool` (`ra_aid/tools/read_file.py`) to strip whitespace from filepaths.
- Added `file_str_replace` and `put_complete_file_contents` to tool configurations and removed old `write_file_tool` (`ra_aid/tool_configs.py`).
- Removed `ripgrep_search` tool from default CIAYN tools (use `run_shell_command` instead) (`ra_aid/tool_configs.py`).
- Updated core agent prompts (Research, Planning, Implementation) to emphasize using `rg` via `run_shell_command`, mandate `emit_research_notes`, and refine instructions (`ra_aid/prompts/`).

### Testing
- Added tests for fallback warning logic in `tests/ra_aid/agent_backends/test_ciayn_fallback_warning.py`.
- Updated tests for `put_complete_file_contents` tool in `tests/ra_aid/tools/test_write_file.py`.

## [0.27.0] 2025-04-16

### Added
- Support for `o4-mini` and `o3` models

### Changed
- **Default Model/Provider Logic (`ra_aid/__main__.py`):**
    - Changed the default OpenAI model from `gpt-4o` to `o4-mini`.
    - Updated the default LLM provider selection priority based on available API keys to: Gemini (`GEMINI_API_KEY`), then OpenAI (`OPENAI_API_KEY`), then Anthropic (`ANTHROPIC_API_KEY`).
- **Expert Model Selection Logic (`ra_aid/__main__.py`, `ra_aid/llm.py`):**
    - Introduced dedicated environment variables for expert model API keys (e.g., `EXPERT_OPENAI_API_KEY`, `EXPERT_ANTHROPIC_API_KEY`).
    - Updated the priority order for selecting the *expert* provider when none is explicitly set: `EXPERT_OPENAI_API_KEY` > `GEMINI_API_KEY` > `EXPERT_ANTHROPIC_API_KEY` > `DEEPSEEK_API_KEY`.
    - Refined fallback logic: If no specific expert key is found, it uses the main provider configuration. A special case ensures that if the main provider is OpenAI and no expert model is specified, the expert model defaults to auto-selection (prioritizing `o3`).
    - Updated the default OpenAI *expert* model selection to prioritize only `"o3"`. An error is now raised if `"o3"` is unavailable via the API key and no specific expert model was requested by the user.
- **Model Parameters (`ra_aid/models_params.py`):**
    - Added configuration parameters (token limits, capabilities) for the `o4-mini` and `o3` models.

### Testing (`tests/ra_aid/test_default_provider.py`, `tests/ra_aid/test_llm.py`)
- Added/updated tests to verify the new default provider logic, ensuring correct prioritization.
- Added/updated tests for expert model selection to reflect the new prioritization and the default selection of `o3` for OpenAI expert.

## [0.26.0] 2025-04-16

### Frontend
- Implement improved autoscroll logic with user scroll detection in `DefaultAgentScreen.tsx`.
- Add `Ctrl+Space` shortcut for new session and completion message in `DefaultAgentScreen.tsx`.
- Make session title header sticky in `DefaultAgentScreen.tsx`.
- Add `Ctrl+Enter` (submit) and `Ctrl+Shift+Enter` (research-only) shortcuts with visual key indicators in `InputSection.tsx`.
- Create new `EnterKeySvg.tsx` component for shortcut key visuals.
- Add `updateSessionDetails` action to `sessionStore.ts` for faster session name updates via WebSocket.

### Backend
- Add `--cowboy-mode` flag with server warning confirmation in `__main__.py`.
- Adjust console output padding in `console/formatting.py` and `console/output.py`.
- Refactor `research_notes_formatter.py` to return raw content.
- Add model parameters for `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano` in `models_params.py`.
- Update CIAYN agent prompts to mandate triple quotes for all string tool arguments in `prompts/ciayn_prompts.py`.
- Broadcast full session details immediately after creation via WebSocket in `server/api_v1_spawn_agent.py`.

### Build
- Update prebuilt frontend assets (`index-*.js`, `index-*.css`, `index.html`).

## [0.25.0] 2025-04-09

### Backend Changes
- Refactored `ra_aid/tools/ripgrep.py`:
  - Removed old search parameter string construction.
  - Introduced new variables: `final_output`, `final_return_code`, `final_success` for capturing command-line output and error handling.
  - Updated trajectory recording logic using consolidated parameters (`tool_parameters` and `step_data`).
  - Enhanced UTF-8 decoding with error replacement and improved error panel displays.
- Updated backend modules:
  - Modified `ra_aid/project_info.py` and `ra_aid/server/api_v1_spawn_agent.py` for improved logging, error handling, and user feedback.
  - Updated server-side prebuilt assets (JavaScript, CSS, and `index.html`) for better asset management.

### Frontend Changes
- Updated several UI components in `frontend/common` including:
  - `DefaultAgentScreen.tsx`, `SessionList.tsx`, `SessionSidebar.tsx`, `TimelineStep.tsx`, and `TrajectoryPanel.tsx`.
- Adjusted state management and utility/store files to support updated UI displays for agent outputs, sessions, and trajectories.

### Configuration & Minor Changes
- Modified configuration files:
  - Updated `.gitignore` and `.ra-prompt` with newer patterns.
  - Revised `frontend/common/package.json` and `frontend/common/tailwind.preset.js` for improved dependency and styling management.
  - Updated `package-lock.json` files and server-side asset references.

## [0.24.0] 2025-04-08

### Added
- Web UI is now available at localhost:1818 when ra-aid is started with `--server`
- Session status tracking (pending, running, completed, failed) in the database and API.
- Robust WebSocket connection handling in the frontend with auto-reconnect and heartbeats (`frontend/common/src/websocket/connection.ts`).
- Serve prebuilt web UI static files directly from the backend server (`ra_aid/server/server.py`, `ra_aid/server/prebuilt/`).
- `broadcast_sender.py` module for decoupled WebSocket message broadcasting via a queue (`ra_aid/server/broadcast_sender.py`).
- `SessionNotFoundError` custom exception (`ra_aid/exceptions.py`).
- `build:prebuilt` npm script to build frontend assets into the backend distribution (`frontend/package.json`).

### Changed
- Refactored backend WebSocket broadcasting to use the new `broadcast_sender` queue, improving reliability and decoupling (`ra_aid/server/server.py`, `ra_aid/server/api_v1_spawn_agent.py`).
- Updated various frontend components and stores to integrate with the new WebSocket logic and session status (`frontend/common/`).
- Enhanced logging in `ra_aid/agents/research_agent.py` with thread IDs.

### Fixed
- Resolved WebSocket message serialization error for `session_update` payloads by ensuring proper JSON serialization (`mode='json'`) before queuing messages in the new broadcast sender mechanism (`ra_aid/server/api_v1_spawn_agent.py`, `ra_aid/server/broadcast_sender.py`).

### Build
- Added script (`frontend/package.json#build:prebuilt`) to build and copy frontend assets to `ra_aid/server/prebuilt/` for server distribution.

### Internal
- Added database migration for the new session `status` field (`ra_aid/migrations/015_20250408_140800_add_session_status.py`).
- Updated `.gitignore`.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.23.0] 2025-04-07

### Added
- Added configuration parameters for the `gemini-2.5-pro-preview-03-25` model (`ra_aid/models_params.py`).

### Changed
- Updated default provider logic in `ra_aid/__main__.py` to prioritize the Gemini provider (`gemini-2.5-pro-preview-03-25` model) if the `GEMINI_API_KEY` environment variable is set. The previous OpenAI/Anthropic logic serves as a fallback.
- Updated default *expert* provider logic in `ra_aid/__main__.py` to prioritize Gemini (`gemini-2.5-pro-preview-03-25` model) if `GEMINI_API_KEY` is set, before falling back to OpenAI or DeepSeek.

### Fixed
- Improved robustness of triple-quoted string handling in tool calls generated by the CIAYN agent, particularly for `put_complete_file_contents`, ensuring the fix is applied only when necessary (`ra_aid/agent_backends/ciayn_agent.py`).

## [0.22.0] 2025-04-03

### Added

- Support for Anthropic\'s `claude-3.7` series models (`ra_aid/models_params.py`, `tests/ra_aid/test_anthropic_token_limiter.py`).
- Support for Fireworks AI provider and models (`fireworks/firefunction-v2`, `fireworks/dbrx-instruct`) (`ra_aid/models_params.py`, `ra_aid/llm.py`).
- Implicit think tag detection: `process_thinking_content` now checks for <think> tags even if `supports_think_tag` is not explicitly `True` in model config, provided it\'s not `False` and the content starts with the tag (`ra_aid/text/processing.py`, `tests/ra_aid/text/test_process_thinking.py`).
- Command-line arguments `--project-dir` and `--db-path` added to `ra-aid usage latest` and `ra-aid usage all` subcommands for specifying database location (`ra_aid/scripts/cli.py`, `ra_aid/scripts/all_sessions_usage.py`, `ra_aid/scripts/last_session_usage.py`).
- Reinitialization capability for Singleton classes via `_initialize` method (`ra_aid/utils/singleton.py`).
- Metadata tracking (`model_name`, `provider`) added during LLM initialization (`ra_aid/llm.py`, `tests/ra_aid/test_llm.py`).

### Changed

- **Refactored Callback Handling:** Replaced `AnthropicCallbackHandler` with a generalized `DefaultCallbackHandler` located in `ra_aid/callbacks/default_callback_handler.py`. This new handler supports multiple providers, improves cost/token tracking logic, standardizes initialization, enhances database interaction for trajectory logging, and provides better context management (`ra_aid/callbacks/default_callback_handler.py`, `ra_aid/agent_utils.py`, `ra_aid/console/output.py`, `tests/ra_aid/callbacks/test_default_callback_handler.py`, `tests/ra_aid/test_token_usage_tracking.py`).
- **Refactored Thinking Processing:** Significantly updated `process_thinking_content` in `ra_aid/text/processing.py` for clearer logic flow. It now explicitly handles structured thinking (list format) separately from string-based <think> tag extraction. The logic for tag extraction now depends on the `supports_think_tag` configuration value (True: always check, False: never check, None: check only if content starts with <think>) (`ra_aid/text/processing.py`, `tests/ra_aid/text/test_process_thinking.py`, `tests/ra_aid/agent_backends/test_ciayn_agent_think_tag.py`).
- **Refactored Token Limiting:** Renamed `sonnet_35_state_modifier` to `base_state_modifier` in `ra_aid/anthropic_token_limiter.py` for broader applicability and adjusted associated logic (`ra_aid/anthropic_token_limiter.py`, `ra_aid/agent_utils.py`, `tests/ra_aid/test_anthropic_token_limiter.py`).
- Updated LLM initialization (`initialize_llm` in `ra_aid/llm.py`) to include provider/model metadata and refine DeepSeek provider logic for different DeepSeek models (`ra_aid/llm.py`, `tests/ra_aid/test_llm.py`).
- Improved rate limit error handling and retry logic in `_handle_api_error` (`ra_aid/agent_utils.py`).
- Removed redundant console output from `ripgrep_search` tool; results are now only in the returned dictionary (`ra_aid/tools/ripgrep.py`).
- Updated numerous unit tests across the codebase to reflect the extensive refactoring in callbacks, thinking processing, token limiting, and LLM initialization.
- Updated project dependencies as recorded in `uv.lock` and `pyproject.toml`.

### Fixed

- Corrected an import path typo in `ra_aid/dependencies.py`.
- Ensured the correct callback handler instance (`DefaultCallbackHandler`) is used for fetching cost information for display (`ra_aid/console/output.py`).
- Addressed various test failures arising from the refactoring of core components.

### Removed

- Removed the dedicated `ra_aid/callbacks/anthropic_callback_handler.py` file. Its functionality has been merged and generalized into `ra_aid/callbacks/default_callback_handler.py`.

## [0.21.0] 2025-03-27

### Added
- Add `include_paths` argument to ripgrep tool (`881d4f0`).
- Add trajectory hooks (`3160dcd`).
- Add support for `--msg-file` argument to read task/message from a file (`a827742`).

### Changed
- Improve CIAYN agent\'s robust code handling (`ac5abb3`, `38340b2`).
- Optimize LLM-based tool call extraction for specific models (`67b268f`).
- Set max context for Fireworks models (`44cbe84`).
- Update model parameters for R1 on Fireworks (`328d49d`).
- Correct CIAYN capitalization (`d07ccc0`).
- Remove duplicate example for ra-aid command in documentation (`3d119e7`).
- Update README to clarify command line options for message and msg-file arguments (`a827742`).

### Fixed
- Fix tests (`ce5301d`, `feb9a11`).
- Fix ripgrep tool functionality (`4d28d68`).
- Add tests for `--msg-file` argument handling and exclusivity (`a827742`).

## [0.20.0] 2025-03-26

### Added
- Added `mark_research_complete_no_implementation_required` tool to prevent infinite research loops when no implementation is needed after research. (83b03bf)

### Changed
- Improved messaging around API rate limits to be less alarming. (9baee8c)
- Updated dependencies and optimized model parameters for Gemini. (4197822)
- Improved support for the `gemini-2.5-pro-exp-03-25` model. (110efc6)
- Updated model parameters. (83d2192)

### Fixed
- Fixed tool call validation logic, improving compatibility with models like `gemini-2.5-pro-exp-03-25`. (3e2d888)
- Prevent console logs from showing when `log_mode` is set to "file". (2ca0da2)
- Fixed a test related to the `mark_research_complete_no_implementation_required` tool. (065747b)

## [0.19.1] 2025-03-25

### Added
- Support for Fireworks.ai LLM provider with error handling
- Support for Groq provider
- Cloudflare build scripts and logging

### Changed
- Updated model parameters and providers configuration
- Multiple package-lock.json updates

### Fixed
- npm version specification in package.json

## [0.18.4] 2025-03-24

### Added
- Custom Tools Feature
  - Added support for custom tools with `--custom-tools <path>` CLI flag
  - Implemented MCP (Model-Completion-Protocol) client for integrating external tool providers
  - Created documentation on custom tools usage in `docs/docs/usage/custom-tools.md`
  - Added example code in `examples/custom-tools-mcp/` directory
- API Documentation
  - Added comprehensive OpenAPI documentation for REST API endpoints
  - Implemented API documentation in Docusaurus with new MDX files
  - Added YAML OpenAPI specification file `docs/ra-aid.openapi.yml`
  - Created script to generate OpenAPI documentation automatically
- Session Usage Statistics
  - Added CLI commands for retrieving usage statistics for all sessions and the latest session
  - Enhanced session and trajectory repositories with new methods
  - Moved scripts into proper Python package structure (`ra_aid/scripts/`)
- Web UI Improvements
  - Added new UI components including input box, session screen, and buttons
  - Improved session management UI
  - Enhanced styling and layout

### Changed
- WebSocket Endpoint Migration
  - Migrated WebSocket endpoint from `/ws` to `/v1/ws` to align with REST API endpoint pattern
  - Updated root HTML endpoint to reflect the new WebSocket path
- Project Maintenance
  - Refactored agent creation logic to use model capabilities for selecting agent type
  - Improved model detection and normalization
  - Updated dependencies via uv.lock
  - Fixed various typos and improved prompts

## [0.18.0] 2025-03-19

### Added
- Project State Directory Feature
  - Added `--project-state-dir` parameter to allow customization of where project data is stored
  - Modified database connection, logging, and memory wiping to support custom directories
  - Created comprehensive documentation in docs/docs/configuration/project-state.md
- Ollama Integration
  - Added support for running models locally via Ollama
  - Implemented configuration options including model selection and context window size
  - Added documentation for Ollama in docs/docs/configuration/ollama.md
  - Updated open-models.md to include Ollama as a supported provider
- Web UI and API Progress (partially implemented)
  - Created API endpoints for session management (create, list, retrieve)
  - Added trajectory tracking and visualization
  - Implemented UI components for session management
  - Added server infrastructure for web interface
- Token Usage and Cost Tracking
  - Enhanced trajectory tracking with token counting
  - Added session-level token usage and cost tracking
  - Improved cost calculation and logging

## [0.17.1] 2025-03-13

### Fixed
- Fixed bug with `process_thinking_content` function by moving it from `agent_utils` to `ra_aid.text.processing` module
- Fixed config parameter handling in research request functions
- Updated development setup instructions in README to use `pip install -e "[dev]"` instead of `pip install -r requirements-dev.txt`

## [0.17.0] 2025-03-12

### Added
- Added support for think tags in models with the new extract_think_tag function
- Enhanced CiaynAgent and expert tool to extract and display thinking content from <think>...</think> tags
- Added model parameters for think tag support
- Added comprehensive testing for think tag functionality
- Added `--show-thoughts` flag to show thoughts of thinking models
- Added `--show-cost` flag to display cost information during agent operations
- Enhanced cost tracking with AnthropicCallbackHandler for monitoring token usage and costs
- Added Session and Trajectory models to track application state and agent actions
- Added comprehensive environment inventory system for collecting and providing system information to agents
- Added repository implementations for Session and Trajectory models
- Added support for reasoning assistance in research phase
- Added new config parameters for managing cost display and reasoning assistance

### Changed
- Updated langchain/langgraph deps
- Improved trajectory tracking for better debugging and analysis
- Enhanced prompts throughout the system for better performance
- Improved token management with better handling of thinking tokens in Claude models
- Updated project information inclusion in prompts
- Reorganized agent code with better extraction of core functionality
- Refactored anthropic token limiting for better control over token usage

### Fixed
- Fixed binary file detection
- Fixed environment inventory sorting
- Fixed token limiter functionality
- Various test improvements and fixes

## [0.16.1] 2025-03-07

### Changed
- Replaced thread-local storage with contextvars in agent_context.py for better context isolation
- Improved React agent execution with LangGraph's interrupt mechanism
- Enhanced _run_agent_stream function to properly handle agent state and continuation

### Fixed
- Fixed tests to work with the new implementation

## [0.16.0] 2025-03-07

### Added
- Database-backed memory system with SQLite (.ra-aid/pk.db)
- Repository pattern for memory access (KeyFactRepository, KeySnippetRepository, ResearchNoteRepository)
- Memory garbage collection with configurable thresholds
- "--wipe-project-memory" flag to reset memory
- Memory statistics in status panel
- Propagation depth control for agent_should_exit
- Fixed string parameter for ripgrep tool
- Support for Claude 3.7 Sonnet thinking tokens in expert tool

### Changed
- Enhanced file logging with support for .ra-aid/logs/
- Improved CiaynAgent with better tool validation and execution
- Memory-related prompt improvements

### Fixed
- Various bug fixes in tool execution
- Test improvements for memory system

## [0.15.2] - 2025-02-27

### Added
- Added agent_should_exit context functionality with propagation to parent contexts
- Improved agent crash detection with non-propagating crash state
- Enhanced ripgrep tool with better context support
- Improved agent context inheritance
- Added comprehensive test coverage for exit and crash handling

## [0.15.1] - 2025-02-27

### Fixed
- Improved chat prompt to prevent endless loop behavior with sonnet 3.7.

## [0.15.0] - 2025-02-27

### Added
- Added database infrastructure with models, connections, and migrations
- Added agent context system for improved context management
- Added aider-free mode with command line option to disable aider-related functionality
- Added database-related dependencies

### Changed
- Improved file editing tools with enhanced functionality
- Enhanced agent implementation tools with modified return values and logic
- Improved agent tool prompts for better clarity and effectiveness
- Fixed langgraph prebuilt dependency

### Fixed
- Fixed project state detection logic with added tests

## [0.14.9] - 2025-02-25

### Added
- Added binary file detection and filtering to prevent binary files from being added to related files
- Added python-magic dependency for improved binary file detection
- Added support for "thinking" budget parameter for Claude 3.7 Sonnet

### Changed
- Updated dependencies:
  - langchain-anthropic from 0.3.7 to 0.3.8
  - langchain-google-genai from 2.0.10 to 2.0.11
- Improved shell command tool description to recommend keeping commands under 300 words
- Enhanced binary file filtering to include detailed reporting of skipped files
- Updated test assertions to be more flexible with parameter checking

## [0.14.8] - 2025-02-25

### Changed
- Improved programmer.py tool prompts for better clarity on related files visibility
- Enhanced programmer tool to remind users to call emit_related_files on any new files created
- Updated README.md to use media queries for showing different logos based on color scheme preference

## [0.14.7] - 2025-02-25

### Added
- Windows compatibility improvements
  - Add error handling for Windows-specific modules
  - Add Windows-specific tests for compatibility

### Changed
- Improve cross-platform support in interactive.py
- WebUI improvements
  - Improve message display
  - Add syntax highlighting
  - Add animations
- Expert tool prompt improvements

### Fixed
- WebUI improvements
  - Fix WebSocket communication
- Interactive command handling improvements
  - Fix interactive history capture
  - Fix command capture bugs
  - Multiple fixes for interactive command execution on both Linux and Windows
  - Enhance error handling for interactive processes

## [0.14.6] - 2025-02-25

### Added
- Added `--no-git` flag to aider commands to prevent git operations

### Changed
- Updated aider-chat dependency from 0.75 to 0.75.1
- Improved prompts for better tool effectiveness
- Enhanced emit_key_snippet documentation to focus on upcoming work relevance

## [0.14.5] - 2025-02-24

### Changed
- Optimized prompts

## [0.14.4] - 2025-02-24

### Changed
- Updated aider-chat dependency from 0.74.2 to 0.75
- Improved tool calling performance by minimizing tool return values
- Replaced emit_key_snippets with emit_key_snippet for simpler code snippet management
- Simplified return values for multiple tools to improve tool calling accuracy
- Updated tool prompts to remove unnecessary context cleanup references
- Reorganized order of tools in read-only tools list

### Fixed
- Fixed tests to align with updated tool return values
- Updated test assertions to match new simplified tool outputs

## [0.14.3] - 2025-02-24

### Added
- Added support for Claude 3.7 Sonnet model
- Added version display in startup configuration panel

### Changed
- Updated language library dependencies (langgraph, langchain-core, langchain, langchain-openai, langchain-google-genai)
- Changed default Anthropic model from Claude 3.5 Sonnet to Claude 3.7 Sonnet

### Fixed
- Fixed f-string syntax error in write_file.py
- Fixed bug where model selection on Anthropic was always using default instead of respecting user selection
- Fixed Anthropic key error message to reference the correct variable
- Added test for user-specified Anthropic model selection

## [0.14.2] - 2025-02-19

### Added
- Added automatic fallback mechanism to alternative LLM models on consecutive failures
- Added FallbackHandler class to manage tool failures and fallback logic
- Added console notification for tool fallback activation
- Added detailed fallback configuration options in command line arguments
- Added validation for required environment variables for LLM providers

### Changed
- Enhanced CiaynAgent to handle chat history and improve context management
- Improved error handling and logging in fallback mechanism
- Streamlined fallback model selection and invocation process
- Refactored agent stream handling for better clarity
- Reduced maximum tool failures from 3 to 2

### Fixed
- Fixed tool execution error handling and retry logic
- Enhanced error resilience and user experience with fallback handler
- Improved error message formatting and logging
- Updated error handling to include base message for better debugging

## [0.14.1] - 2025-02-13

### Added
- Added expected_runtime_seconds parameter for shell commands with graceful process shutdown
- Added config printing at startup (#88)

### Changed
- Enforce byte limit in interactive commands
- Normalize/dedupe related file paths
- Relax aider version requirement for SWE-bench compatibility
- Upgrade langchain/langgraph dependencies

### Fixed
- Fixed aider flags (#89)
- Fixed write_file_tool references

## [0.14.0] - 2025-02-12

### Added
- Status panel showing tool/LLM status and outputs
- Automatic detection of OpenAI expert models
- Timeouts on LLM clients

### Changed
- Improved interactive TTY process capture and history handling
- Upgraded langgraph dependencies
- Improved prompts and work logging
- Refined token/bytes ratio handling
- Support default temperature on per-model basis
- Reduced tool count for more reliable tool calling
- Updated logo and branding assets
- Set environment variables to disable common interactive modes

### Fixed
- Various test fixes
- Bug fixes for completion message handling and file content operations
- Interactive command input improvements
- Use reasoning_effort=high for OpenAI expert models
- Do not default to o1 model (#82)
- Make current working directory and date available to more agents
- Fixed o1 reference (#82)

## [0.13.2] - 2025-02-02

- Fix temperature parameter error for expert tool.

## [0.13.1] - 2025-01-31

### Added
- WebUI (#61)
- Support o3-mini

### Changed
- Convert list input to string to handle create-react-agent tool calls correctly (#66)
- Add commands for code checking and fixing using ruff (#63)

### Fixed
- Fix token estimation
- Fix tests
- Prevent duplicate files (#64)
- Ensure default temperature is set correctly for different providers
- Do not incorrectly give temp parameter to expert model
- Correcting URLs that were referencing ai-christianson/ra-aid - should be ai-christianson/RA.Aid (#69)

### Improved
- Integrate litellm to retrieve model token limits for better flexibility (#51)
- Handle user defined test cmd (#59)
- Run tests during Github CICD (#58)
- Refactor models_tokens to be models_params so we can track multiple parameters on a per-model basis.

## [0.13.0] - 2025-01-22

### Added
- Added Deepseek Provider Support and Custom Deepseek Reasoner Chat Model (#50)
- Added Aider config File Argument Support (#43)
- Added configurable --recursion-limit argument (#46)
- Set Default Max Token Limit with Provider/Model Dictionary (#45)

### Changed
- Updated aider-chat version from 0.69.1 to 0.72.1 (#47)

### Fixed
- Fixed Issue 42 related to Levenshtein (#44)

### Improved
- Various prompt improvements
- Better handling of 429 errors on openrouter
- Improved project info handling and token usage optimization
- Extracted tool reflection functionality
- Improved work log handling
- Added tests for CiaynAgent._does_not_conform_to_pattern

## [0.12.1] - 2025-01-08
- Fix bug where directories are added as related files.

## [0.12.0] - 2025-01-04

### Added
- Google Gemini AI provider support
- Dependency check functionality in ra_aid/dependencies.py
- Test coverage reporting to pytest commands

### Changed
- Updated minimum Python requirement to 3.9
- Updated OpenAI model defaults
- Modified test files to support new Gemini provider
- Updated SWE-bench dataset generation script with UV package management

### Fixed
- Date-based assertions in directory listing tests

## [0.11.3] - 2024-12-30

- MacOS fixes.

## [0.11.2] - 2024-12-30

- Fix SyntaxError: f-string expression part cannot include a backslash.

## [0.11.1] - 2024-12-29

- Improve prompts.
- Fix issue #24.

## [0.11.0] - 2024-12-28

- Add CiaynAgent to support models that do not have, or are not good at, agentic function calling.
- Improve env var validation.
- Add --temperature CLI parameter.

## [0.10.3] - 2024-12-27

- Fix logging on interrupt.
- Fix web research prompt.
- Simplify planning stage by executing tasks directly.
- Make research notes available to more agents/tools.

## [0.10.2] - 2024-12-26

- Add logging.
- Fix bug where anthropic is used in chat mode even if another provider is specified.

## [0.10.0] - 2024-12-24

- Added new web research agent.

## [0.9.1] - 2024-12-23

- Fix ask human multiline continuation.

## [0.9.0] - 2024-12-23

- Improve agent interruption UX by allowing user to specify feedback or exit the program entirely.
- Do not put file ID in file paths when reading for expert context.
- Agents log work internally, improving context information.
- Clear task list when plan is completed.

## [0.8.2] - 2024-12-23

- Optimize first prompt in chat mode to avoid unnecessary LLM call.

## [0.8.1] - 2024-12-22

- Improved prompts.

## [0.8.0] - 2024-12-22

- Chat mode.
- Allow agents to be interrupted.

## [0.7.1] - 2024-12-20

- Fix model parameters.

## [0.7.0] - 2024-12-20

- Make delete_tasks tool available to planning agent.
- Get rid of implementation args as they are not used.
- Improve ripgrep tool status output.
- Added ask_human tool to allow human operator to answer questions asked by the agent.
- Handle keyboard interrupt (ctrl-c.)
- Disable PAGERs for shell commands so agent can work autonomously.
- Reduce model temperatures to 0.
- Update dependencies.

## [0.6.4] - 2024-12-19

- Added monorepo_detected, existing_project_detected, and ui_detected tools so the agent can take specific actions.
- Prompt improvements for real-world projects.
- Fix env var fallback when base key is given, expert and base provider are different, and expert key is missing.

## [0.6.3] - 2024-12-18

- Fix one shot completion signaling.
- Clean up error outputs.
- Update prompt for better performance on large/monorepo projects.
- Update programmer prompt so we don\'t use it to delete files.

## [0.6.2] - 2024-12-18
- Allow shell commands to be run in read-only mode.
- When asking for shell command approval, allow cowboy mode to be enabled.
- Update prompt to suggest commands be run in non-interactive mode if possible, e.g. using --no-pager git flag.
- Show tool errors in a panel.

## [0.6.1] - 2024-12-17

### Added
- When key snippets are emitted, snippet files are auto added to related files.
- Add base task to research subtask prompt.
- Adjust research prompt to make sure related files are related to the base task, not just the research subtask.
- Track tasks by ID and allow them to be deleted.
- Make one_shot_completed tool available to research agent.
- Make sure file modification tools are not available when research only flag is used.
- Temporarily disable write file/str replace as they do not work as well as just using the programmer tool.

## [0.6.0] - 2024-12-17

### Added
- New `file_str_replace` tool for performing exact string replacements in files with unique match validation
- New `write_file_tool` for writing content to files with rich output formatting and comprehensive error handling
