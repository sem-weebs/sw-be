from typing import List
from SPARQLWrapper import JSON, SPARQLWrapper
import json

url = "http://localhost:9999/blazegraph/namespace/kb/sparql"

try:
   with open("./.enviro") as f:
      url = f.read().strip()
except Exception:
   pass

print(f"{url=}")

sparql = SPARQLWrapper(
    url
)

sparql.setReturnFormat(JSON)

def search(query: str, category_list: List[str]):
    if len(category_list) > 0:
      cat_filter = f"HAVING(regex(?categories, \"{category_list[0]}\", \"i\")"
      for i in range(1, len(category_list)):
        cat_filter += f" || regex(?categories, \"{category_list[i]}\", \"i\")"
      cat_filter += ")"
    else:
      cat_filter = ""

      

    print(cat_filter)
    qq = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX swep: <http://semweebs.org/property/>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?username ?title ?image ?categories WHERE {{
      {{
      	SELECT DISTINCT ?username ?title (GROUP_CONCAT(?category; SEPARATOR=",") as ?categories) WHERE {{
            ?usernameIRI rdfs:label ?username ;
                      swep:title ?title .

            OPTIONAL {{ 
              ?usernameIRI swep:category ?categoryIRI .
              ?categoryIRI rdfs:label ?category 
            }}
          	FILTER(CONTAINS(LCASE(?username), LCASE("{query}")) || CONTAINS(LCASE(?title), LCASE("{query}")))
        }}  GROUP BY ?username ?title
            {cat_filter}
      }}
      

      SERVICE <https://query.wikidata.org/sparql> {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        {{
          SELECT DISTINCT ?username2 ?image WHERE {{
            ?itemIRI p:P2003 [ ps:P2003 ?username2 ] .
            OPTIONAL {{
              ?itemIRI p:P18 [ ps:P18 ?image ] .
            }}
            FILTER(CONTAINS(LCASE(?username2), LCASE("{query}")) || CONTAINS(LCASE(?title2), LCASE("{query}")))
          }} LIMIT 1
        }}
      }}
    }}
    """

    print(qq)
    sparql.setQuery(qq)
    
    return sparql.queryAndConvert()["results"]["bindings"]

def get_suggestions(account_username: str):
    sparql.setQuery(f""" 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX swep: <http://semweebs.org/property/>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?sampledCategory WHERE {{
      ?userIRI rdfs:label "{account_username}" ;
              swep:category ?categoryIRI .
      ?categoryIRI rdfs:label ?sampledCategory
    }} LIMIT 1

    SELECT DISTINCT ?username ?title ?image (GROUP_CONCAT(?category; SEPARATOR=",") as ?categories) WHERE {{
      ?usernameIRI rdfs:label ?username ;
                  swep:title ?title .
      OPTIONAL {{
        ?usernameIRI swep:category ?categoryIRI .
        ?categoryIRI rdfs:label ?category
      }}
      SERVICE <https://query.wikidata.org/sparql> {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        {{
          SELECT DISTINCT ?image WHERE {{
            ?itemIRI p:P2003 [ps:P2003 ?username] .
            OPTIONAL {{
              ?itemIRI p:P18 [ ps:P18 ?image ] .
            }}
            FILTER(CONTAINS(LCASE(?username), LCASE("{account_username}")))
          }} LIMIT 1
        }}
      }}
      FILTER(CONTAINS(LCASE(?username), LCASE("{account_username}")))
    }} 
    GROUP BY ?username ?title ?image
    HAVING(regex(?categories, ?sampledCategory, "i") && ?username != "{account_username}")
    LIMIT 10
    """)

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
PREFIX psv: <http://www.wikidata.org/prop/statement/value/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX :      <http://127.0.0.1:3333/>
PREFIX dbr:   <http://dbpedia.org/resource/>
PREFIX owl:   <http://www.w3.org/2002/07/owl#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX swep:  <http://semweebs.org/property/>
PREFIX swer:  <http://semweebs.org/resource/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?item ?itemDescription ?birthDate ?birthPlace ?gender ?birthName ?nativeName ?image ?citizenship ?signature ?occupations ?workDate (GROUP_CONCAT(?category; separator=",") AS ?categories) ?audienceCountry ?authenticEngagement ?country ?engagementAvg ?followers ?link ?rank ?title WHERE {{
  {{
  ?usernameIRI rdfs:label "{account_username}" ;
               swep:audienceCountry [ rdfs:label ?audienceCountry ] ;
               swep:authenticEngagement ?authenticEngagement ;
               swep:country ?country ;
               swep:engagementAvg ?engagementAvg ;
               swep:followers ?followers ;
               swep:link ?link ;
               swep:rank ?rank ;
               swep:title ?title .
    OPTIONAL {{ ?usernameIRI swep:category ?categoryIRI .
              ?categoryIRI rdfs:label ?category }}
               
  }}
  {{
        SERVICE <https://query.wikidata.org/sparql> {{
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
          {{
            SELECT DISTINCT ?item ?itemDescription ?birthDate ?gender ?birthName ?birthPlace ?nativeName ?image ?citizenship ?signature (GROUP_CONCAT(?occupation; separator=",") AS ?occupations) ?workDate WHERE {{
            ?item p:P2003 [ps:P2003 "{account_username}"].
              
            OPTIONAL {{
              ?item p:P1477 [ps:P1477 ?birthName] .
            }}
            OPTIONAL {{
              ?item p:P1559 [ps:P1559 ?nativeName] .
            }}
            OPTIONAL {{
              ?item p:P18 [ ps:P18 ?image ] .
            }}
            OPTIONAL {{
              ?item p:P21 [ ps:P21 ?genderIRI ] .

              ?genderIRI rdfs:label ?gender .
              FILTER(LANG(?gender) = "en")
            }}
            OPTIONAL {{
              ?item p:P27 [ ps:P27 ?citizenshipIRI ] .

              ?citizenshipIRI rdfs:label ?citizenship .
              FILTER(LANG(?citizenship) = "en")
            }}
            OPTIONAL {{
              ?item p:P109 [ ps:P109 ?signature ] .
            }}
            OPTIONAL {{
              ?item p:P569 [ psv:P569 [ wikibase:timeValue ?birthDate ] ] .
            }}
            OPTIONAL {{
              ?item p:P19 [ ps:P19 ?birthPlaceIRI] .

              ?birthPlaceIRI rdfs:label ?birthPlace .
              FILTER(LANG(?birthPlace) = "en")
            }}
            OPTIONAL {{
              ?item p:P2031 [ psv:P2031 [ wikibase:timeValue ?workDate ] ] .
            }}
            OPTIONAL {{
              ?item p:P106 [ ps:P106 ?occupationIRI ] .

              ?occupationIRI rdfs:label ?occupation .
              FILTER(LANG(?occupation) = "en")
            }}
              
            }} GROUP BY ?item ?itemDescription ?birthDate ?gender ?birthName ?birthPlace ?nativeName ?image ?citizenship ?signature ?workDate
          }}
        }}
      }}
    }}
    GROUP BY ?item ?itemDescription ?birthDate ?gender ?birthName ?birthPlace ?nativeName ?image ?citizenship ?signature ?workDate ?audienceCountry ?authenticEngagement ?country ?engagementAvg ?followers ?link ?rank ?title ?occupations
      """)
    
    return sparql.queryAndConvert()["results"]["bindings"][0]