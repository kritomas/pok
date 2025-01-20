import multiprocessing, signal
import dbctl

class Master(multiprocessing.Process):
	def __init__(self):
		super().__init__()

	def log(self, what):
		print ("Master: " + what)
	def run(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		self.connection = dbctl.DBController()
		self.log("Initialized")