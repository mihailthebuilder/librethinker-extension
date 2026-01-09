# -*- coding: utf-8 -*-
#!/usr/bin/env python

# =============================================================================
#
# Write your code here
#
# =============================================================================

import uno, tempfile, unohelper
import os, random, string, threading
from uuid import uuid4
from .utils import wrap_text, is_older

from .api import get_answer, get_direct_answer, Request
from com.sun.star.awt.PosSize import POSSIZE
from com.sun.star.awt import XItemListener
from com.sun.star.awt.MessageBoxButtons import (
    BUTTONS_OK,
    BUTTONS_OK_CANCEL,
    BUTTONS_YES_NO,
    BUTTONS_YES_NO_CANCEL,
    BUTTONS_RETRY_CANCEL,
    BUTTONS_ABORT_IGNORE_RETRY,
)
from com.sun.star.awt.MessageBoxButtons import (
    DEFAULT_BUTTON_OK,
    DEFAULT_BUTTON_CANCEL,
    DEFAULT_BUTTON_RETRY,
    DEFAULT_BUTTON_YES,
    DEFAULT_BUTTON_NO,
    DEFAULT_BUTTON_IGNORE,
)
from com.sun.star.awt.MessageBoxType import (
    MESSAGEBOX,
    INFOBOX,
    WARNINGBOX,
    ERRORBOX,
    QUERYBOX,
)
from com.sun.star.beans import PropertyValue

try:
    from ui.Panel1_UI import Panel1_UI
except:
    from pythonpath.ui.Panel1_UI import Panel1_UI

# -------------------------------------
# HELPERS FOR MRI AND  XRAY
# -------------------------------------

# Uncomment for MRI
# def mri(ctx, target):
#     mri = ctx.ServiceManager.createInstanceWithContext("mytools.Mri", ctx)
#     mri.inspect(target)

# Uncomment for Xray
# def xray(myObject):
#     try:
#         sm = uno.getComponentContext().ServiceManager
#         mspf = sm.createInstanceWithContext("com.sun.star.script.provider.MasterScriptProviderFactory", uno.getComponentContext())
#         scriptPro = mspf.createScriptProvider("")
#         xScript = scriptPro.getScript("vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
#         xScript.invoke((myObject,), (), ())
#         return
#     except:
#         raise _rtex("\nBasic library Xray is not installed", uno.getComponentContext())
# -------------------------------------------------------------------


