import scrapy


class SinisterLySpiderSpider(scrapy.Spider):
    name = 'sinister_ly_spider'
    allowed_domains = ['sinister.ly']
    start_urls = ['http://sinister.ly/']
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    # Preciso estar logado para procurar as coisas; nome do cookie: mybbuser
    # Gerar o token de sessão e passar por aqui; como? ler no código do onionjuicer
    # 1
    def login(self):
        pass

    # 3
    def make_search(self):
        keywords = ['vulnerability', 'exploit']
        # Juntar start_urls com keyowrds
        # Seguir quando tiver link para a próxima página
        # follow_link = CSS path que contém o link para a próxima página
        # if follow_link is not None:
        #     chamada recursiva self.make_search
        pass

    # 2
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.make_search)

    # 4
    def parse(self, response):
        pass
