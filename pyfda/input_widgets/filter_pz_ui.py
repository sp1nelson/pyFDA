# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 16:13:50 2017

@author: muenker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import logging
logger = logging.getLogger(__name__)

from ..compat import (Qt, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                      QFrame, QSpinBox, QFont, QIcon, QVBoxLayout, QHBoxLayout)

from pyfda.pyfda_qt_lib import qset_cmb_box
from pyfda.pyfda_io_lib import CSV_option_box
from pyfda.pyfda_lib import rt_label
from pyfda.pyfda_rc import params

class FilterPZ_UI(QWidget):
    """
    Create the UI for the FilterPZ class
    """


    def __init__(self, parent):
        """
        Pass instance `parent` of parent class (FilterCoeffs)
        """
        super(FilterPZ_UI, self).__init__(parent)
#        self.parent = parent # instance of the parent (not the base) class
        self.eps = 1.e-4 # # tolerance value for e.g. setting P/Z to zero
        
        """
        Intitialize the widget, consisting of:
        - top chkbox row
        - coefficient table
        - two bottom rows with action buttons
        """
        
        self.bfont = QFont()
        self.bfont.setBold(True)
        self.bifont = QFont()
        self.bifont.setBold(True)
        self.bifont.setItalic(True)
#        q_icon_size = QSize(20, 20) # optional, size is derived from butEnable

        # ---------------------------------------------
        # UI Elements for controlling the display
        # ---------------------------------------------
        
        self.butEnable = QPushButton(self)
        self.butEnable.setIcon(QIcon(':/circle-x.svg'))
        q_icon_size = self.butEnable.iconSize() # <- set this for manual icon sizing
        self.butEnable.setIconSize(q_icon_size)
        self.butEnable.setCheckable(True)
        self.butEnable.setChecked(True)
        self.butEnable.setToolTip("<span>Show / hide poles and zeros in an editable table."
                " For high order systems, the table display might be slow.</span>")

        self.cmbPZFrmt = QComboBox(self)
        pz_formats = [('Cartesian', 'cartesian'), ('Polar (rad)', 'polar_rad'),
                      ('Polar (pi)', 'polar_pi'), ('Polar (°)', 'polar_deg')] # display text, data
        # π: u'3C0, °: u'B0, ∠: u'2220
        for pz in pz_formats:
            self.cmbPZFrmt.addItem(*pz)
        self.cmbPZFrmt.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        # self.cmbPZFrmt.setEnabled(False)
        self.cmbPZFrmt.setToolTip("<span>Set display format for poles and zeros to"
                                  " either cartesian (x + jy) or polar (r * &ang; &Omega;)."
                                  " Type 'o' for '&deg;', '&lt;' for '&ang;' and 'pi' for '&pi;'.</span>")

        self.spnDigits = QSpinBox(self)
        self.spnDigits.setRange(0,16)
        self.spnDigits.setToolTip("Number of digits to display.")
        self.lblDigits = QLabel("Digits", self)
        self.lblDigits.setFont(self.bifont)
        
        self.cmbCausal = QComboBox(self)
        causal_types = ['Causal', 'Acausal', 'Anticausal']
        for cs in causal_types:
            self.cmbCausal.addItem(cs)

        qset_cmb_box(self.cmbCausal, 'Causal')
        self.cmbCausal.setToolTip('<span>Set the system type. Not implemented yet.</span>')
        self.cmbCausal.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.cmbCausal.setEnabled(False)
            
        layHDisplay = QHBoxLayout()
        layHDisplay.setAlignment(Qt.AlignLeft)
        layHDisplay.addWidget(self.butEnable)
        layHDisplay.addWidget(self.cmbPZFrmt)
        layHDisplay.addWidget(self.spnDigits)
        layHDisplay.addWidget(self.lblDigits)
        layHDisplay.addWidget(self.cmbCausal)
        layHDisplay.addStretch()

        # ---------------------------------------------
        # UI Elements for setting the gain
        # ---------------------------------------------
        self.lblNorm = QLabel(rt_label("Normalize"), self)
        self.cmbNorm = QComboBox(self)
        self.cmbNorm.addItems(["None", "1", "Max"])
        self.cmbNorm.setToolTip("<span>Set the gain <i>k</i> so that H(f)<sub>max</sub> is "
                                "either 1 or the max. of the previous system.</span>")

        self.lblGain = QLabel(rt_label("k = "), self)
        self.ledGain = QLineEdit(self)
        self.ledGain.setToolTip("<span>Specify gain factor <i>k</i>"
                                " (only possible for Normalize = 'None').</span>")
        self.ledGain.setText(str(1.))
        self.ledGain.setObjectName("ledGain")
        
        layHGain = QHBoxLayout()
        layHGain.addWidget(self.lblNorm)
        layHGain.addWidget(self.cmbNorm)
        layHGain.addWidget(self.lblGain)
        layHGain.addWidget(self.ledGain)
        layHGain.addStretch()

        # ---------------------------------------------
        # UI Elements for loading / storing / manipulating cells and rows
        # ---------------------------------------------

