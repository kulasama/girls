#coding:utf8
from pony.orm import *

db = Database('mysql', host='127.0.0.1', user='root', passwd='', db='girls')

class Girl(db.Entity):
    name = Required(unicode)
    twitter = Required(unicode)


class Photo(db.Entity):
    uid = Required(int)
    link = Required(unicode)
    local = Optional(unicode)
   



if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
