import multiprocessing, urllib.parse, signal
import requests, bs4, sqlite3
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

	def scannable(self, link):
		if not link:
			return False
		scannable = False

		scannable |=("/zpravy/" in link and not "/foto" in link)

		return scannable

	def processNextLink(self, link):
		next = urllib.parse.urljoin(self.connection.baseUrl(), link)
		if self.scannable(next):
			self.connection.addLink(next)

	def parseSoup(self, soup):
		title = soup.find("meta", attrs={"property":"og:title"})
		if title:
			title = title["content"]

		content = None
		article_body = soup.find("div", attrs={"id":"art-text"})
		if article_body:
			content = "\n".join([p.get_text(strip=True) for p in soup.find("div", attrs={"id":"art-text"}).find_all("p")])

		date = soup.find("meta", attrs={"property":"article:published_time"})
		if date:
			date = date["content"]

		photo_count = len(soup.find_all('img'))


		return {
			"title": title,
			"content": content,
			"date": date,
			"photo_count": photo_count
		}

	def run(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		self.connection = dbctl.DBConnection()
		self.log("Initialized")
		while self.connection.active():
			try:
				currentLink = self.connection.nextLink()
				if currentLink == None:
					currentLink = self.connection.baseUrl()
				if not self.connection.alreadyCrawled(currentLink):
					response = requests.get(currentLink, cookies=_cookies)
					soup = bs4.BeautifulSoup(response.text, "html.parser")
					for next in soup.find_all("a", href=True):
						self.processNextLink(next["href"])
					self.connection.addCrawl(currentLink, response.text, self.parseSoup(soup))
			except sqlite3.IntegrityError as error:
				self.log("SQLite integrity violation: " + str(error))
			except Exception as error:
				self.log("Exception: " + str(error))
		self.log("Terminating")