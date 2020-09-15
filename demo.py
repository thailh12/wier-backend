from json_utils import *
from selenium_utils import *
from sql_utils import insert_item
import sqlite3

wd = get_webdriver()
category_id = 78 # thoi trang nu
search_terms = ['vay', 'quan', 'ao', 'phu kien']
# search_terms = ['vay']
items = get_items(wd, search_terms, 5, category_id)
item_id_0, shop_id_0 = next(iter(items))
print(item_id_0, shop_id_0)
print(items[(item_id_0, shop_id_0)].keys())

#conn = sqlite3.connect('shopee.db')
#c = conn.cursor()
#insert_item(c, item_id_0, shop_id_0)
#conn.commit()
#conn.close()