import signal
import config, dbctl, agent, master, activator, deactivator

class SigTermException(Exception):
	pass
def handle_sigterm(signum, frame):
	raise SigTermException("Received SIGTERM signal.")
signal.signal(signal.SIGTERM, handle_sigterm)

act = activator.Activator()
act.start()
act.join()

ctl = master.Master()
ctl.start()

agents = []

for i in range(config.conf["crawler"]["processes"]):
	agents.append(agent.Agent(i))
for a in agents:
	a.start()

def log(what):
	print("Main process: " + what)

try:
	connection = dbctl.DBController()
	while connection.active():
		pass
except KeyboardInterrupt:
	log("Caught SIGINT, terminating")
except SigTermException:
	log("Caught SIGTERM, terminating")
dea = deactivator.Deactivator()
dea.start()
dea.join()
signal.signal(signal.SIGINT, signal.SIG_IGN)
log("Waiting for agents to terminate")
for a in agents:
	a.join()