
def get_weather_info(city_name):
    try:
        g = Graph()

        # SPARQL query
        query = f"""
        prefix : <http://ns.inria.fr/sparql-micro-service/api#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        prefix schema: <http://schema.org/#>
        prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

        SELECT ?dt_txt ?temp ?description ?temp_min ?temp_max ?humidity ?icon
        WHERE {{
            SERVICE <http://localhost/service/openweathermap/forecast?city={city_name}> {{
                ?forecast schema:temp ?temp ;
                schema:dt_txt ?dt_txt ;
                schema:description ?description ;
                schema:temp_min ?temp_min ;
                schema:temp_max ?temp_max ;
                schema:humidity ?humidity ;
                schema:icon ?icon
            }}
        }}
        """

        # Execute the query
        results = g.query(query)

        # Create HTML for the results
        html_result = "<div style='display: flex; flex-wrap: wrap;'>"
        for row in results:
            icon_url = f"https://openweathermap.org/img/wn/{row.icon}@2x.png"
            html_result += f"""
                <div style='width: 200px; margin: 10px; padding: 20px; border: 1px solid black; border-radius: 10px; text-align: center;'>
                    <h4>{row.dt_txt}</h4>
                    <img src='{icon_url}' alt='Weather icon' style='width: 100px; height: auto; margin: 10px 0;'>
                    <p>Temp: {row.temp} °C</p>
                    <p>{row.description}</p>
                    <p>Min: {row.temp_min} °C, Max: {row.temp_max} °C</p>
                    <p>Humidity: {row.humidity}%</p>
                </div>
            """
        html_result += "</div>"

        return html_result

    except Exception as e:
        return str(e)
