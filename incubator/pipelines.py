# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib, re, csv, os

from bs4 import BeautifulSoup
from datetime import datetime
from itemadapter import ItemAdapter
from openpyxl import Workbook
from scrapy.exceptions import DropItem

class IncubatorPipeline:
	def process_item(self, item, spider):
		try:
			if item['name'] == None or item['name'] == '':
				raise DropItem(item['url'])
		except KeyError:
			raise DropItem(item['url'])
		item['hash'] = hashlib.md5(item['url'].encode('UTF-8')).hexdigest()
		item['extracted_date'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return item

class CleanHTML:
	def process_item(self, item, spider):
		for key in item:
			try:
				item[key] = self._sanitize_html(item[key]).strip()
			except TypeError:
				pass

		return item

	def _sanitize_html(self, html):
		pattern = re.compile(r"<!\s*--(.*?)(--\s*\>)", re.DOTALL | re.MULTILINE | re.IGNORECASE)
		soup = BeautifulSoup(html, 'lxml')

		for tag in soup.findAll(True):
			tag.hidden = True

		content = soup.renderContents()

		return pattern.sub('', content)

class ExportToCSV:
	def process_item(self, item, spider):
		file_path = "export/%s.csv" % datetime.now().strftime("%Y%m%d%H")
		file_size = os.stat(file_path).st_size if os.path.exists(file_path) else 0

		items = {}
		for key in item:
			if key not in ['referer', 'size', 'hash']:
				items[key] = '' if item[key] == None else item[key]

		f = open(file_path, 'a' if os.path.exists(file_path) else 'w')
		writer = csv.writer(f)
		if file_size == 0:
			writer.writerow(items.keys())
		writer.writerow(items.values())

		return item
