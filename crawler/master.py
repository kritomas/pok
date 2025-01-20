import multiprocessing
import dbctl

class Master(multiprocessing.Process):
	def __init__(self):
		super().__init__()

	def log(self, what):
		print ("Master: " + what)
	def run(self):
		self.connection = dbctl.DBController()
		self.connection.activate()
		self.log("Initialized")