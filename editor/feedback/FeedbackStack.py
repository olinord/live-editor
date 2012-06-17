import inspect
import code
import re
from FeedbackInterpreter import FeedbackInterpreter

class FeedbackStack(object):

	def __init__(self):
		# linenr -> statement, if a statement is a class or function then it is a linenr -> class or function (nested)
		self._stack = [] 
		self._errors = {}


	def Clear(self):
		self._stack = []
		self._errors = {}


	def GetErrors(self):
		return self._errors


	def GetStack(self):
		return self._stack


	def Populate(self, inputString):

		lines = inputString.split('\n')
		interpreter = FeedbackInterpreter()
		statement = ""
		for lineNr, line in enumerate(lines):
			line  = line + "\n"
			statement += line
			if not interpreter.push(line):
				self._stack.append(FeedbackObject(statement, 0, 0))
	
				if interpreter.error:
					self._errors[lineNr] = interpreter.error

				statement = ""

			
		self._stack.append(FeedbackObject(statement, 0, 0))


class FeedbackObject():

	def __init__(self, statement, lineFrom, lineTo):
		self.statement = statement
		self.lineFrom = lineFrom
		self.lineTo = lineTo

		self.errors = []

	def AddError(self, error):
		self.error.append(error)



