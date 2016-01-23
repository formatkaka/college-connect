import urllib2, os
import codecs
from bs4 import BeautifulSoup
from time import sleep

os.environ['http_proxy']=''

class Scrap:
	url = 'http://svnit.ac.in/'
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
		source = urllib2.urlopen(url)
		soup = BeautifulSoup(source, "html.parser")
		soup.prettify()
		sleep(10)
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