#        self.cmbFilterType = QComboBox(self)
#        self.cmbFilterType.setObjectName("comboFilterType")
#        self.cmbFilterType.setToolTip("Select between IIR and FIR filte for manual entry.")
#        self.cmbFilterType.addItems(["FIR","IIR"])
#        self.cmbFilterType.setSizeAdjustPolicy(QComboBox.AdjustToContents)


        self.butAddCells = QPushButton(self)
        self.butAddCells.setIcon(QIcon(':/row_insert_above.svg'))
        self.butAddCells.setIconSize(q_icon_size)
        self.butAddCells.setToolTip("<SPAN>Select cells to insert a new cell above each selected cell. "
                                "Use &lt;SHIFT&gt; or &lt;CTRL&gt; to select multiple cells. "
                                "When nothing is selected, add a row at the end.</SPAN>")

        self.butDelCells = QPushButton(self)
        self.butDelCells.setIcon(QIcon(':/row_delete.svg'))
        self.butDelCells.setIconSize(q_icon_size)
        self.butDelCells.setToolTip("<SPAN>Delete selected cell(s) from the table. "
                "Use &lt;SHIFT&gt; or &lt;CTRL&gt; to select multiple cells. "
                "When nothing is selected, delete the last row.</SPAN>")

        self.butSave = QPushButton(self)
        self.butSave.setIcon(QIcon(':/upload.svg'))
        self.butSave.setIconSize(q_icon_size)
        self.butSave.setToolTip("<span>Save coefficients and update all plots. "
                                "No modifications are saved before!</span>")

        self.butLoad = QPushButton(self)
        self.butLoad.setIcon(QIcon(':/download.svg'))
        self.butLoad.setIconSize(q_icon_size)
        self.butLoad.setToolTip("Reload coefficients.")

        self.butClear = QPushButton(self)
        self.butClear.setIcon(QIcon(':/trash.svg'))
        self.butClear.setIconSize(q_icon_size)
        self.butClear.setToolTip("Clear all entries.")


        self.butFromTable = QPushButton(self)
        self.butFromTable.setIcon(QIcon(':/to_clipboard.svg'))
        self.butFromTable.setIconSize(q_icon_size)
        self.butFromTable.setToolTip("<span>"
                            "Copy table to clipboard / file, SELECTED items are copied as "
                            "displayed. When nothing is selected, the whole table "
                            "is copied with full precision in decimal format.</span>")
        
        self.butToTable = QPushButton(self)
        self.butToTable.setIcon(QIcon(':/from_clipboard.svg'))
        self.butToTable.setIconSize(q_icon_size)
        self.butToTable.setToolTip("<span>Copy clipboard / file to table.</span>")

        butSettingsClipboard = QPushButton(self)
        butSettingsClipboard.setIcon(QIcon(':/settings.svg'))
        butSettingsClipboard.setIconSize(q_icon_size)
        butSettingsClipboard.setToolTip("<span>Adjust settings for CSV format and whether "
                                "to copy to/from clipboard or file.</span>")

        layHButtonsCoeffs1 = QHBoxLayout()
#        layHButtonsCoeffs1.addWidget(self.cmbFilterType)
        layHButtonsCoeffs1.addWidget(self.butAddCells)
        layHButtonsCoeffs1.addWidget(self.butDelCells)
        layHButtonsCoeffs1.addWidget(self.butClear)
        layHButtonsCoeffs1.addWidget(self.butSave)
        layHButtonsCoeffs1.addWidget(self.butLoad)
        layHButtonsCoeffs1.addWidget(self.butFromTable)
        layHButtonsCoeffs1.addWidget(self.butToTable)
        layHButtonsCoeffs1.addWidget(butSettingsClipboard)
        layHButtonsCoeffs1.addStretch()

        #-------------------------------------------------------------------
        #   Eps / set zero settings
        # ---------------------------------------------------------------------
        self.butSetZero = QPushButton("= 0", self)
        self.butSetZero.setToolTip("<span>Set selected poles / zeros = 0 with a magnitude &lt; &epsilon;. "
        "When nothing is selected, test the whole table.</span>")
        self.butSetZero.setIconSize(q_icon_size)

        lblEps = QLabel(self)
        lblEps.setText("<b><i>for &epsilon;</i> &lt;</b>")

        self.ledEps = QLineEdit(self)
        self.ledEps.setToolTip("Specify tolerance value.")

        layHButtonsCoeffs2 = QHBoxLayout()
        layHButtonsCoeffs2.addWidget(self.butSetZero)
        layHButtonsCoeffs2.addWidget(lblEps)
        layHButtonsCoeffs2.addWidget(self.ledEps)
        layHButtonsCoeffs2.addStretch()

        # ########################  Main UI Layout ############################
        # layout for frame (UI widget)
        layVMainF = QVBoxLayout()
        layVMainF.addLayout(layHDisplay)
        layVMainF.addLayout(layHGain)
        layVMainF.addLayout(layHButtonsCoeffs1)
        layVMainF.addLayout(layHButtonsCoeffs2)
        # This frame encompasses all UI elements
        frmMain = QFrame(self)
        frmMain.setLayout(layVMainF)

        layVMain = QVBoxLayout()
        layVMain.setAlignment(Qt.AlignTop) # this affects only the first widget (intended here)
        layVMain.addWidget(frmMain)
        layVMain.setContentsMargins(*params['wdg_margins'])
        self.setLayout(layVMain)
        
        #--- set initial values from dict / signal slot connections------------
        self.spnDigits.setValue(params['FMT_pz'])
        self.ledEps.setText(str(self.eps))
        butSettingsClipboard.clicked.connect(self._copy_options)
        
    #------------------------------------------------------------------------------
    def _copy_options(self):
        """
        Set options for copying to/from clipboard or file, storing the selections
        in `params`
        """
        self.opt_widget = CSV_option_box(self) # important: Handle must be class attribute
        #self.opt_widget.show() # modeless dialog, i.e. non-blocking
        self.opt_widget.exec_() # modal dialog (blocking)

#------------------------------------------------------------------------------
if __name__ == '__main__':
    """ Test with python -m pyfda.input_widgets.filter_pz_ui """
    import sys
    from ..compat import QApplication

    app = QApplication(sys.argv)
    mainw = FilterPZ_UI(None)

    app.setActiveWindow(mainw)
    mainw.show()

    sys.exit(app.exec_())
