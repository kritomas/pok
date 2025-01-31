import multiprocessing, signal, time
import dbctl

class Activator(multiprocessing.Process):
	def __init__(self):
		super().__init__()

	def log(self, what):
		print ("Activator: " + what)

	def run(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		self.connection = dbctl.DBController()
		while not self.connection.active():
			self.connection.activate()
			time.sleep(0.1)
		self.log("DB ready for agents")