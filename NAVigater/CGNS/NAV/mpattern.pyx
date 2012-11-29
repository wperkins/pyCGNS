#  -------------------------------------------------------------------------
#  pyCGNS.NAV - Python package for CFD General Notation System - NAVigater
#  See license.txt file in the root directory of this Python module source  
#  -------------------------------------------------------------------------
#  $Release$
#  -------------------------------------------------------------------------

from PySide.QtCore    import *
from PySide.QtGui     import *

COPYPATTERN='@@COPYPATTERN@@'

KEYMAPPING={
 COPYPATTERN:   Qt.Key_Space,
}

# -----------------------------------------------------------------
class Q7PatternTableWidget(QTableWidget):
    def mousePressEvent(self,event):
        self.lastPos=event.globalPos()
        self.lastButton=event.button()
        QTableWidget.mousePressEvent(self,event)
    def keyPressEvent(self,event):
        kmod=event.modifiers()
        kval=event.key()
        if (kval==KEYMAPPING[COPYPATTERN]):
            self._panel.copyPatternInBuffer()
            return
        QTableWidget.keyPressEvent(self,event)
       
# -----------------------------------------------------------------
