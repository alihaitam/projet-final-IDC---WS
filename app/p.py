from rdflib import Graph, Namespace, ConjunctiveGraph

def run_venueCategory_query(venueCategory, city_name):

    # Load the local .ttl file into a graph
    g = Graph()
    g.parse(r"C:\Users\user\Desktop\projet 100%\projet-final-IDC-WS\api_lifitng\data\city_venues.ttl", format="turtle")
    g.parse(r"C:\Users\user\Desktop\projet 100%\projet-final-IDC-WS\csv_lifitng\services_providers.ttl", format="turtle")

    # SPARQL query using the provided venueCategory
    # query = f"""
    # PREFIX ns1: <http://schema.org/#>
    # PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    # PREFIX org: <file:/mnt/c/Users/anass/Downloads/TP_IDC/prestataires_et_organisateurs_details.csv#>

    # query = f"""
    # PREFIX ns1: <http://schema.org/#>
    # PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    # PREFIX org: <file:/mnt/c/Users/anass/Downloads/TP_IDC/prestataires_et_organisateurs_details.csv#>

    # SELECT ?venueName ?venueAddress ?providerName ?providerTheme ?providerCity
    # WHERE {{
    # {{
    #     ?place ns1:name ?venueName .
    #     OPTIONAL {{ ?place ns1:address ?venueAddress ; }}
    #     OPTIONAL {{ ?place ns1:city ?venueCity ; }}
    
    # }} UNION {{
    #     ?provider org:provider_name ?providerName .
    #     OPTIONAL {{ ?provider org:theme ?providerTheme ; }}
    #     OPTIONAL {{ ?provider org:city ?providerCity ; }}
    #     FILTER (?providerCity = "{city_name}")
    # }}
    # }}
    # """

    city_name_lower = city_name.lower()
    venueCategory_lower = venueCategory.lower()

    # SPARQL query using the provided venueCategory
    query = f"""
    PREFIX ns1: <http://schema.org/#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX org: <file:/mnt/c/Users/anass/Downloads/TP_IDC/prestataires_et_organisateurs_details.csv#>

    SELECT ?venueName ?venueAddress ?venueCity ?providerName ?providerPrice ?providerPhone ?providerCity
    WHERE {{
    {{
        ?place ns1:name ?venueName .
        OPTIONAL {{ ?place ns1:freeFormAddress ?venueAddress ; }}
        OPTIONAL {{ ?place ns1:city ?venueCity ; }}
        OPTIONAL {{ ?place ns1:category ?venueCategory ; }}
    }} UNION {{
        ?provider org:provider_name ?providerName .
        OPTIONAL {{ ?provider org:theme ?providerTheme ; }}
        OPTIONAL {{ ?provider org:price ?providerPrice ; }}
        OPTIONAL {{ ?provider org:phone ?providerPhone ; }}
        OPTIONAL {{ ?provider org:city ?providerCity ; }}
        FILTER (LCASE(STR(?providerCity)) = STR("{city_name_lower}"))
    }}
    }}
    """

    # Execute the query
    results = g.query(query)

    print("XX", len(results))
    for row in results:
        print(row)

run_venueCategory_query("restaurant", "Nice")