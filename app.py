from flask import Flask, request
from flask_api import status
from flask_cors import CORS

import json
import sparql

app = Flask(__name__)

CORS(app)

@app.route("/search", methods=["GET"])
def search():
    args = request.args
    # print(args)
    query = args.get("q")
    # print(query)
    categories = args.get("categories")
    # print(categories)

    if (categories is not None):
        categories_list = categories.split(";")
    else:
        categories_list = []

    # print(categories_list)

    if not query:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.search(query, categories_list)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_INTERNAL_SERVER_ERROR
    
@app.route("/suggestions", methods=["GET"])
def suggestions():
    args = request.args
    query = args.get("q")

    if not query:
        return json.dumps([])

    try:
        return sparql.get_suggestions(query)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route("/details", methods=["GET"])
def details():
    args = request.args
    account_username = args.get("username")

    if not account_username:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.get_account_details(account_username)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_INTERNAL_SERVER_ERROR