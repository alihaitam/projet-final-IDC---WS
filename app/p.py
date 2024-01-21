from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib

def execute_federated_query():
    # Load the local .ttl file
    g = rdflib.Graph()
    file_path = 'C:/Users/user/Desktop/projet 100%/projet-final-IDC-WS/csv_lifitng/prestataires.ttl'
    g.parse(file_path, format="ttl")
    print("LEEEEN", len(g))
    
    # Define the federated query
    query = f"""
    prefix : <http://ns.inria.fr/sparql-micro-service/api#>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix schema: <http://schema.org/#>
    prefix org: <file:/mnt/c/Users/anass/Downloads/TP_IDC/prestataires_et_organisateurs_details.csv#>
    
    SELECT  ?dt_txt ?theme ?description
    WHERE {{
           
        SERVICE <http://localhost/service/openweathermap/forecast?city=paris> {{
            ?forecast schema:temp ?temp ;
                schema:dt_txt ?dt_txt ;
                schema:description ?description ;
                schema:cityName ?cityName ;
                schema:dt ?dt .
        }}
        FILTER (STR(?cityName) = STR(?city))
    }}
    ORDER BY (?dt)
    """

    # Execute the query on the local graph
    results = g.query(query)

    # Process results
    for row in results:
        print(row)

    # If you need to query a remote SPARQL endpoint, use SPARQLWrapper
    # sparql = SPARQLWrapper("http://localhost/service/openweathermap/forecast?city=paris")
    # sparql.setQuery(query)
    # sparql.setReturnFormat(JSON)
    # remote_results = sparql.query().convert()

    # Process remote results
    # for result in remote_results["results"]["bindings"]:
    #     print(result)

execute_federated_query()