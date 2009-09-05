import asynchat
import sys, traceback

from PodSix.UniversalJSONEncoder import *

class Channel(asynchat.async_chat):
	def __init__(self, conn=None, addr=(), server=None):
		asynchat.async_chat.__init__(self, conn=conn)
		self.addr = addr
		self._server = server
		self._ibuffer = ""
		self.set_terminator("\0")
	
	def collect_incoming_data(self, data):
		self._ibuffer += data
	
	def found_terminator(self):
		data = loads(self._ibuffer)
		self._ibuffer = ""
		
		if type(dict()) == type(data) and data.has_key('action'):
			method = getattr(self, 'Network_' + data['action'], None)
			if method:
				method(data)
			method = getattr(self, 'Network', None)
			if method:
				method(data)
		else:
			print "OOB data:", data
	
	def Send(self, data):
		asynchat.async_chat.push(self, dumps(data, cls=UniversalJSONEncoder) + "\0")
	
	def handle_connect(self):
		if hasattr(self, "Connected"):
			self.Connected()
		else:
			print "Unhandled Connected()"
	
	def handle_error(self):
		try:
			self.close()
		except:
			pass
		if hasattr(self, "Error"):
			self.Error(sys.exc_info()[1])
		else:
			asynchat.async_chat.handle_error(self)
	
	def handle_expt(self):
		pass
	
	def handle_close(self):
		if hasattr(self, "Close"):
			self.Close()
		asynchat.async_chat.handle_close(self)

