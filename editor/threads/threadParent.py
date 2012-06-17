
"""
	Defines a parent thread which handles common traits among the threads in the editor
"""

import threading

class ParentThread(threading.Thread):

	def __init__(self, interval = 1):
		threading.Thread.__init__(self)
		self._interval = interval
		self._keepGoing = True


	def setInterval(self, interval):
		"""
		Sets the check interval of the thread
		"""
		self._interval = interval


	def stop(self):
		"""
		Sets the threads _keepGoing flag to False
		"""
		self._keepGoing = False


	def run(self):
		raise "parentThread should never be run! You're doing it wrong!"

