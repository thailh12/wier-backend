from cache_utils import saved_data
from json_utils import *
from sql_utils import insert_item
import sqlite3

items_keys = list(saved_data['items_dict'].keys())
print(len(items_keys))
conn = sqlite3.connect('shopee.db')
c = conn.cursor()
for item_id, shop_id in items_keys:
    insert_item(c, str(item_id), str(shop_id))

conn.commit()
conn.close()
dump_saved_data()