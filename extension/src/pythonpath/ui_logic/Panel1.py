# -*- coding: utf-8 -*-
#!/usr/bin/env python

# =============================================================================
#
# Write your code here
#
# =============================================================================

import uno, tempfile, unohelper
import os, random, string, threading
from .utils import is_older, is_ollama, ollama_model
from dataclasses import dataclass


from .settings import Settings
import traceback

from .api import LtClient, OllamaClient
from com.sun.star.awt.PosSize import POSSIZE
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


@dataclass
class Response:
    answer: str
    label: str


class Panel1(Panel1_UI):
    """
    Class documentation...
    """

    def __init__(
        self, ctx=uno.getComponentContext(), dialog=None, **kwargs
    ):  # (self, panelWin, context=uno.getComponentContext()):

        try:
            self.ctx = ctx
            self.dialog = dialog

            self.settings = Settings(ctx)
            Panel1_UI.__init__(
                self, ctx=self.ctx, dialog=self.dialog, settings=self.settings
            )

            # get desktop
            desktop = ctx.getByName("/singletons/com.sun.star.frame.theDesktop")
            # get document
            self.document = desktop.getCurrentComponent()

        except Exception as e:
            self.messageBox(
                f"Error initializing panel: {str(traceback.format_exc())}",
                "Error",
                ERRORBOX,
            )

    def getHeight(self):
        return self.DialogContainer.Size.Height

    # --------- my code ---------------------
    # mri(self.LocalContext, self.DialogContainer)
    # xray(self.DialogContainer)

    def myFunction(self):
        # TODO: not implemented
        pass

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
        if self.Submit.Enabled is False:
            return

        # Needs to be here as get_all_txt() refreshes the Submit button state
        docText = (
            self.get_all_txt()
            if self.EntireDocumentOption.State
            else self.get_selected_txt()
        )

        self.Submit.Enabled = False
        self.StatusText.Label = "Loading..."

        threading.Thread(target=self.submit_background, args=(docText,)).start()

    def submit_background(self, docText: str):
        try:
            inputPrompt = self.DialogContainer.getControl("Prompt").getText()

            model: str = self.DialogContainer.getControl("ModelId").getText()

            response = (
                self.server_response(inputPrompt, docText, model)
                if not is_ollama(model)
                else self.ollama_response(inputPrompt, docText, ollama_model(model))
            )

            desktop = self.ctx.ServiceManager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", self.ctx
            )
            currentComponent = desktop.getCurrentComponent()
            selection = currentComponent.CurrentController.getSelection()
            text_range = selection.getByIndex(0)
            previous_text = text_range.getString()
            text_range.setString(previous_text + response.answer)

            self.StatusText.Label = response.label

        except Exception as e:
            self.messageBox(str(e), "Error", ERRORBOX)
            self.StatusText.Label = ""
        finally:
            self.Submit.Enabled = True

    def server_response(self, inputPrompt: str, docText: str, model: str) -> Response:
        extensionVersion = "0.2.9"

        apiKey: str = self.DialogContainer.getControl("ModelApiKey").getText()

        client = LtClient(extensionVersion=extensionVersion)
        answer = client.getAnswer(
            inputPrompt=inputPrompt, docText=docText, apiKey=apiKey, model=model
        )

        freeModel = len(apiKey) == 0 and len(model) == 0

        if not answer.success:
            error_message = "Error getting response."
            if freeModel:
                error_message += "\nYou are using the free model which may have issues. Try again later or set up an API key."

            error_message += (
                f"\nRequest ID: {client.requestId}.\nDetails: {str(answer.message)}"
            )

            raise Exception(error_message)

        label = "Done."
        if is_older(extensionVersion, answer.latestExtensionVersion):
            label += " New version is out, please update."

        if freeModel:
            label += " You're using a free model; visit librethinker.com to learn about alternatives."
        else:
            label += f" Generated with model {model}."

        return Response(answer=answer.response, label=label)

    def ollama_response(self, userPrompt: str, text: str, model: str) -> Response:
        client = OllamaClient()
        answer = client.getAnswer(userPrompt=userPrompt, text=text, model=model)
        if not answer.success:
            error_message = (
                f"Error getting response from Ollama.\nDetails: {str(answer.message)}"
            )
            raise Exception(error_message)
        label = f"Done. Generated with Ollama model {model}."
        return Response(answer=answer.response, label=label)

    def SaveSettings_OnClick(self):
        try:
            if self.SaveSettings.Enabled is False:
                return

            self.SaveSettingsStatus.Label = "Saving..."
            self.SaveSettings.Enabled = False

            model = self.DialogContainer.getControl("ModelId").getText()
            apiKey = self.DialogContainer.getControl("ModelApiKey").getText()
            self.settings.save(modelId=model, apiKey=apiKey)

            self.SaveSettingsStatus.Label = "Saved."

        except Exception as e:
            self.messageBox(f"Error saving settings: {str(e)}", "Error", ERRORBOX)
            self.SaveSettingsStatus.Label = ""
        finally:
            self.SaveSettings.Enabled = True

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
