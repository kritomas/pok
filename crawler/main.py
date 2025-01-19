import dbctl, agent, master

ctl = master.Master()

ctl.start()
ctl.join()

print("Ready")

agents = []
for i in range(8):
	agents.append(agent.Agent(i))
for a in agents:
	a.start()