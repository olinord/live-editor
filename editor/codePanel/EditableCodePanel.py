
from CodePanel import CodePanel
from PySide import QtCore

from feedback.PyLintFeedbackStack import Parse

class EditableCodePanel(CodePanel):


	def __init__(self, parent):
		CodePanel.__init__(self, parent)
		self.textArea.textChanged.connect(self.OnTextChanged)


	def ReloadWidget(self):
		CodePanel.ReloadWidget(self)
		self.__class__ = EditableCodePanel


	def OnTextChanged(self):
		print Parse(self.textArea.toPlainText()).read()
