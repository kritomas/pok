import multiprocessing, signal
import dbctl

class Deactivator(multiprocessing.Process):
	def __init__(self):
		super().__init__()

	def log(self, what):
		print ("Deactivator: " + what)

	def run(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		self.connection = dbctl.DBController()
		self.connection.deactivate()
		self.log("DB closed, agents terminating")