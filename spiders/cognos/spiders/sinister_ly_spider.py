import scrapy
from scrapy import Request
from scrapy.http import FormRequest
from cognos.items import CognosItem
from scrapy.loader import ItemLoader
import pytomlpp


class SinisterLySpiderSpider(scrapy.Spider):
    name = 'sinister_ly_spider'
    allowed_domains = ['sinister.ly']
    start_urls = ['https://sinister.ly/member.php?action=login']

    def load_from_toml_file(self):
        with open('../spiders_credentials/credentials.toml') as toml_file:
            return pytomlpp.load(toml_file)

    # 1
    def parse(self, response):
        toml_content = self.load_from_toml_file()
        my_post_key = self.get_my_post_key(response)
        self.logger.info(f'Post key: {my_post_key}')
        # Salvar em um arquivo (dotfile ou toml) separado e não commitar pro github
        # Burner account
        username = toml_content["sinisterly"]["username"]
        password = toml_content["sinisterly"]["password"]

        return FormRequest.from_response(
            response,
            formdata = {
                'my_post_key': my_post_key,
                'username': username,
                'password': password
            },
            callback=self.after_login
        )
    
    # 1.1
    def get_my_post_key(self, response):
        return response.xpath('/html/body/div[3]/div[2]/form/input[3]/@value').get()

    # 1.2
    def after_login(self, response):
        if response.status != 200:
            self.logger.error('Erro ao logar.')
            return
        else:
            yield Request(url=f'https://{self.allowed_domains[0]}/search.php', callback=self.make_search)
        # Checar se consegui logar
        # Fazer um login errado para ver o que retorna

    # 2
    def make_search(self, response):
        self.logger.info('I am here')
        keywords = ['vulnerability', 'exploit']
        search_url = response.request.url
        #search_url = f'https://{self.allowed_domains[0]}/search.php'

        for keyword in keywords:
            return FormRequest(
                url=search_url,
                formdata={
                    'action': 'do_search',
                    'keywords': keyword,
                    'postthread': '1',
                    'matchusername': '1',
                    'forum[]': 'all',
                    'findthreadst': '1',
                    'postdate': '0',
                    'pddir': '1',
                    'threadprefix[]': 'any',
                    'sortby': 'lastpost',
                    'sortordr': 'desc',
                    'showresults': 'threads',
                    'submit': 'Search'
                },
                callback=self.extract_URL_from_search
            )
        # Juntar start_urls com keyowrds
        # Chamar self.follow_link, que irá retornar um Request para self.make_search quando tiver link para a próxima página
        # follow_link = CSS path que contém o link para a próxima página
        # if follow_link is not None:
        #     chamada recursiva self.make_search
        # callback para self.follow_link para entrar na thread
        # quando entrar na thread, chamar self.parse para extrair os dados
        # quando na thread tiver próxima pagina, chamar self.follow_link e fazer assim até não ter mais next page
    
    # 2.1
    def follow_link_next_page(self, response):
        pass

    # 2.2
    def extract_URL_from_search(self, response):
        css_thread_post_pattern = 'tr.inline_row:nth-child(n) > td:nth-child(n) > div:nth-child(n) > span:nth-child(n) > a:nth-child(n)::attr(href)' # usar selector para fazer genérico, ir de post em post
        # Como cada href é apenas o path, preciso pegar o path e montar junto com o domínio para enviar para extrair os dados
        paths = response.selector.css(css_thread_post_pattern).getall()

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        for path in paths:
            yield Request(
                url='https://{allowed_domains}/{path}'.format(allowed_domains=self.allowed_domains[0],
                path=path
                ),
                callback=self.extract_content_from_threads
            )

        xpath_next_page_pattern = '/html/body/div[3]/div[2]/table[3]/tr/td[1]/div/a[6]/@href'
        xpath_next_page_link = response.xpath(xpath_next_page_pattern).get()

        if xpath_next_page_link is not None:
            yield response.follow(xpath_next_page_link, callback=self.extract_URL_from_search)

    # 3
    def extract_content_from_threads(self, response):
        # extração dos dados e guardar no CognosItem
        self.logger.info('----------- Title: %s -----------', response.xpath('/html/head/title/text()').get())
        contents = response.selector.xpath('//*[@id="posts"]/div[*]')

        # test
        print(response)

        for content in contents:
            loader = ItemLoader(item=CognosItem(), selector=content)

            # TODO
            loader.add_xpath('title', '/html/head/title')
            loader.add_xpath('username', '//*[@id="posts"]/div[*]/div[1]/div[2]/strong/span/a/span')
            # loader.add_xpath('reputation', '')
            loader.add_xpath('info_date_post', '//*[@id="posts"]/div[*]/div[2]/div[1]/span[2]/span')
            loader.add_xpath('post_content', '//*[@id="posts"]/div[*]/div[2]/div[2]')

        yield loader.load_item()
