from flask import Flask
from markupsafe import escape
from SPARQLWrapper import SPARQLWrapper, JSON
import re

neighborhoods = {}

app = Flask(__name__)

@app.route("/<neighborhood>")
def is_neighborhood(neighborhood):
    normalized_name = normalize_neighborhood_name(neighborhood)
    if normalized_name in neighborhoods:
        real_name = neighborhoods[normalized_name]
        return f"yes {escape(real_name)} is real."
    else:
        return f"no {escape(neighborhood)} is not real."


def normalize_neighborhood_name(name):
    return re.sub(r'[^a-zA-Z0-9]','', name.lower())


def preload_neighborhoods():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX gold: <http://purl.org/linguistics/gold/>

    SELECT ?name 
    WHERE {
      ?neighborhood dbp:name ?name .
      ?neighborhood gold:hypernym dbr:Neighborhood .
      ?neighborhood dbo:subdivision dbr:New_York_City .
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for neighborhood in results["results"]["bindings"]:
        real_name = neighborhood['name']['value']
        normalized_name = normalize_neighborhood_name(real_name)
        neighborhoods[normalized_name] = real_name
    print(neighborhoods)


preload_neighborhoods()

