import multiprocessing, urllib.parse
import requests, bs4
import dbctl

_cookies = {
	"dCMP": "mafra=1111,all=1,reklama=1,part=0,cpex=1,google=1,gemius=1,id5=1,next=0000,onlajny=0000,jenzeny=0000,"
	"databazeknih=0000,autojournal=0000,skodahome=0000,skodaklasik=0000,groupm=1,piano=1,seznam=1,geozo=0,"
	"czaid=1,click=1,verze=2,"
}

class Agent(multiprocessing.Process):
	def __init__(self, agent_id):
		super().__init__()
		self._agent_id = agent_id

	def log(self, what):
		print ("Agent " + str(self._agent_id) + ": " + what)

	def processNextLink(self, link):
		next = urllib.parse.urljoin(self.connection.baseUrl(), link)
		self.connection.addLink(next)

	def run(self):
		self.connection = dbctl.DBConnection()
		self.log("Initialized")
		currentLink = self.connection.nextLink()
		while currentLink != None:
			if not self.connection.alreadyCrawled(currentLink):
				response = requests.get(currentLink, cookies=_cookies)
				self.connection.addCrawl(currentLink, response)
				soup = bs4.BeautifulSoup(response)
				for next in soup.find_all("a", href=True):
					self.processNextLink(next["href"])

			currentLink = self.connection.nextLink(currentLink)