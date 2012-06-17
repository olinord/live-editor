
from pylint import lint
from pylint.reporters.text import TextReporter
import os.path

tmp_file = r'__tmp__'

class WritableObject(object):
	def __init__(self):
		self.content = []
	def write(self, st):
		"dummy write"
		self.content.append(st)
	def read(self):
		"dummy read"
		return self.content

def Parse(script):
	global tmp_file

	with open(tmp_file, 'w') as tmpFile:
		tmpFile.write(script)
		tmpFile.close()

	ARGS = ["-r","n", "--rcfile=rcpylint"]  # put your own here
	pylint_output = WritableObject()
	lint.Run([tmp_file]+ARGS, reporter=TextReporter(pylint_output), exit=False)

	return pylint_output
	