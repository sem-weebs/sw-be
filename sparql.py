from SPARQLWrapper import JSON, SPARQLWrapper
import json

sparql = SPARQLWrapper(
    "http://localhost:9999/blazegraph/namespace/kb/sparql"
)

sparql.setReturnFormat(JSON)

def search(query: str, category_list: list):
    if len(category_list) > 0:
      filter = f"HAVING(regex(?genres, \"{category_list[0].capitalize()}\")"
      for i in range(1, len(category_list)):
        filter += f" || regex(?genres, \"{category_list[i].capitalize()}\")"
      filter += ")"
    else:
      filter = ""

    print(filter)
    sparql.setQuery(""" """)
    
    return sparql.queryAndConvert()["results"]["bindings"]

def get_suggestions(query: str):
    sparql.setQuery(""" """.format(json.dumps(query)))

    return sparql.queryAndConvert()["results"]["bindings"]

def get_account_details(account_id: str):
    sparql.setQuery(f""" """)

    return sparql.queryAndConvert()["results"]["bindings"][0]