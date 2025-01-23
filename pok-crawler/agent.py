import multiprocessing, urllib.parse, signal, time
import requests, bs4, sqlite3
import dbctl

ACTIVITY_TIMEOUT = 5

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

		scannable |= (("/zpravy/" in link and not "/foto" in link) or ("_metro-" in link) or ("_ln_") in link)

		return scannable

	def processNextLink(self, link):
		next = urllib.parse.urljoin(self.connection.baseUrl(), link)
		#if self.scannable(next):
		self.connection.addLink(next)
	def processNextLinks(self, links):
		for link in links:
			link = urllib.parse.urljoin(self.connection.baseUrl(), link)
		self.connection.addLinks(links)

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

		category = soup.find("meta", attrs={"name":"cXenseParse:qiw-rubrika"})
		if category:
			category = category["content"]

		comment_count = soup.find("a", attrs={"class": "artsum-btn ico-discusion"})
		if comment_count:
			comment_count = comment_count.find("span")
			comment_count = comment_count.text
			comment_count = int(comment_count.split(" ")[0][1:])

		photo_count = len(soup.find_all('img'))


		return {
			"title": title,
			"content": content,
			"date": date,
			"category": category,
			"comment_count": comment_count,
			"photo_count": photo_count
		}

	def run(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		self.connection = dbctl.DBConnection()
		self.log("Initialized")
		activityTimer = self.connection.active() * ACTIVITY_TIMEOUT
		while activityTimer > 0:
			beginTime = time.time()
			currentLink = self.connection.nextLink()
			if currentLink == None:
				currentLink = self.connection.baseUrl()
			try:
				if not self.connection.alreadyCrawled(currentLink):
					response = requests.get(currentLink, cookies=_cookies)
					soup = bs4.BeautifulSoup(response.text, "lxml")
					rawLinks = soup.find_all("a", href=True)
					nextLinks = [None] * len(rawLinks)
					for index in range(0, len(rawLinks)):
						nextLinks[index] = rawLinks[index]["href"]
					self.processNextLinks(nextLinks)
					self.connection.addCrawl(currentLink, response.text, self.parseSoup(soup))
					#self.connection.addCrawlHtmlOnly(currentLink, response.text)
			except sqlite3.IntegrityError as error:
				self.log("SQLite integrity violation for '" + currentLink + "': " + str(error))
			except Exception as error:
				self.log("Exception: " + str(error))
			activityTimer -= (time.time() - beginTime)
			if activityTimer <= 0:
				activityTimer = self.connection.active() * ACTIVITY_TIMEOUT
		self.log("Terminating")