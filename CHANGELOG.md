# Changelog

All notable changes to LibreThinker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Direct Model Access**: Connect to local AI models via Ollama, LM Studio, or any OpenAI-compatible server
- New "Direct model access" checkbox in sidebar to toggle between local and cloud models
- Configuration fields for endpoint URL, model name, and API key (optional)
- Support for environment variables to persist direct model access settings:
  - `LT_DIRECT_ENABLED` - Auto-enable direct model access on startup
  - `LT_DIRECT_ENDPOINT` - Default endpoint URL
  - `LT_DIRECT_MODEL` - Default model name
  - `LT_DIRECT_API_KEY` - Default API key (optional)
- OpenAI-compatible API support (`/v1/chat/completions` endpoint)
- Privacy-focused offline mode when using local models
- Comprehensive error handling for connection and API errors
- Build script (`build.sh`) for easy extension building
- Documentation:
  - `BUILD.md` - Build and installation guide
  - `TESTING.md` - Testing procedures for new features
  - `CHANGELOG.md` - Version history

### Changed
- Updated README with local model setup instructions
- Enhanced extension description to highlight local model support
- Improved error messages with context-specific information
- Extension description updated to highlight new capabilities

### Technical Details
- Added `get_direct_answer()` function in `api.py` for OpenAI-compatible API calls
- Extended UI with checkbox and text field controls for direct model configuration
- Routing logic in `_submit_background()` to switch between local and cloud APIs
- Automatic endpoint normalization (auto-appends `/v1` if missing)
- Uses only built-in Python modules (no external dependencies)

## [0.1.8] - Previous Release

### Features
- AI-assisted text editing in LibreOffice Writer sidebar
- Free cloud model (no signup required)
- OpenAI API key support via `LT_LLM_API_KEY` environment variable
- Text rephrasing, summarizing, and proofreading capabilities
- Radio button options for selected text vs entire document

[Unreleased]: https://github.com/yourusername/librethinker-extension/compare/v0.1.8...HEAD
[0.1.8]: https://github.com/yourusername/librethinker-extension/releases/tag/v0.1.8
