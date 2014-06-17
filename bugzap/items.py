# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.item import Item, Field

class Bug(Item):
    id = Field(output_processor=TakeFirst())
    url = Field()
    product = Field(output_processor=TakeFirst())
    component = Field(output_processor=TakeFirst())
    status = Field(output_processor=TakeFirst())
    assignee = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    comments = Field()

class Comment(Item):
    commenter = Field(output_processor=TakeFirst())
    body = Field(output_processor=TakeFirst())
