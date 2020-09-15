import os.path
from cache_utils import *
import sqlite3
from sqlite3 import IntegrityError


def insert_execute(c, table, columns, data):
    try:
        c.execute("INSERT INTO "+table+" VALUES (?"+',?' * (len(columns)-1)+")", data)
    except IntegrityError as e:
        # print(e)
        pass

def insert_shop(c, shopid):
    url = 'https://shopee.vn/api/v2/shop/get?shopid='+shopid
    response = get_response(url)
    target = response.json()['data']
    table = 'shops'
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'shopid'
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)

def insert_item(c, itemid, shopid):
    url = 'https://shopee.vn/api/v2/item/get?itemid='+itemid+'&shopid='+shopid
    response = get_response(url)
    target = response.json()['item']
    target.update(target['item_rating'])
    table = 'items'
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    columns[2] = 'shopid'
    insert_shop(c, shopid)
    data = [target[col] if col!='rating_count' else str(target[col]) \
            for col in columns]
    insert_execute(c, table, columns, data)
    for tier_variation in target['tier_variations']:
        insert_tier_variations(c, target, tier_variation)
    parent_cat = None
    for category in target['categories']:
        insert_category(c, target, category, parent_cat)
        parent_cat = category
    for image in target['images']:
        insert_image(c, target, image)
    for video in target['video_info_list']:
        insert_video(c, target, video)
    for attribute in target['attributes']:
        insert_attribute(c, target, attribute)
    if target['bundle_deal_info'] is not None:
        insert_bundle_deal(c, target)

def insert_attribute(c, target, attribute):
    target = target.copy()
    target.update(attribute)

    table = "'items-attributes'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)


def insert_tier_variations(c, target, tier_variations):
    target = target.copy()
    target.update(tier_variations)
    table = "'items-tier_variations'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    for option in target['options']:
        data = [target[col] if col!='option' else option for col in columns]
        insert_execute(c, table, columns, data)

def insert_category(c, target, category, parent_cat):
    target = target.copy()

    cat_id = category['catid']
    url = "https://shopee.vn/api/v2/category/get?catid=" + str(cat_id)
    response = get_response(url)
    if response.json() is None or response.json()['data'] is None:
        return None
    else:
        target_2 = response.json()['data']
    target.update(target_2)
    table = "'categories'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'catid'
    if parent_cat is not None:
        data = [target[col] if col!='parent_id' else parent_cat['catid'] for col in columns]
    else:
        data = [target[col] if col!='parent_id' else None for col in columns]
    insert_execute(c, table, columns, data)

    table = "'items-categories'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    columns[1] = 'catid'
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)

def insert_image(c, target, image):
    table = "'items-images'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    data = [target[col] if col!='image_id' else image for col in columns]
    insert_execute(c, table, columns, data)

def insert_video(c, target, video):
    target = target.copy()
    target.update(video)
    table = "'items-videos'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)

def insert_bundle_deal(c, target):
    target = target.copy()
    target.update(target['bundle_deal_info'])

    table = "'bundle_deal'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)

    table = "'items-bundle_deal'"
    c.execute("SELECT * FROM " + table)
    columns = [description[0] for description in c.description]
    columns[0] = 'itemid'
    data = [target[col] for col in columns]
    insert_execute(c, table, columns, data)