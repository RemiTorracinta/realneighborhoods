from flask import Flask
from markupsafe import escape
from SPARQLWrapper import SPARQLWrapper, JSON


neighborhoods = set()

app = Flask(__name__)

@app.route("/<neighborhood>")
def is_neighborhood(neighborhood):
    if neighborhood in neighborhoods:
        return f"yes {escape(neighborhood)} is real."
    else:
        return f"no {escape(neighborhood)} is not real."


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
        neighborhoods.add(neighborhood['name']['value'])


preload_neighborhoods()

