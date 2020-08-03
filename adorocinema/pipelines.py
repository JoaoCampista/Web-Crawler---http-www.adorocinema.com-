# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class AdorocinemaPipeline(object):
    def open_spider(self, movie_review):
        self.file = open('items.json', 'w', encoding='utf-8')
        self.file.write('[ \n')

    def close_spider(self, movie_review):
        self.file.close()

    def process_item(self, item, movie_review):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ", \n"
        self.file.write(line)
        return item
