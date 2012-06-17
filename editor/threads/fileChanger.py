"""
	Defines the FileChanger thread
"""

import reloader.monitor
from threadParent import ParentThread
import time


class FileChanger(ParentThread):

	"""
		A thread which polls the file reloader
	"""

	def __init__(self):
		ParentThread.__init__(self)
		self.fileReloader = reloader.monitor.Reloader()


	def run(self):
		"""
		Polls the fileReloader
		And sleeps for self._interval seconds
		"""
		while(self._keepGoing):
			self.fileReloader.poll()
			time.sleep(self._interval)
