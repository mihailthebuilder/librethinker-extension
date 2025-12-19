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


class Panel1_UI(unohelper.Base, XActionListener, XWindowListener, XJobExecutor):
    """
    Class documentation...
    """

    def __init__(self, ctx=uno.getComponentContext(), dialog=None):
        self.LocalContext = ctx
        self.dlg = dialog
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
        self.DialogModel.Height = 180
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
        self.Submit.TabIndex = 1
        self.Submit.PositionX = dialogLeftPadding
        self.Submit.PositionY = "120"
        self.Submit.Width = 64
        self.Submit.Height = 23
        self.Submit.Label = "Submit"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("Submit", self.Submit)

        # --------- create an instance of RadioButton control, set properties ---
        self.SelectedTextOption = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlRadioButtonModel"
        )

        self.SelectedTextOption.Name = "SelectedText"
        self.SelectedTextOption.TabIndex = 3
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
        self.EntireDocumentOption.TabIndex = 2
        self.EntireDocumentOption.PositionX = "82"
        self.EntireDocumentOption.PositionY = "135"
        self.EntireDocumentOption.Width = 64
        self.EntireDocumentOption.Height = 10
        self.EntireDocumentOption.Label = "Entire document"
        self.EntireDocumentOption.State = True

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("EntireDocumentOption", self.EntireDocumentOption)

        # add the action listener
        self.DialogContainer.getControl("Submit").addActionListener(self)
        self.DialogContainer.getControl("Submit").setActionCommand("Submit_OnClick")

        self.StatusText = self.DialogModel.createInstance(
            "com.sun.star.awt.UnoControlFixedTextModel"
        )
        self.StatusText.Name = "StatusText"
        self.StatusText.PositionX = dialogLeftPadding
        self.StatusText.PositionY = "148"
        self.StatusText.Width = 136
        self.StatusText.Height = 50
        self.StatusText.Label = ""

        self.DialogModel.insertByName("StatusText", self.StatusText)

        # add the window listener
        self.DialogContainer.addWindowListener(self)

    # -----------------------------------------------------------
    #               Action events
    # -----------------------------------------------------------

    def actionPerformed(self, oActionEvent):

        if oActionEvent.ActionCommand == "Submit_OnClick":
            self.Submit_OnClick()

    # -----------------------------------------------------------
    #               Window (dialog/panel) events
    # -----------------------------------------------------------

    def windowResized(self, oWindowEvent):
        # print(dir(oWindowEvent.Source))
        self.resizeControls(dialog=oWindowEvent.Source)


# ----------------- END GENERATED CODE ----------------------------------------
