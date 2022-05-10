import logging
import scrapy

from incubator.items import IncubatorItem
from scrapy.http import Request, Response
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from slugify import slugify

class IncubatorSpider(scrapy.Spider):
	name = "incubator"

	starting_url = 'https://incubatorlist.com/'

	def __init__(self, **kw):
		super(IncubatorSpider, self).__init__(**kw)

		self.allowed_domains = ['incubatorlist.com']
		self.link_extractor = LxmlLinkExtractor(unique=True)
		self.cookies_seen = set()

	def start_requests(self):
		urls = [self.starting_url]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = self._get_item(response)
		r = [page]
		r.extend(self._extract_requests(response))
		return r

	def _extract_requests(self, response):
		r = []
		if isinstance(response, Response):
			links = self.link_extractor.extract_links(response)
			r.extend(Request(x.url, callback=self.parse) for x in links)
		return r

	def _get_item(self, response):
		item = IncubatorItem(
			url=response.url,
			size=str(len(response.body)),
			referer=response.request.headers.get('Referer'),
			name="",
			logo="",
			year_founded="",
			mission_vision="",
			website_url="",
			apply_url="",
			program_type="",
			categories="",
			duration="",
			description="",
			city_state="",
			country="",
			type_of_funding="",
			offer="",
			program_fee="",
			offer_details="",
			other_benefits="",
			application_status="",
			application_deadline="",
			of_exits="",
			of_cohorts_year="",
			of_startups_invested="",
			number_of_alumni_startups="",
			total_funding_raised_by_startups="",
			crunchbase_rank="",
			extracted_date="",
			hash="",
		)

		try:
			self._set_content_data(item, response)
		except Exception:
			pass

		# self._set_new_cookies(item, response)

		return item

	def _set_content_data(self, page, response):
		if isinstance(response, Response):
			for i, metadata in enumerate(response.css('.container .row.mb-2')):
				meta_key = metadata.css('.key::text').get()
				meta_values = ""
				meta_values_links = metadata.css('.value a')

				if len(meta_values_links) > 0:
					for j, value in enumerate(meta_values_links):
						meta_values += "%s, " % value.css('a::text').get()
				else:
					meta_values = metadata.css('.value::text').get()

				key = slugify(meta_key, separator='_')
				value = meta_values.rstrip(', ')
				page[key] = value

			for i, button_url in enumerate(response.css('.text-center .text-center a')):
				page["%s_url" % button_url.css('a::text').get().strip().lower()] = button_url.css('a').attrib['href']

			page['name'] = response.css('.title::text').get()
			page['logo'] = "%s%s" % (self.starting_url.rstrip('/'), response.css('.program-thumbnail').attrib['src']) \
   							if 'http' not in response.css('.program-thumbnail').attrib['src'] \
              				else response.css('.program-thumbnail').attrib['src']
			page['year_founded'] = response.css('.founded span.value::text').get()
			page['description'] = response.css('.container .description::text').get()
			page['mission_vision'] = response.css('.text-center .description::text').get()

			logging.debug(page['website_url'])

	def _set_new_cookies(self, page, response):
		cookies = []
		for cookie in [x.split(';', 1)[0] for x in response.headers.getlist('Set-Cookie')]:
			if cookie not in self.cookies_seen:
				self.cookies_seen.add(cookie)
				cookies.append(cookie)
		if cookies:
			page['newcookies'] = cookies