class Panel1(Panel1_UI, XItemListener):
    """
    Class documentation...
    """

    def __init__(
        self, ctx=uno.getComponentContext(), dialog=None, **kwargs
    ):  # (self, panelWin, context=uno.getComponentContext()):

        self.ctx = ctx
        self.dialog = dialog

        Panel1_UI.__init__(self, ctx=self.ctx, dialog=self.dialog)

        # get desktop
        desktop = ctx.getByName("/singletons/com.sun.star.frame.theDesktop")
        # get document
        self.document = desktop.getCurrentComponent()

        self.ExtensionVersion = "0.1.8"

        # Add direct model access controls
        self._add_direct_model_controls()

    def _add_direct_model_controls(self):
        """Add UI controls for direct model access (Ollama/LM Studio)"""
        dialogLeftPadding = 6

        # Read default values from environment variables
        direct_enabled = os.environ.get("LT_DIRECT_ENABLED", "").lower() in ("1", "true")
        direct_endpoint = os.environ.get("LT_DIRECT_ENDPOINT", "http://localhost:11434/v1")
        direct_model = os.environ.get("LT_DIRECT_MODEL", "llama3")
        direct_api_key = os.environ.get("LT_DIRECT_API_KEY", "")

        # Add Replace/Append checkboxes (using checkboxes to avoid radio button auto-grouping issues)
        self.ReplaceOption = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlCheckBoxModel"
        )
        self.ReplaceOption.Name = "ReplaceOption"
        self.ReplaceOption.TabIndex = 4
        self.ReplaceOption.PositionX = 82
        self.ReplaceOption.PositionY = 146
        self.ReplaceOption.Width = 64
        self.ReplaceOption.Height = 10
        self.ReplaceOption.Label = "Replace text"
        self.ReplaceOption.State = 0
        self.DialogModel.insertByName("ReplaceOption", self.ReplaceOption)

        self.AppendOption = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlCheckBoxModel"
        )
        self.AppendOption.Name = "AppendOption"
        self.AppendOption.TabIndex = 5
        self.AppendOption.PositionX = 82
        self.AppendOption.PositionY = 157
        self.AppendOption.Width = 64
        self.AppendOption.Height = 10
        self.AppendOption.Label = "Append to text"
        self.AppendOption.State = 1
        self.DialogModel.insertByName("AppendOption", self.AppendOption)

        # Move StatusText down to make room for new controls
        self.StatusText.PositionY = 260

        # Checkbox: Direct model access
        self.DirectModelCheckbox = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlCheckBoxModel"
        )
        self.DirectModelCheckbox.Name = "DirectModelCheckbox"
        self.DirectModelCheckbox.PositionX = dialogLeftPadding
        self.DirectModelCheckbox.PositionY = 170
        self.DirectModelCheckbox.Width = 136
        self.DirectModelCheckbox.Height = 10
        self.DirectModelCheckbox.Label = "Direct model access"
        self.DirectModelCheckbox.State = 1 if direct_enabled else 0
        self.DialogModel.insertByName("DirectModelCheckbox", self.DirectModelCheckbox)

        # Text field: Endpoint
        self.EndpointLabel = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.EndpointLabel.Name = "EndpointLabel"
        self.EndpointLabel.PositionX = dialogLeftPadding + 10
        self.EndpointLabel.PositionY = 182
        self.EndpointLabel.Width = 40
        self.EndpointLabel.Height = 10
        self.EndpointLabel.Label = "Endpoint:"
        self.DialogModel.insertByName("EndpointLabel", self.EndpointLabel)

        self.EndpointField = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )
        self.EndpointField.Name = "EndpointField"
        self.EndpointField.PositionX = dialogLeftPadding + 10
        self.EndpointField.PositionY = 192
        self.EndpointField.Width = 126
        self.EndpointField.Height = 12
        self.EndpointField.Text = direct_endpoint
        self.EndpointField.Enabled = direct_enabled
        self.DialogModel.insertByName("EndpointField", self.EndpointField)

        # Text field: Model
        self.ModelLabel = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.ModelLabel.Name = "ModelLabel"
        self.ModelLabel.PositionX = dialogLeftPadding + 10
        self.ModelLabel.PositionY = 206
        self.ModelLabel.Width = 40
        self.ModelLabel.Height = 10
        self.ModelLabel.Label = "Model:"
        self.DialogModel.insertByName("ModelLabel", self.ModelLabel)

        self.ModelField = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )
        self.ModelField.Name = "ModelField"
        self.ModelField.PositionX = dialogLeftPadding + 10
        self.ModelField.PositionY = 216
        self.ModelField.Width = 126
        self.ModelField.Height = 12
        self.ModelField.Text = direct_model
        self.ModelField.Enabled = direct_enabled
        self.DialogModel.insertByName("ModelField", self.ModelField)

        # Text field: API Key (optional)
        self.ApiKeyLabel = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.ApiKeyLabel.Name = "ApiKeyLabel"
        self.ApiKeyLabel.PositionX = dialogLeftPadding + 10
        self.ApiKeyLabel.PositionY = 230
        self.ApiKeyLabel.Width = 80
        self.ApiKeyLabel.Height = 10
        self.ApiKeyLabel.Label = "API Key (optional):"
        self.DialogModel.insertByName("ApiKeyLabel", self.ApiKeyLabel)

        self.ApiKeyField = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )
        self.ApiKeyField.Name = "ApiKeyField"
        self.ApiKeyField.PositionX = dialogLeftPadding + 10
        self.ApiKeyField.PositionY = 240
        self.ApiKeyField.Width = 126
        self.ApiKeyField.Height = 12
        self.ApiKeyField.Text = direct_api_key
        self.ApiKeyField.Enabled = direct_enabled
        self.DialogModel.insertByName("ApiKeyField", self.ApiKeyField)

        # Add item listeners for manual radio button group management
        selected_text_control = self.DialogContainer.getControl("SelectedTextOption")
        entire_doc_control = self.DialogContainer.getControl("EntireDocumentOption")
        replace_control = self.DialogContainer.getControl("ReplaceOption")
        append_control = self.DialogContainer.getControl("AppendOption")

        selected_text_control.addItemListener(self)
        entire_doc_control.addItemListener(self)
        replace_control.addItemListener(self)
        append_control.addItemListener(self)

        # Add action listener for checkbox to enable/disable fields
        checkbox_control = self.DialogContainer.getControl("DirectModelCheckbox")
        checkbox_control.addItemListener(self)

        # Adjust dialog height to accommodate new controls
        self.DialogModel.Height = 320

    def getHeight(self):
        return self.DialogContainer.Size.Height

    # --------- my code ---------------------
    # mri(self.LocalContext, self.DialogContainer)
    # xray(self.DialogContainer)

    def myFunction(self):
        # TODO: not implemented
        pass

    def itemStateChanged(self, event):
        """Handle item state changes for checkboxes"""
        control_name = None
        try:
            control_name = event.Source.Model.Name
        except:
            pass

        # Handle Direct model access checkbox
        if control_name == "DirectModelCheckbox":
            enabled = event.Selected == 1
            self.EndpointField.Enabled = enabled
            self.ModelField.Enabled = enabled
            self.ApiKeyField.Enabled = enabled
            return

        # Manual checkbox group handling - enforce mutual exclusivity
        # When checked: uncheck the other in its group
        # When unchecked: re-check it (prevent having none selected)

        # Input group: SelectedTextOption and EntireDocumentOption
        if control_name == "SelectedTextOption":
            if event.Selected == 1:
                self.EntireDocumentOption.State = 0
            else:
                # Prevent unchecking - keep it checked
                self.SelectedTextOption.State = 1
        elif control_name == "EntireDocumentOption":
            if event.Selected == 1:
                self.SelectedTextOption.State = 0
            else:
                # Prevent unchecking - keep it checked
                self.EntireDocumentOption.State = 1

        # Output group: ReplaceOption and AppendOption
        elif control_name == "ReplaceOption":
            if event.Selected == 1:
                self.AppendOption.State = 0
            else:
                # Prevent unchecking - keep it checked
                self.ReplaceOption.State = 1
        elif control_name == "AppendOption":
            if event.Selected == 1:
                self.ReplaceOption.State = 0
            else:
                # Prevent unchecking - keep it checked
                self.AppendOption.State = 1

    # --------- helpers ---------------------

    def messageBox(self, MsgText, MsgTitle, MsgType=MESSAGEBOX, MsgButtons=BUTTONS_OK):
        sm = self.ctx.ServiceManager
        si = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", self.ctx)
        mBox = si.createMessageBox(self.Toolkit, MsgType, MsgButtons, MsgTitle, MsgText)
        mBox.execute()

    # -----------------------------------------------------------
    #               Execute dialog
    # -----------------------------------------------------------

    def showDialog(self):
        self.DialogContainer.setVisible(True)
        self.DialogContainer.createPeer(self.Toolkit, None)
        self.DialogContainer.execute()

    # -----------------------------------------------------------
    #               Action events
    # -----------------------------------------------------------

    def get_all_txt(self):
        tmp_dir = tempfile.gettempdir()
        name = (
            "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
            + ".txt"
        )
        out_path = os.path.join(tmp_dir, name)

        file_url = unohelper.systemPathToFileUrl(os.path.abspath(out_path))

        props = (
            PropertyValue(Name="FilterName", Value="Text (encoded)"),
            PropertyValue(
                Name="FilterData", Value=(PropertyValue(Name="Encoding", Value="UTF8"),)
            ),
        )

        self.document.storeToURL(file_url, props)

        with open(out_path, "r", encoding="utf-8-sig", errors="replace") as f:
            txt = f.read()

        try:
            os.remove(out_path)
        except OSError:
            pass

        return txt

    def get_selected_txt(self):
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx
        )
        model = desktop.getCurrentComponent()
        selection = model.CurrentController.getSelection()
        text_range = selection.getByIndex(0)
        return text_range.getString()

    def Submit_OnClick(self):
        try:
            self.StatusText.Label = "Loading..."
            self.Submit.Enabled = False

            docText = (
                self.get_all_txt()
                if self.EntireDocumentOption.State
                else self.get_selected_txt()
            )
            inputPrompt = self.DialogContainer.getControl("Prompt").getText()

            CHARACTER_LIMIT = 380_000
            if len(docText + inputPrompt) > CHARACTER_LIMIT:
                raise Exception(
                    f"Input text is too long ({len(docText) + len(inputPrompt)} characters).\nPlease reduce the size to under {CHARACTER_LIMIT} characters."
                )

            threading.Thread(
                target=self._submit_background, args=(inputPrompt, docText)
            ).start()

        except Exception as e:
            self.messageBox(str(e), "Error", ERRORBOX)
            self.StatusText.Label = ""
            self.Submit.Enabled = True

    def _submit_background(self, inputPrompt: str, docText: str):
        requestId = None  # Initialize for error handling
        direct_mode_enabled = False  # Initialize for error handling

        try:
            # Check if direct model access is enabled
            direct_mode_enabled = self.DirectModelCheckbox.State == 1

            if direct_mode_enabled:
                # Use direct model access (Ollama/LM Studio)
                endpoint = self.EndpointField.Text.strip()
                model = self.ModelField.Text.strip()
                api_key = self.ApiKeyField.Text.strip() or None

                if not endpoint or not model:
                    raise Exception("Endpoint and Model fields are required for direct model access")

                response_text = get_direct_answer(
                    endpoint=endpoint,
                    model=model,
                    api_key=api_key,
                    prompt=inputPrompt,
                    doc_text=docText
                )

                # Insert response into document
                desktop = self.ctx.ServiceManager.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", self.ctx
                )
                model_doc = desktop.getCurrentComponent()
                selection = model_doc.CurrentController.getSelection()
                text_range = selection.getByIndex(0)

                # Check if Replace or Append mode
                if self.ReplaceOption.State == 1:
                    # Replace: just use the response
                    text_range.setString(response_text)
                else:
                    # Append: add response to existing text
                    previous_text = text_range.getString()
                    text_range.setString(previous_text + response_text)

                label = "Done."
                label = wrap_text(input=label, limit=50)
                self.StatusText.Label = label
                self.Submit.Enabled = True

            else:
                # Use original librethinker.com API
                apiKey = os.environ.get("LT_LLM_API_KEY")
                self.FreeModel = apiKey is None

                requestId = str(uuid4())
                request = Request(
                    id=requestId,
                    inputPrompt=inputPrompt,
                    docText=docText,
                    apiKey=apiKey,
                    extensionVersion=self.ExtensionVersion,
                )

                answer = get_answer(request)
                if not answer.success:
                    raise Exception(answer.message)

                self.LatestExtensionVersion = answer.latestExtensionVersion

                desktop = self.ctx.ServiceManager.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", self.ctx
                )
                model_doc = desktop.getCurrentComponent()
                selection = model_doc.CurrentController.getSelection()
                text_range = selection.getByIndex(0)

                # Check if Replace or Append mode
                if self.ReplaceOption.State == 1:
                    # Replace: just use the response
                    text_range.setString(answer.response)
                else:
                    # Append: add response to existing text
                    previous_text = text_range.getString()
                    text_range.setString(previous_text + answer.response)

                label = "Done."
                if is_older(self.ExtensionVersion, self.LatestExtensionVersion):
                    label += " New version is out, please update."

                if self.FreeModel:
                    label += " You're using a free model; visit librethinker.com to learn about alternatives."

                label = wrap_text(input=label, limit=50)

                self.StatusText.Label = label
                self.Submit.Enabled = True

        except Exception as e:
            error = "Error getting answer."

            if direct_mode_enabled:
                error += f"\n\nUsing direct model access.\nDetails: {str(e)}"
            else:
                if hasattr(self, 'FreeModel') and self.FreeModel:
                    error += "\nYou are using the free model which may have issues. Try again later or set up an API key."
                if requestId:
                    error += f"\nRequest ID: {requestId}."
                error += f"\nDetails: {str(e)}"

            self.messageBox(error, "Error", ERRORBOX)
            self.StatusText.Label = ""
            self.Submit.Enabled = True

    # -----------------------------------------------------------
    #               Window (dialog/panel) events
    # -----------------------------------------------------------

    def resizeControls(self, dialog):
        # # see https://forum.openoffice.org/en/forum/viewtopic.php?f=45&t=85181#
        # ratio = 1.1
        # margin = 5
        # dlg_width = dialog.Size.Width
        # # add control names
        # controls = ['btnOK', 'lbList', 'cbPrinters']
        # for c in controls:
        #    cntr = dialog.getControl(c)
        #    width = (dlg_width / ratio) - margin
        #    cntr.setPosSize(cntr.PosSize.X, cntr.PosSize.Y, width, cntr.PosSize.Height, POSSIZE)
        pass


def Run_Panel1(*args):
    """
    Intended to be used in a development environment only
    Copy this file in src dir and run with (Tools - Macros - MyMacros)
    After development copy this file back
    """
    try:
        ctx = remote_ctx  # IDE
    except:
        ctx = uno.getComponentContext()  # UI

    # dialog
    dialog = ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.awt.UnoControlDialog", ctx
    )

    app = Panel1(ctx=ctx, dialog=dialog)
    app.showDialog()


g_exportedScripts = (Run_Panel1,)

# -------------------------------------
# HELPER FOR AN IDE
# -------------------------------------

if __name__ == "__main__":
    """Connect to LibreOffice proccess.
    1) Start the office in shell with command:
    soffice "--accept=socket,host=127.0.0.1,port=2002,tcpNoDelay=1;urp;StarOffice.ComponentContext" --norestore
    2) Run script
    """
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "pythonpath"))

    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstance(
        "com.sun.star.bridge.UnoUrlResolver"
    )
    try:
        remote_ctx = resolver.resolve(
            "uno:socket,"
            "host=127.0.0.1,"
            "port=2002,"
            "tcpNoDelay=1;"
            "urp;"
            "StarOffice.ComponentContext"
        )
    except Exception as err:
        print(err)

    Run_Panel1()
