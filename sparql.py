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

def get_account_details(account_username: str):
    sparql.setQuery(f"""
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wds: <http://www.wikidata.org/entity/statement/>
      PREFIX wdv: <http://www.wikidata.org/value/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX p: <http://www.wikidata.org/prop/>
      PREFIX ps: <http://www.wikidata.org/prop/statement/>
      PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX bd: <http://www.bigdata.com/rdf#>

          SELECT DISTINCT ?item ?itemDescription ?gender ?birthName ?nativeName ?image ?citizenship ?signature WHERE {{
            SERVICE <https://query.wikidata.org/sparql> {{
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
              {{
                SELECT DISTINCT ?item ?itemDescription ?gender ?birthName ?nativeName ?image ?citizenship ?signature WHERE {{
                ?item p:P2003 [ps:P2003 "{account_username}"].
                  
                  ?item p:P1477 [ps:P1477 ?birthName] ;
                        p:P1559 [ps:P1559 ?nativeName] ;
                        p:P18 [ps:P18 ?image] ;
                        p:P21 [ps:P21 ?genderIRI] ;
                        p:P27 [ps:P27 ?citizenshipIRI] ;
                        p:P109 [ps:P109 ?signature] .
                  
                  ?genderIRI rdfs:label ?gender .
                  FILTER(LANG(?gender) = "en")
                
                  ?citizenshipIRI rdfs:label ?citizenship .
                  FILTER(LANG(?citizenship) = "en")
                  
                  }}                  
              }}
            }}
          }}
      """)
    
    return sparql.queryAndConvert()["results"]["bindings"]