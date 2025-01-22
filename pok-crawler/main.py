import signal, gc
import config, dbctl, agent, master, activator, deactivator

class SigTermException(Exception):
	pass
def handle_sigterm(signum, frame):
	raise SigTermException("Received SIGTERM signal.")
signal.signal(signal.SIGTERM, handle_sigterm)

act = activator.Activator()
act.start()
act.join()

m = master.Master()
m.start()

agents = []

for i in range(config.conf["crawler"]["agents"]):
	agents.append(agent.Agent(i))
for a in agents:
	a.start()

def log(what):
	print("Main process: " + what)

try:
	connection = dbctl.DBController()
	while connection.active():
		time.sleep(1)
except KeyboardInterrupt:
	log("Caught SIGINT, terminating")
except SigTermException:
	log("Caught SIGTERM, terminating")
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
del connection
gc.collect()
dea = deactivator.Deactivator()
dea.start()
dea.join()
log("Waiting for agents to terminate")
for a in agents:
	a.join()
m.join()