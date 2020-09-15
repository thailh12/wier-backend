import requests
import time
from cache_utils import *
from tqdm.auto import tqdm

def get_items(wd, keywords, page_num, category_id, enable_dump=False):
	global saved_data
	if 'items_dict' not in saved_data:
		saved_data['items_dict'] = {}
	items_dict = saved_data['items_dict']
	items_page_dict = {}
	for keyword in keywords:
		for page in range(page_num):
			id_pairs = get_id_pairs_from_search(wd, keyword, page, category_id, enable_dump)
			for id_pair in tqdm(id_pairs):
				itemid, shopid = id_pair
				if (itemid, shopid) in items_dict.keys():
					pass
				item = get_item(str(itemid), str(shopid), enable_dump)
				item.setdefault('keywords', [])
				if keyword not in item['keywords']:
					item['keywords'].append(keyword)
				items_dict[(itemid, shopid)] = item
				items_page_dict[(itemid, shopid)] = item
			dump_saved_data()
	if enable_dump is False:
		dump_saved_data()
	wd.close()
	return items_page_dict

def get_shop(shopid, enable_dump=True):
    url = 'https://shopee.vn/api/v2/shop/get?shopid='+shopid
    response = get_response(url, enable_dump)
    target = response.json()['data']
    return target

def get_item(itemid, shopid, enable_dump=True):
    url = 'https://shopee.vn/api/v2/item/get?itemid='+itemid+'&shopid='+shopid
    response = get_response(url, enable_dump)
    target = response.json()['item']
    shop = get_shop(shopid, enable_dump)
    data = {
        'item': target,
        'shop': shop
    }
    return data

def get_id_pairs_from_search(wd, keyword, page, category_id=None, enable_dump=True):
    global saved_data
    if 'urls_dict' not in saved_data:
        saved_data['urls_dict'] = {}
    urls_dict = saved_data['urls_dict']
    url="https://shopee.vn/search?keyword="+str(keyword)+"&page="+str(page)
    if category_id:
        url += "&category="+str(category_id)
    if url in urls_dict.keys():
        return urls_dict[url]
    print("New Search Url!!!")
    wd.get(url)
    
    time.sleep(0.5)
    y = wd.execute_script("return window.scrollY;")
    Y = wd.execute_script("return document.body.scrollHeight;")
    while y < Y:
        wd.execute_script("window.scrollTo(0, window.scrollY + 200)")
        time.sleep(0.5)
        y = wd.execute_script("return window.scrollY;")

    items_elems = wd.find_elements_by_xpath('//a[@data-sqe="link"]')
    pairs = []
    for i in items_elems:
        href = i.get_attribute('href')
        try:
            pair = get_id_pair_from_link(href)
            pairs.append(pair)
        except:
            pass
    urls_dict[url] = pairs
    if enable_dump:
        dump_saved_data()
    return pairs

def get_id_pair_from_link(link):
    shopid, itemid = map(int, link.split('i.')[1].split('.'))
    return (itemid, shopid)