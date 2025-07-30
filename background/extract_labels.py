from rdflib import Graph

g = Graph().parse("borehole-status-gsq.ttl")
q = """
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    CONSTRUCT {
        ?iri
            rdfs:label ?name ;
            schema:description ?desc ;
        .
    }
    WHERE {
        ?iri
            skos:prefLabel ?name ;
        .
    
        OPTIONAL {
            ?iri
                skos:definition ?desc ;
            .
        }
    }
    """

r = g.query(q)
r.serialize(format="longturtle", destination="borehole-status-gsq.2.ttl")