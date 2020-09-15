from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
import datetime
import time

es=Elasticsearch([{'host':'localhost','port':9200}])

def search_view(es_results):
    results = []
    for i in es_results:
        t = {}
        t['item_itemid'] = i['_source']['item_itemid']
        t['item_name'] = i['_source']['item_name']
        t['item_description'] = i['_source']['item_description']
        t['item_price'] = int(i['_source']['item_price'] / 100000)
        t['item_ctime'] = datetime.datetime.fromtimestamp(\
        i['_source']['item_ctime']).isoformat()
        t['item_sold'] = i['_source']['item_sold']
        results.append(t)
    if not results:
        return "No results!!"
    else:
        r = ""
        for i in results:
            d = ""
            for k in i:
                d += str(k) + " : " + str(i[k]) + "</br>"
            r += "<div><p>" + d + "</p></div>"
        return r

def search(query, order=None, maxPrice=None, minPrice=None, sortBy=None, page=None):
    s = Search(using=es, index="shopee")
    q = Q("multi_match", query=query, fields=['item_name', 'item_name.folded'])
    s = s.query(q)
    if sortBy=='ctime':
        s = s.sort({"item_ctime" : {"order" : "desc"}})
    elif sortBy=='sales':
        s = s.sort({"item_sold" : {"order" : "desc"}})
    elif sortBy=='price' and order!="desc":
        s = s.sort({"item_price" : {"order" : "asc"}})
    elif sortBy=='price' and order=="desc":
        s = s.sort({"item_price" : {"order" : "desc"}})
    item_price={}
    if minPrice: 
        minPrice = int(minPrice) * 100000
        item_price['gte'] = str(minPrice)
    if maxPrice: 
        maxPrice = int(maxPrice) * 100000
        item_price['lte'] = maxPrice
    if item_price:
        print(item_price)
        s = s.filter('range', item_price=item_price)
    page = int(page) if page else 0
    s = s[20*page:20*(page+1)]
    response = s.execute()
    results = response['hits']['hits']
    return results