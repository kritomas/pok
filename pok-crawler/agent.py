import multiprocessing, urllib.parse, signal, time
import requests, sqlite3
from lxml import html
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
		filtered = [urllib.parse.urljoin(self.connection.baseUrl(), link) for link in links if self.scannable(urllib.parse.urljoin(self.connection.baseUrl(), link))]
		self.connection.addLinks(filtered)
		#for link in links:
		#	link = urllib.parse.urljoin(self.connection.baseUrl(), link)
		#self.connection.addLinks(links)

	def parseTree(self, tree):
		# Extract the title
		title_meta = tree.xpath('//meta[@property="og:title"]/@content')
		title = title_meta[0] if title_meta else None

		# Extract the content
		article_body = tree.xpath('//div[@id="art-text"]')
		content = None
		if article_body:
			paragraphs = article_body[0].xpath('.//p/text()')
			content = "\n".join([p.strip() for p in paragraphs])

		# Extract the publication date
		date_meta = tree.xpath('//meta[@property="article:published_time"]/@content')
		date = date_meta[0] if date_meta else None

		# Extract the category
		category_meta = tree.xpath('//meta[@name="cXenseParse:qiw-rubrika"]/@content')
		category = category_meta[0] if category_meta else None

		# Extract the comment count
		comment_count_elem = tree.xpath('//a[@class="artsum-btn ico-discusion"]/span')
		comment_count = None
		if comment_count_elem:
			comment_count_text = comment_count_elem[0].text
			comment_count = int(comment_count_text.split(" ")[0][1:])

		# Count the number of images
		photo_count = len(tree.xpath('//img'))

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
					tree = html.fromstring(response.text)
					rawLinks = tree.xpath('//a[@href]')
					nextLinks = [link.get('href') for link in rawLinks]
					self.processNextLinks(nextLinks)
					self.connection.addCrawl(currentLink, response.text, self.parseTree(tree))
					#self.connection.addCrawlHtmlOnly(currentLink, response.text)
			except sqlite3.IntegrityError as error:
				self.log("SQLite integrity violation for '" + currentLink + "': " + str(error))
			except Exception as error:
				self.log("Exception: " + str(error))
			activityTimer -= (time.time() - beginTime)
			if activityTimer <= 0:
				activityTimer = self.connection.active() * ACTIVITY_TIMEOUT
		self.log("Terminating")