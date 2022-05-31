# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
from w3lib import html

class CognosPipeline:
    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + '\n'
        if self.file.writable():
            self.file.write(line)
        return item

    def open_spider(self, spider):
        # Criar um arquivo JSON para salvar os dados
        # TODO: salvar num sqlite ou postgres para deixar mais profissional
        self.file = open('dataset.json', 'w')

    def close_spider(self, spider):
        # Fechar o arquivo JSON
        # TODO: fechar a conexão com o banco
        self.file.close()