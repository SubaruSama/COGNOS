import scrapy
from scrapy.http import FormRequest
from cognos.items import CognosItem
from scrapy.loader import ItemLoader

class SinisterLySpiderSpider(scrapy.Spider):
    name = 'sinister_ly_spider'
    allowed_domains = ['sinister.ly']
    start_urls = ['https://sinister.ly/member.php?action=login']

    # 1
    def parse(self, response):
        my_post_key = self.get_my_post_key(response)
        self.logger.info(f'Post key: {my_post_key}')
        username = 'iphenneas'
        password = ''

        return scrapy.FormRequest.from_response(
            response,
            formdata = {
                'my_post_key': my_post_key,
                'username': username,
                'password': password
            },
            callback=self.make_search
        )
    
    # 1.1
    def get_my_post_key(self, response):
        my_post_key = response.xpath('/html/body/div[3]/div[2]/form/input[3]/@value').get()
        
        return my_post_key

    # 3
    def extract_content_from_threads(self, response):
        # extração dos dados e guardar no CognosItem
        pass

    # 2
    def make_search(self, response):
        keywords = ['vulnerability', 'exploit']
        # Juntar start_urls com keyowrds
        # Chamar self.follow_link, que irá retornar um Request para self.make_search quando tiver link para a próxima página
        # follow_link = CSS path que contém o link para a próxima página
        # if follow_link is not None:
        #     chamada recursiva self.make_search
        # callback para self.follow_link para entrar na thread
        # quando entrar na thread, chamar self.parse para extrair os dados
        # quando na thread tiver próxima pagina, chamar self.follow_link e fazer assim até não ter mais next page
        pass
    
    # 2.1
    def follow_link(self, response):
        pass

    # 1.2
    def is_logged_in(self, response):
        # Checar se consegui logar
        pass



