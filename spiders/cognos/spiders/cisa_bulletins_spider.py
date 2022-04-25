import scrapy


class ScrapeTableSpider(scrapy.Spider):
    name = 'cisa_bulletin'
    allowed_domains = ['cisa.gov']
    start_urls = ['https://www.cisa.gov/uscert/ncas/bulletins/sb22-080']


    def start_requests(self):
        urls = [
            'https://www.cisa.gov/uscert/ncas/bulletins/sb22-080',
            'https://www.cisa.gov/uscert/ncas/bulletins/sb22-073',
            'https://www.cisa.gov/uscert/ncas/bulletins/sb22-066'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table = response.xpath('//*[@class="field field--name-body field--type-text-with-summary field--label-hidden field--item"]//tbody//tr')
        for row in table:
            yield {
                'Primary Vendor -- Product': row.xpath('td[1]//text()').extract(),
                'Descritption': row.xpath('td[2]//text()').extract(),
                'Date published': row.xpath('td[3]//text()').extract(),
                'CVSS Score': row.xpath('td[4]//text()').extract(),
                'Source and Patch info': row.xpath('td[5]//text()').extract()
            }