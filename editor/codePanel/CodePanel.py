
"""
Defines a panel which contains a code

This panel is inherited from by the EditableCodePanel and the LiveFeedbackCodePanel
"""

from PySide import QtGui, QtCore
from util.ReloadableQWidget import ReloadableQWidget
import PythonHighlighter 

class CodePanel(ReloadableQWidget):

	def __init__(self, parent):
		ReloadableQWidget.__init__(self)
		self.parent = parent
		self.setParent(parent)
		self.hbox = QtGui.QHBoxLayout(self)
		self.setLayout(self.hbox)
		self.SetupUi()

		self.show()


	def ReloadWidget(self):
		self.__class__ = CodePanel
		self.layout().removeWidget(self.textArea)
		self.textArea.setParent(None)
		self.textArea.deleteLater()

		oldText = self.textArea.toPlainText()

		#print self.textArea
		self.SetupUi()
		self.textArea.show()
		self.show()
		#print self.textArea
		self.textArea.setPlainText(oldText)

	def SetupUi(self):

		self.textArea = QtGui.QPlainTextEdit(self)
		self.textArea.setFont (QtGui.QFont ("Courier", 15))
		self.textArea.setTabStopWidth(24)
		self.textArea.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)

		highlighter = PythonHighlighter.PythonHighlighter(self.textArea.document())
		
		self.layout().addWidget(self.textArea)

