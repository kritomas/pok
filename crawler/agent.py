import multiprocessing
import dbctl

class Agent(multiprocessing.Process):
	def __init__(self, agent_id):
		super().__init__()
		self._agent_id = agent_id

	def log(self, what):
		print ("Agent " + str(self._agent_id) + ": " + what)
	def run(self):
		self.connection = dbctl.DBConnection()
		self.log("Initialized")