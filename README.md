# LibreThinker

LibreThinker is a LibreOffice Writer extension that brings AI-assisted text
editing directly into your sidebar. It integrates with LLMs to help you rewrite, improve,
and edit text without leaving your document.

![Screenshot](./screenshot.png)

## Features

- **Local Model Support**: Connect directly to Ollama, LM Studio, or any OpenAI-compatible local server
- **Cloud API Support**: Use the free cloud model or bring your own OpenAI API key
- **Flexible Configuration**: Choose between local and cloud models with a simple checkbox
- **Privacy-Focused**: Run completely offline with local models
- **No Signup Required**: Use the free cloud model or your own local models without creating accounts

## Quickstart

### Installation

Download the latest extension file (.oxt) from the [LibreOffice extension directory](https://extensions.libreoffice.org/en/extensions/show/99471). Either double-click the .oxt file; or, open LibreOffice Writer, go to *Tools > Extension Manager > Add*, and select the downloaded .oxt file.

Open the sidebar in LibreOffice (View > Sidebar or F5); you should see the lightbulb icon for the extension. Click on the icon to open the extension's sidebar panel, then you're ready to go!

### Option 1: Local Models (Ollama / LM Studio)

**Best for privacy and offline use**

1. Install and run [Ollama](https://ollama.com/) or [LM Studio](https://lmstudio.ai/)
2. For Ollama, pull a model: `ollama pull llama3`
3. In the LibreThinker sidebar, check **"Direct model access"**
4. Configure:
   - **Endpoint**: `http://localhost:11434/v1` (Ollama default)
   - **Model**: `llama3` (or your chosen model)
   - **API Key**: Leave empty for Ollama

For persistent settings, set environment variables before starting LibreOffice:

```bash
export LT_DIRECT_ENABLED=1
export LT_DIRECT_ENDPOINT=http://localhost:11434/v1
export LT_DIRECT_MODEL=llama3
```

### Option 2: Cloud API (OpenAI)

**Best for quality with paid API**

Generate an API key on the OpenAI platform: https://platform.openai.com/settings/organization/api-keys

Set the key as the `LT_LLM_API_KEY` environment variable in your operating system:

```bash
export LT_LLM_API_KEY=sk-your-api-key-here
```

Restart LibreOffice. Make sure **"Direct model access"** is unchecked to use the cloud API.

### Option 3: Free Cloud Model

**No setup required, but lower quality**

Simply uncheck **"Direct model access"** and start using the extension. The free model is provided as a fallback but has significantly lower quality than local models or OpenAI.

## Building from Source

See [BUILD.md](./BUILD.md) for detailed build and installation instructions.

```bash
./build.sh
```

## License

See [license.txt](./extension/registration/license.txt) for license.