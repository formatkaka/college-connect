import os
import codecs
from bs4 import BeautifulSoup
from time import sleep

os.environ['http_proxy']=''
os.environ['https_proxy']=''
os.environ['no_proxy']='svnit.ac.in'

import urllib2, requests

class Scrap:
	url = 'http://svnit.ac.in:80/'
	home = url + 'home.php'
	index = url + 'index.php'

	def get_url(self, div, tag, field, url=''):
		dict = {}
		for link in div.find_all(tag):
			text = link.text
			path = url + link.get(field)
			if text and path:
				dict[text] = path
		return dict

	def get_soup(self, url):
		# proxy = urllib2.ProxyHandler()
		# opener = urllib2.build_opener(proxy)
		# urllib2.install_opener(opener)
		session = requests.Session()
		session.trust_env = False
		limit = 0
		while limit < 3:
			try:
				source = requests.get(url).text
			except (exceptions.ConnectionError, exceptions.HTTPError, exceptions.Timeout):
				raise "Error"
				break
			limit = limit + 1
		soup = BeautifulSoup(source, "html.parser")
		soup.prettify()
		sleep(2)
		return soup

	def get_notice(self):
		home_soup = self.get_soup(self.home)
		notices_div = home_soup.find("div", {"id": "mysagscroller5"})
		notices = self.get_url(notices_div, 'a', 'href', self.url)
		return notices

	def get_seminar(self):
		home_soup = self.get_soup(self.home)
		seminar_div = home_soup.find("div", {"id": "mysagscroller"})
		seminars = self.get_url(seminar_div, 'a', 'href', self.url)
		return seminars

	def get_quicks(self):
		index_soup = self.get_soup(self.index)
		quick_div = index_soup.find("select", {"name": "quicklinks"})
		quicks = self.get_url(quick_div, 'option', 'value')
		return quicks
