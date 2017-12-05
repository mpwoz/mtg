# -*- coding: utf-8 -*-
import scrapy


class DirectorySpider(scrapy.Spider):
    name = 'directory'

    sets = ['xln', 'hou']
    start_urls = map(lambda s: 'http://magiccards.info/{0}/en.html'.format(s), sets)

    def parse(self, response):
        """ Main parsing method, given a set listing, find the card detail pages and parse them """

        # The only table with a 'th' is the card directory.
        card_listing = response.xpath("//th/ancestor::table[1]")

        # Get all links inside that table
        # Call the detail page parser for each card we've found
        limit = 15
        for a in card_listing.xpath('.//a')[:limit]:
            yield response.follow(a, self.parse_detail)

    def parse_detail(self, response):
        """ Parse a single card's detail page, getting relevant data for that card. """

        # Extract the image with a 'scans' in the src attribute. This is the card image.
        card_image = response.xpath("//img[contains(@src, 'scans')]/@src").extract_first()

        # There's only one 'i' element on the page and it contains the flavor text of the card
        flavor = response.xpath('//i/text()').extract_first()

        item = {
            'image': card_image,
            'flavor': flavor
        }
        yield item



