from flask import Flask, flash, render_template, request, json, redirect
import json
import pandas as pd
from werkzeug.exceptions import HTTPException
from search_api import search, search_view
from cache_utils import saved_data

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        es_results = search(request.form['search'])
        return search_view(es_results)
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def json_search():
    content = request.get_json()
    print(request.get_data())
    if not content:
        flash('Please insert query')
        return redirect('/')
    paras_dict = {}
    paras = ['query', 'mode', 'priceOrder', 'maxPrice', 'minPrice', 'sortBy', 'page']
    for para in paras:
        paras_dict[para] = content[para] if para in content else None
    
    query = paras_dict['query']
    mode = paras_dict['mode']
    order = paras_dict['priceOrder']
    maxPrice = paras_dict['maxPrice']
    minPrice = paras_dict['minPrice']
    sortBy = paras_dict['sortBy']
    page = paras_dict['page']
    if not query:
        flash('Please insert query')
        return redirect('/')
    es_results = search(query, order, maxPrice, \
                        minPrice, sortBy, page)
    if mode == "view":
        return search_view(es_results)
    results = []
    for i in es_results:
        results.append(i['_source']['item_itemid'])
    return {'items_list': results}

@app.route('/para_search', methods=['POST', 'GET'])
def para_search():
    query = request.args.get('query', None)
    mode = request.args.get('mode', None)
    order = request.args.get('priceOrder', None)
    maxPrice = request.args.get('maxPrice', None)
    minPrice = request.args.get('minPrice', None)
    sortBy = request.args.get('sortBy', None)
    page = request.args.get('page', None)
    if not query:
        flash('Please insert query')
        return redirect('/')
    es_results = search(query, order, maxPrice, \
                        minPrice, sortBy, page)
    if mode == "view":
        return search_view(es_results)
    results = []
    keys = ['categories', 'description', 'price', 'tier_variations', 'sold', 'stock', 'name', 'images', 'image', 'attributes']
    for i in es_results:
        _id = eval(i['_id'])
        item = saved_data['items_dict'][_id]
        item_filtered = {key:item['item'][key] for key in keys if key in item['item']}
        results.append(item_filtered)
        #results.append(item['item'])
    return {'items_list': results}

    
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.secret_key = "hello"
    app.run(host='0.0.0.0', port=9873, threaded=True, debug=True)
#     app.run(host='192.168.1.6', port=9873, threaded=True)
