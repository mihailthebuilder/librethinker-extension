# LibreThinker

LibreThinker is a LibreOffice Writer extension that brings AI-assisted text 
editing directly into your sidebar. It integrates an LLM to help you rewrite, improve, 
and edit text without leaving your document.

![Screenshot](./screenshot.png)

## Quickstart

Download the latest extension file (.oxt) from the [LibreOffice extension directory](https://extensions.libreoffice.org/en/extensions/show/99471). Open LibreOffice Writer, go to *Tools > Extension Manager > Add*, and select the downloaded .oxt file to install.

Open the sidebar in LibreOffice; you should see the lightbulb icon for the extension. Click the icon to open the extension panel, then you're ready to start using the free model!

## Bring your API key

You can also connect to a wide range of LLM APIs using your own API key.

Go to [LiteLLM's model directory](https://models.litellm.ai/), and find the model that you wish to connect to. Copy its value from the `Model` column - eg `gpt-5.2`, or `mistral/mistral-medium`.

Set the value as the `LT_LLM_MODEL` environment variable in your operating system. Then set the API key as the `LT_LLM_API_KEY` environment variable.

Restart LibreOffice Writer. The extension will now use the LLM vendor's API, with your key, to generate the text.

## License

See [license.txt](./extension/registration/license.txt) for license.

## More info

Check out the project's site [librethinker.com](https://librethinker.com)