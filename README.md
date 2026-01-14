# LibreThinker

LibreThinker is a LibreOffice Writer extension that brings AI-assisted text 
editing directly into your sidebar. It integrates an LLM to help you rewrite, improve, 
and edit text without leaving your document.

![Screenshot](./screenshot.png)

## Quickstart

Download the latest extension file (.oxt) from the [LibreOffice extension directory](https://extensions.libreoffice.org/en/extensions/show/99471). Open LibreOffice Writer, go to *Tools > Extension Manager > Add*, and select the downloaded .oxt file to install.

Open the sidebar in LibreOffice; you should see the lightbulb icon for the extension. Click on the icon to open the extension's sidebar panel, then you're ready to go!

**Note on model quality:**  By default, the extension falls back to a free model, which is significantly lower quality. For best results, it is recommended to use an OpenAI model (see below).

## OpenAI model

Generate an API key on the OpenAI platform: https://platform.openai.com/settings/organization/api-keys 

Set the key as the `LT_LLM_API_KEY` environment variable in your operating system.

Restart LibreOffice. The extension will now use the API key from your environment variable.

## License

See [license.txt](./extension/registration/license.txt) for license.

## More info

Check out the project's site [librethinker.com](https://librethinker.com)