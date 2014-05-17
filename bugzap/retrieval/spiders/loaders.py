__author__ = 'fcanas'
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.utils.markup import remove_entities
from scrapy.utils.python import unicode_to_str
import nltk

class BugLoader(ItemLoader):
    default_input_processor = MapCompose(nltk.clean_html)

class CommentsLoader(ItemLoader):
    default_input_processor = MapCompose(nltk.clean_html)

