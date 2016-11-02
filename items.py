# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
from scrapy.item import Item, Field


def room_serialize(content):
    res = ""
    if len(content) == 0:
        return res
    expbr = re.compile(r'\d+br')
    bed = expbr.search(content[0])
    if bed is not None:
        res = bed.group(0)[:-2]
    return res


def area_serialize(content):
    res = ""
    if len(content) == 0:
        return res
    expft = re.compile(r'\d+ft')
    ft = expft.search(content[0])
    if ft is not None:
        res = ft.group(0)
    return res


class CraigslistItem(Item):
    datetime = Field()
    price = Field()
    location = Field()
    room = Field(serializer=room_serialize)
    area = Field(serializer=area_serialize)
