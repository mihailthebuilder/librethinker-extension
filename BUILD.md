# Building the LibreThinker Extension

## Quick Build

Simply run the build script:

```bash
./build.sh
```

This will create `dist/LibreThinker.oxt` which can be installed in LibreOffice.

## Manual Build

If you prefer to build manually, an .oxt file is just a ZIP archive with a specific structure. From the extension directory:

```bash
mkdir -p dist
cd extension
zip -r ../dist/LibreThinker.oxt \
    META-INF/ \
    description.xml \
    description/ \
    empty_dialog.xdl \
    Factory.xcu \
    ProtocolHandler.xcu \
    Sidebar.xcu \
    image/ \
    registration/ \
    src/
cd ..
```

## Installing the Extension

### Method 1: Double-Click (Easiest)
1. Double-click `dist/LibreThinker.oxt`
2. LibreOffice will open and prompt you to install the extension

### Method 2: Extension Manager
1. Open LibreOffice Writer
2. Go to **Tools > Extension Manager**
3. Click **Add**
4. Navigate to and select `dist/LibreThinker.oxt`
5. Click **Open**
6. Accept the license agreement
7. Close the Extension Manager

### Method 3: Command Line
```bash
# On macOS
"/Applications/LibreOffice.app/Contents/MacOS/unopkg" add dist/LibreThinker.oxt

# On Linux
unopkg add dist/LibreThinker.oxt

# On Windows
"C:\Program Files\LibreOffice\program\unopkg.exe" add dist\LibreThinker.oxt
```

## Using the Extension

1. Open LibreOffice Writer
2. Open the sidebar (View > Sidebar or F5)
3. Look for the lightbulb icon in the sidebar
4. Click the icon to open the LibreThinker panel
5. Configure your settings:
   - For **direct model access** (Ollama/LM Studio):
     - Check "Direct model access"
     - Set endpoint (default: http://localhost:11434/v1)
     - Set model name (e.g., llama3)
     - Optionally set API key
   - For **cloud API** (librethinker.com):
     - Leave "Direct model access" unchecked
     - Optionally set `LT_LLM_API_KEY` environment variable for OpenAI

## Uninstalling

### Via Extension Manager
1. Open **Tools > Extension Manager**
2. Select **LibreThinker**
3. Click **Remove**
4. Restart LibreOffice

### Via Command Line
```bash
# On macOS
"/Applications/LibreOffice.app/Contents/MacOS/unopkg" remove org.librethinker.LibreThinkerExtension

# On Linux
unopkg remove org.librethinker.LibreThinkerExtension

# On Windows
"C:\Program Files\LibreOffice\program\unopkg.exe" remove org.librethinker.LibreThinkerExtension
```

## Environment Variables

Set these **before** starting LibreOffice:

### For Direct Model Access (Ollama/LM Studio)
```bash
export LT_DIRECT_ENABLED=1
export LT_DIRECT_ENDPOINT=http://localhost:11434/v1
export LT_DIRECT_MODEL=llama3
export LT_DIRECT_API_KEY=your-key-here  # Optional
```

### For Cloud API (OpenAI)
```bash
export LT_LLM_API_KEY=sk-your-openai-api-key
```

### Setting Environment Variables Permanently

**macOS/Linux:**
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
export LT_DIRECT_ENABLED=1
export LT_DIRECT_ENDPOINT=http://localhost:11434/v1
export LT_DIRECT_MODEL=llama3
```

Then restart your terminal or run `source ~/.zshrc`

**Windows:**
1. Search for "Environment Variables" in Start menu
2. Click "Edit system environment variables"
3. Click "Environment Variables"
4. Add new user variables

## Troubleshooting

### Extension doesn't appear in sidebar
- Restart LibreOffice completely
- Check Tools > Extension Manager to verify it's installed
- Try View > Sidebar (F5) to open the sidebar

### Direct model access connection errors
- Verify Ollama/LM Studio is running
- Check the endpoint URL is correct
- Try `curl http://localhost:11434/v1/models` to test connectivity

### Changes not reflected after rebuild
1. Uninstall the old extension
2. Restart LibreOffice completely
3. Install the new extension
4. Restart LibreOffice again

### Python errors
- Ensure all .py files are in the correct locations under `src/pythonpath/`
- Check `META-INF/manifest.xml` references the correct files

## Development Workflow

1. Make code changes
2. Run `./build.sh` to rebuild
3. Uninstall old extension in LibreOffice
4. Restart LibreOffice
5. Install new extension
6. Restart LibreOffice again
7. Test changes

## References

- [LibreOffice Extension Development Documentation](https://wiki.documentfoundation.org/Development/Extension_Development)
- [Python-UNO Bridge](https://wiki.documentfoundation.org/Documentation/DevGuide/Professional_UNO)
- [Extension Packaging](https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/Extensions)
