import multiprocessing, signal, os
import dbctl, config

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
		while self.connection.active():
			try:
				if os.path.getsize(dbctl.DB_PATH) > config.conf["crawler"]["critical_db_size"]:
					self.log("Critical size reached")
					self.connection.deactivate()
			except Exception as error:
				self.log("Exception: " + str(error))
		self.log("Terminating")