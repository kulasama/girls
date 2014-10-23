#coding:utf8
import requests
import time
from pyquery import PyQuery as pq
import unittest
import re
from pony.orm import *
from models import Girl,Photo,db
import os





def crawl_photo(avator):
    print avator
    basename = os.path.basename(avator)
    filename = os.path.join("media",basename)
    r = requests.get(avator)
    f = open(filename,"wb")
    f.write(r.content)
    f.close()
    return filename



class Bot(object):

    def crawl(self,current_page = 1):
        url = "http://jigadori.fkoji.com/?p=%d" % current_page
        print "parse %s" % url
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
        }


        r = requests.get(url,headers=headers)
        self.content = r.content
        return r.content

    def parse(self):
        d = pq(self.content)
        icontent = d(".photo")
        for item in icontent:
            self.parse_item(item)

    def parse_item(self,item):
        name = item.xpath("div[@class='user-info']/h3/a")[0].text
        twitter = item.xpath("div[@class='user-info']/h3/span/a")[0].text
  

        avators = item.xpath("div[@class='photo-link-outer']/a/img//@src")

        with db_session:
            girl = Girl.get(twitter=twitter)
            if girl is None:
                girl = Girl(name=name,twitter=twitter)
            else:
                girl.name = name
            commit()
            for avator in avators:
                photo = Photo.get(link=avator)
                if photo is None:
                    try:
                        local = crawl_photo(avator)
                        photo = Photo(uid=girl.id,link=avator,local=local)
                        commit()
                    except requests.exceptions.ConnectionError:
                        pass



  

    def do(self):
        for i in xrange(21,1302):
            self.crawl(i)
            self.parse()
            time.sleep(0.5)



class BotTestCase(unittest.TestCase):

    def test_ok(self):
        avator = "http://pbs.twimg.com/media/By83pn0CQAA_yUZ.jpg"
        crawl_photo(avator)



if __name__ == "__main__":

    #unittest.main()
    db.generate_mapping(create_tables=True)
    bot = Bot()
    bot.do()
