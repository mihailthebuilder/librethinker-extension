# LibreThinker

LibreThinker is a LibreOffice Writer extension that brings AI-assisted text 
editing directly into your sidebar. It integrates an LLM to help you rewrite, improve, 
and edit text without leaving your document.

You can use a free online LLM (no signup required), locally self-hosted Ollama, or bring your API key (ChatGPT/OpenAI, Mistral, Groq, etc).

![Screenshot](./screenshot.png)

## Quickstart

Download the latest extension file (.oxt) from the [LibreOffice extension directory](https://extensions.libreoffice.org/en/extensions/show/99471). Open LibreOffice Writer, go to *Tools > Extension Manager > Add*, and select the downloaded .oxt file to install.

Open the sidebar in LibreOffice; you should see the lightbulb icon for the extension. Click the icon to open the extension panel, then you're ready to start using the free model!

## Bring your API key

You can connect to a wide range of LLM APIs using your own API key.

Go to [LiteLLM's model directory](https://models.litellm.ai/), and find the model that you wish to connect to. Copy its value from the `Model` column - eg `gpt-5.2`, or `mistral/mistral-medium`.

Go back to the extension, and set the value as the model ID in the Optional Settings section. Then set the API key in that section as well.

The extension will now use the LLM vendor's API, with your key, to generate the text.

## Ollama

In the BYOK/Ollama Settings, set the model ID as `sh/ollama/{ollamaModelYouWant}` ; for example, `sh/ollama/gemma3:1b` to use the `gemma3:1b` Ollama model.

## License

See [license.txt](./extension/registration/license.txt) for license.

## More info

Check out the project's site [librethinker.com](https://librethinker.com)