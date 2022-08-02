import scrapy


class SinisterLySpiderSpider(scrapy.Spider):
    name = 'sinister_ly_spider'
    allowed_domains = ['sinister.ly']
    start_urls = ['http://sinister.ly/']
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    # Preciso estar logado para procurar as coisas
    # Gerar o token de sessão e passar por aqui; como? ler no código do onionjuicer
    def login(self):
        pass

    def make_search(self):
        keywords = ['vulnerability', 'exploit']
        # Juntar start_urls com keyowrds
        pass

    # 1
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.extract_URL_from_forumdisplay)

    def parse(self, response):
        pass
