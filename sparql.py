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

SELECT DISTINCT ?item ?itemDescription ?birthDate ?gender ?birthName ?nativeName ?image ?citizenship ?signature ?occupations ?workDate (GROUP_CONCAT(?category; separator=",") AS ?categories) ?audienceCountry ?authenticEngagement ?country ?engagementAvg ?followers ?link ?rank ?title WHERE {{
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
            SELECT DISTINCT ?item ?itemDescription ?birthDate ?gender ?birthName ?nativeName ?image ?citizenship ?signature (GROUP_CONCAT(?occupation; separator=",") AS ?occupations) ?workDate WHERE {{
            ?item p:P2003 [ps:P2003 "{account_username}"].
              
              ?item p:P1477 [ps:P1477 ?birthName] ;
                    p:P1559 [ps:P1559 ?nativeName] ;
                    p:P18 [ ps:P18 ?image ] ;
                    p:P21 [ ps:P21 ?genderIRI ] ;
                    p:P27 [ ps:P27 ?citizenshipIRI ] ;
                    p:P109 [ ps:P109 ?signature ] ;
                    p:P569 [ psv:P569 [ wikibase:timeValue ?birthDate ] ] ;
                    p:P19 [ ps:P19 ?birthPlaceIRI] ;
                    p:P2031 [ psv:P2031 [ wikibase:timeValue ?workDate ] ];
                    p:P106 [ ps:P106 ?occupationIRI ] .
              
              ?genderIRI rdfs:label ?gender .
              FILTER(LANG(?gender) = "en")
            
              ?citizenshipIRI rdfs:label ?citizenship .
              FILTER(LANG(?citizenship) = "en")
              
              ?occupationIRI rdfs:label ?occupation .
              FILTER(LANG(?occupation) = "en")
              
              ?birthPlaceIRI rdfs:label ?birthPlace .
              FILTER(LANG(?birthPlace) = "en")
            }} GROUP BY ?item ?itemDescription ?birthDate ?gender ?birthName ?nativeName ?image ?citizenship ?signature ?workDate
          }}
        }}
      }}
    }}
    GROUP BY ?item ?itemDescription ?birthDate ?gender ?birthName ?nativeName ?image ?citizenship ?signature ?workDate ?audienceCountry ?authenticEngagement ?country ?engagementAvg ?followers ?link ?rank ?title ?occupations
      """)
    
    return sparql.queryAndConvert()["results"]["bindings"][0]