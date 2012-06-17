
from PySide import QtGui, QtCore

class ReloadableQWidget(QtGui.QWidget):

	"""defines a reloadable qt widget"""
	
	reloadWidget = QtCore.Signal()

	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.reloadWidget.connect(self.ReloadWidget)


	def ReloadInstance(self):
		self.reloadWidget.emit()


	def ReloadWidget(self, newClass):
		pass