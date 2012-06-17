
import sys
import os

libraryPath = os.path.join(os.path.dirname(__file__), "lib")
sys.path.append(libraryPath)

from reloader import reloader 
reloader.enable()

from threads.fileChanger import FileChanger

from PySide import QtGui, QtCore

from codePanel.EditableCodePanel import EditableCodePanel
import exceptions

editor = None

class LiveEditorWidget(QtGui.QWidget):

	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.initUI()


	def Reload(self):
		oldText = self.codePanel.textArea.toPlainText()

		self.close()
		self.initUI()

		self.codePanel.textArea.SetPlainText(oldText)


	def initUI(self):
		self.codePanel = EditableCodePanel(self)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.codePanel)

		self.setLayout(hbox)
		self.show()


	"""def UpdateFeedback( self ):
		self.feedbackPanel.setPlainText( self.textEditor.toPlainText())

		self._feedbackStack.Clear()
		self._feedbackStack.Populate( self.textEditor.toPlainText())
		lines = self.textEditor.toPlainText().split("\n")
		extraSelections = []

		errorColor = QtGui.QColor(QtCore.Qt.red).lighter(160)

		# highlight the errors
		for eachLine, parseException in self._feedbackStack.GetErrors().iteritems():
			sel = QtGui.QTextEdit.ExtraSelection()
			sel.format.setForeground(errorColor)
			sel.cursor = QtGui.QTextCursor(self.feedbackPanel.document())
			if type(parseException) == exceptions.SyntaxError:
				sel.cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveMode.MoveAnchor, n=eachLine)
				sel.cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.MoveMode.MoveAnchor, n = parseException.offset)
				sel.cursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.MoveMode.KeepAnchor, n = len(parseException.text))
			else:
				sel.cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveMode.MoveAnchor, n=eachLine)
				sel.cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.MoveMode.KeepAnchor, n = len(lines[eachLine]))
				
			extraSelections.append(sel)

		self.feedbackPanel.setExtraSelections(extraSelections)
	"""

class LiveEditor(QtGui.QMainWindow):
	
	instance = None

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.initUI()
		

	def initUI(self):               
		
		self.resize(QtCore.QSize(800, 600))
		self.statusBar().showMessage('Ready')

		self.setCentralWidget(LiveEditorWidget())

class EditorApp(QtGui.QApplication):

	threads = []
	def __init__(self, argv):
		QtGui.QApplication.__init__(self, argv)

		EditorApp.threads.append( FileChanger() )

		for eachThread in EditorApp.threads:
			eachThread.start()

		styleSheetFile = QtCore.QFile("css/EditorStyle.css")
		styleSheetFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)

		css = QtCore.QTextStream(styleSheetFile)

		self.setStyleSheet(css.readAll())
		editor = LiveEditor()
		editor.show()
		self.exec_()

if __name__ == '__main__':
	app = EditorApp(sys.argv)
	
	for eachThread in EditorApp.threads:
		eachThread.stop()

	sys.exit()
		
