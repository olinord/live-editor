# Python Module Reloader
#
# Copyright (c) 2009, 2010 Jon Parise <jon@indelible.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import imp
import os
try:
    import queue
except ImportError:
    #python 2.x
    import Queue as queue
import reloader
import sys
import threading
import time

_win32 = (sys.platform == 'win32')

class ModuleMonitor(threading.Thread):
    """Monitor module source file changes"""

    def __init__(self, interval=1):
        threading.Thread.__init__(self)
        self.daemon = True
        self.mtimes = {}
        self.queue = queue.Queue()
        self.interval = interval


    def run(self):
        while True:
            self._scan()
            time.sleep(self.interval)

    def _scan(self):
        # We're only interested in file-based modules (not C extensions).
        modules = [m.__file__ for m in sys.modules.values()
                if m and '__file__' in m.__dict__ ]
        #and m.__file__.startswith(r'/Users/olinord/Desktop/Programming/PyEdit/editor/codePanel/EditableCodePanel.py')
        for filename in modules:
            # We're only interested in the source .py files.
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                filename = filename[:-1]

            # stat() the file.  This might fail if the module is part of a
            # bundle (.egg).  We simply skip those modules because they're
            # not really reloadable anyway.
            try:
                stat = os.stat(filename)
            except OSError:
                continue
            
            # Check the modification time.  We need to adjust on Windows.
            mtime = stat.st_mtime
            if _win32:
                mtime -= stat.st_ctime

            # Check if we've seen this file before.  We don't need to do
            # anything for new files.
            if filename in self.mtimes:
                # If this file's mtime has changed, queue it for reload.
                if mtime > self.mtimes[filename]:
                    modules = [m for m in sys.modules.values() if getattr(m, '__file__', None) == filename]
                    self.queue.put(filename)

            # Record this filename's current mtime.
            self.mtimes[filename] = mtime


class Reloader(object):

    def __init__(self, interval=1):
        self.monitor = ModuleMonitor(interval=interval)
        self.monitor.start()


    def poll(self):
        filenames = []
        while not self.monitor.queue.empty():
            try:
                filenames.append(self.monitor.queue.get_nowait())
            except queue.Empty:
                break
        if len(filenames) > 0:
            self._reload(filenames)


    def _reload(self, filenames):
        modules = [m for m in sys.modules.values()
                if getattr(m, '__file__', None) in filenames]

        for mod in modules:
            reloader.reload(mod)
