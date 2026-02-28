# -*- coding: utf-8 -*-
#!/usr/bin/env python

# =============================================================================
#
# Dialog implementation generated from a XDL file.
#
# Created: Sun Nov 23 01:30:57 2025
#      by: unodit 0.8.0
#
# WARNING! All changes made in this file will be overwritten
#          if the file is generated again!
#
# =============================================================================

import uno
import unohelper
from com.sun.star.awt import XActionListener
from com.sun.star.awt import XWindowListener
from com.sun.star.task import XJobExecutor
from ui_logic.settings import Settings


class Panel1_UI(unohelper.Base, XActionListener, XWindowListener, XJobExecutor):
    """
    Class documentation...
    """

    def __init__(
        self, ctx=uno.getComponentContext(), dialog=None, settings: Settings = None
    ):
        self.LocalContext = ctx
        self.dlg = dialog
        self.settings = settings
        self.ServiceManager = self.LocalContext.ServiceManager
        self.Toolkit = self.ServiceManager.createInstanceWithContext(
            "com.sun.star.awt.ExtToolkit", self.LocalContext
        )

        # -----------------------------------------------------------
        #               Create dialog and insert controls
        # -----------------------------------------------------------

        # --------------create dialog container and set model and properties
        self.DialogContainer = self.dlg
        self.DialogModel = self.ServiceManager.createInstance(
            "com.sun.star.awt.UnoControlDialogModel"
        )
        self.DialogContainer.setModel(self.DialogModel)
        self.DialogModel.Name = "LlmDialog"
        self.DialogModel.PositionX = "204"
        self.DialogModel.PositionY = "117"
        self.DialogModel.Width = 156
        self.DialogModel.Height = 360
        self.DialogModel.Closeable = True
        self.DialogModel.Moveable = True

        dialogLeftPadding = "6"

        # --------- create an instance of Edit control, set properties ---
        self.Prompt = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )

        self.Prompt.Name = "Prompt"
        self.Prompt.TabIndex = 0
        self.Prompt.PositionX = dialogLeftPadding
        self.Prompt.PositionY = "8"
        self.Prompt.Width = 136
        self.Prompt.Height = 104
        self.Prompt.Text = "YourPromptHere"
        self.Prompt.MultiLine = True
        self.Prompt.VerticalAlign = "TOP"
        self.Prompt.AutoVScroll = True

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("Prompt", self.Prompt)

        # --------- create an instance of Button control, set properties ---
        self.Submit = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlButtonModel"
        )

        self.Submit.Name = "Submit"
        self.Submit.TabIndex = self.Prompt.TabIndex + 1
        self.Submit.PositionX = dialogLeftPadding
        self.Submit.PositionY = "120"
        self.Submit.Width = 64
        self.Submit.Height = 23
        self.Submit.Label = "Submit"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("Submit", self.Submit)

        # add the action listener
        self.DialogContainer.getControl("Submit").addActionListener(self)
        self.DialogContainer.getControl("Submit").setActionCommand("Submit_OnClick")

        # --------- create an instance of RadioButton control, set properties ---
        self.SelectedTextOption = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlRadioButtonModel"
        )

        self.SelectedTextOption.Name = "SelectedText"
        self.SelectedTextOption.TabIndex = self.Submit.TabIndex + 1
        self.SelectedTextOption.PositionX = "82"
        self.SelectedTextOption.PositionY = "124"
        self.SelectedTextOption.Width = 64
        self.SelectedTextOption.Height = 10
        self.SelectedTextOption.Label = "Selected text"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("SelectedTextOption", self.SelectedTextOption)

        # --------- create an instance of RadioButton control, set properties ---
        self.EntireDocumentOption = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlRadioButtonModel"
        )

        self.EntireDocumentOption.Name = "EntireDocument"
        self.EntireDocumentOption.TabIndex = self.SelectedTextOption.TabIndex + 1
        self.EntireDocumentOption.PositionX = "82"
        self.EntireDocumentOption.PositionY = "135"
        self.EntireDocumentOption.Width = 64
        self.EntireDocumentOption.Height = 10
        self.EntireDocumentOption.Label = "Entire document"
        self.EntireDocumentOption.State = True

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("EntireDocumentOption", self.EntireDocumentOption)

        self.StatusText = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.StatusText.Name = "StatusText"
        self.StatusText.PositionX = dialogLeftPadding
        self.StatusText.PositionY = "148"
        self.StatusText.Width = 136
        self.StatusText.Height = 30
        self.StatusText.Label = ""
        self.StatusText.MultiLine = True

        self.DialogModel.insertByName("StatusText", self.StatusText)

        self.Support = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedHyperlinkModel"
        )
        self.Support.Name = "Support"
        self.Support.Enabled = True
        self.Support.PositionX = dialogLeftPadding
        self.Support.PositionY = "178"
        self.Support.TabIndex = self.EntireDocumentOption.TabIndex + 1
        self.Support.Width = 136
        self.Support.Height = 10
        self.Support.Label = "Click here for support"
        self.Support.URL = "https://tally.so/r/jaZx41"

        self.DialogModel.insertByName("Support", self.Support)

        self.FeedbackPrompt = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.FeedbackPrompt.Name = "FeedbackPrompt"
        self.FeedbackPrompt.PositionX = dialogLeftPadding
        self.FeedbackPrompt.PositionY = 193
        self.FeedbackPrompt.Width = 136
        self.FeedbackPrompt.Height = 30
        self.FeedbackPrompt.Label = "If you like this extension, please leave a review on the LibreOffice extensions repository! It'll motivate me to keep working on it."
        self.FeedbackPrompt.MultiLine = True

        self.DialogModel.insertByName("FeedbackPrompt", self.FeedbackPrompt)

        self.SettingsSectionHeading = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.SettingsSectionHeading.Name = "SettingsSectionHeading"
        self.SettingsSectionHeading.PositionX = dialogLeftPadding
        self.SettingsSectionHeading.PositionY = self.FeedbackPrompt.PositionY + 40
        self.SettingsSectionHeading.Width = 136
        self.SettingsSectionHeading.Height = 15
        self.SettingsSectionHeading.Label = "--OPTIONAL SETTINGS--"

        self.DialogModel.insertByName(
            "SettingsSectionHeading", self.SettingsSectionHeading
        )

        self.ModelIdLabel = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.ModelIdLabel.Name = "ModelIdLabel"
        self.ModelIdLabel.PositionX = dialogLeftPadding
        self.ModelIdLabel.PositionY = self.SettingsSectionHeading.PositionY + 20
        self.ModelIdLabel.Width = 136
        self.ModelIdLabel.Height = 10
        self.ModelIdLabel.Label = "Model ID (e.g. claude-opus-4-6)"
        self.ModelIdLabel.MultiLine = True

        self.DialogModel.insertByName("ModelIdLabel", self.ModelIdLabel)

        self.ModelId = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )

        self.ModelId.Name = "ModelId"
        self.ModelId.TabIndex = self.Support.TabIndex + 1
        self.ModelId.PositionX = dialogLeftPadding
        self.ModelId.PositionY = self.ModelIdLabel.PositionY + 10
        self.ModelId.Width = 136
        self.ModelId.Height = 15
        self.ModelId.Text = self.settings.modelId

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("ModelId", self.ModelId)

        self.ModelApiKeyLabel = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.ModelApiKeyLabel.Name = "ModelApiKeyLabel"
        self.ModelApiKeyLabel.PositionX = dialogLeftPadding
        self.ModelApiKeyLabel.PositionY = self.ModelId.PositionY + 20
        self.ModelApiKeyLabel.Width = 136
        self.ModelApiKeyLabel.Height = 10
        self.ModelApiKeyLabel.Label = "Model API key"
        self.ModelApiKeyLabel.MultiLine = True

        self.DialogModel.insertByName("ModelApiKeyLabel", self.ModelApiKeyLabel)

        self.ModelApiKey = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlEditModel"
        )

        self.ModelApiKey.Name = "ModelApiKey"
        self.ModelApiKey.TabIndex = self.ModelId.TabIndex + 1
        self.ModelApiKey.PositionX = dialogLeftPadding
        self.ModelApiKey.PositionY = self.ModelApiKeyLabel.PositionY + 10
        self.ModelApiKey.Width = 136
        self.ModelApiKey.Height = 15
        self.ModelApiKey.Text = self.settings.apiKey
        self.ModelApiKey.EchoChar = 42

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("ModelApiKey", self.ModelApiKey)

        # --------- create an instance of Button control, set properties ---
        self.SaveSettings = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlButtonModel"
        )

        self.SaveSettings.Name = "SaveSettings"
        self.SaveSettings.TabIndex = self.ModelApiKey.TabIndex + 1
        self.SaveSettings.PositionX = dialogLeftPadding
        self.SaveSettings.PositionY = self.ModelApiKey.PositionY + 20
        self.SaveSettings.Width = 64
        self.SaveSettings.Height = 23
        self.SaveSettings.Label = "Save settings"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("SaveSettings", self.SaveSettings)

        # add the action listener
        self.DialogContainer.getControl("SaveSettings").addActionListener(self)
        self.DialogContainer.getControl("SaveSettings").setActionCommand(
            "SaveSettings_OnClick"
        )

        self.SaveSettingsStatus = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.SaveSettingsStatus.Name = "SaveSettingsStatus"
        self.SaveSettingsStatus.PositionX = dialogLeftPadding
        self.SaveSettingsStatus.PositionY = self.SaveSettings.PositionY + 30
        self.SaveSettingsStatus.Width = 136
        self.SaveSettingsStatus.Height = 30
        self.SaveSettingsStatus.Label = ""
        self.SaveSettingsStatus.MultiLine = True

        self.DialogModel.insertByName("SaveSettingsStatus", self.SaveSettingsStatus)

        # add the window listener
        self.DialogContainer.addWindowListener(self)

    # -----------------------------------------------------------
    #               Action events
    # -----------------------------------------------------------

    def actionPerformed(self, oActionEvent):

        if oActionEvent.ActionCommand == "Submit_OnClick":
            self.Submit_OnClick()

        if oActionEvent.ActionCommand == "SaveSettings_OnClick":
            self.SaveSettings_OnClick()

    # -----------------------------------------------------------
    #               Window (dialog/panel) events
    # -----------------------------------------------------------

    def windowResized(self, oWindowEvent):
        # print(dir(oWindowEvent.Source))
        self.resizeControls(dialog=oWindowEvent.Source)


# ----------------- END GENERATED CODE ----------------------------------------
