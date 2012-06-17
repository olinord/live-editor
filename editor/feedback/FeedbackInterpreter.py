import code
import sys
import traceback

class FeedbackInterpreter(code.InteractiveConsole):

	def __init__(self):
		code.InteractiveConsole.__init__(self)
		self.error = None


	def showsyntaxerror(self, filename=None):
		"""
		Stores the syntax error object in the self.error variable
		"""
		self.error = sys.exc_info()[1]
		

	def showtraceback(self):
		"""
		Stores the exception object in the self.error variable
		"""
		self.error = sys.exc_info()[1]
		
