# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class IncubatorItem(Item):
	name = Field()
	logo = Field()
	year_founded = Field()
	mission_vision = Field()
	website_url = Field()
	apply_url = Field()
	program_type = Field()
	categories = Field()
	duration = Field()
	description = Field()
	city_state = Field()
	country = Field()
	type_of_funding = Field()
	offer = Field()
	program_fee = Field()
	offer_details = Field()
	other_benefits = Field()
	application_status = Field()
	application_deadline = Field()
	of_exits = Field()
	of_cohorts_year = Field()
	of_startups_invested = Field()
	number_of_alumni_startups = Field()
	total_funding_raised_by_startups = Field()
	crunchbase_rank = Field()
	extracted_date = Field()
	url = Field()
	referer = Field()
	size = Field()
	hash = Field()
