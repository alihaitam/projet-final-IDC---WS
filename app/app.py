import streamlit as st
import subprocess
from rdflib import Graph, Namespace, ConjunctiveGraph
import streamlit.components.v1 as components

# Function to call the Bash script for coordinates
def call_bash_script(city_name):
    try:
        process = subprocess.Popen(
            ['C:\\Program Files\\Git\\git-bash.exe', 'C:\\Users\\user\\Desktop\\projet 100%\\projet-final-IDC-WS\\api_lifitng\\services\\utils\\script.sh', city_name],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout.decode()
        else:
            return f"Error: {stderr.decode()}"
    except Exception as e:
        return str(e)


# Function to query weather information using RDFLib and SPARQL
def get_weather_info(city_name):
    try:
        g = Graph()

        # SPARQL query
        query = f"""
        PREFIX : <http://ns.inria.fr/sparql-micro-service/api#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX schema: <http://schema.org/#>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

        SELECT ?dt_txt ?icon ?temp ?description ?temp_min ?temp_max ?humidity
        WHERE {{
            SERVICE <http://localhost/service/openweathermap/forecast?city={city_name}> {{
                ?forecast schema:temp ?temp ;
                schema:dt_txt ?dt_txt ;
                schema:feels_like ?feels_like ;
                schema:description ?description ;
                schema:temp_min ?temp_min ;
                schema:temp_max ?temp_max ;
                schema:humidity ?humidity ;
                schema:icon ?icon ;
                schema:dt ?dt
            }}
        }}
        ORDER BY (?dt)
        """

        # Execute the query
        results = g.query(query)

        return results

    except Exception as e:
        return str(e)


# Function to run the federated query
def run_federated_query(city_name):
    try:
        # Load the local .ttl file into a graph
        g = ConjunctiveGraph()
        g.parse("C:/Users/user/Desktop/projet 100%/projet-final-IDC-WS/csv_lifitng/prestataires.ttl", format="turtle")

        # SPARQL federated query
        query = f"""
        PREFIX : <http://ns.inria.fr/sparql-micro-service/api#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX schema: <http://schema.org/#>
        PREFIX org: <file:/mnt/c/Users/anass/Downloads/TP_IDC/prestataires_et_organisateurs_details.csv#>

        SELECT ?city ?organizer ?theme ?description
        WHERE {{
            ?organizer org:theme ?theme ;
                org:city ?city .	

            SERVICE <http://localhost/service/openweathermap/forecast?city={city_name}> {{
                ?forecast schema:temp ?temp ;
                schema:dt_txt ?dt_txt ;
                schema:description ?description ;
                schema:cityName ?cityName .
            }}
            FILTER (STR(?cityName) = STR(?city))
        }}
        ORDER BY (?dt)
        """

        # Execute the federated query
        results = g.query(query)
        print("XXXXXXXXXXX", results)

        return results

    except Exception as e:
        return str(e)
    

# Function to create HTML for the weather cards
def create_weather_cards(weather_results):
    cards_html = '<div style="display: flex; overflow-x: auto;">'
    for row in weather_results:
        # Check if icon data exists for this row
        if hasattr(row, 'icon') and row.icon:
            icon_code = row.icon
        else:
            icon_code = "01d"  # Default icon code if none is provided

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        card_html = f"""
            <div style="min-width: 310px; margin: 10px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f1f1f1; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,.2);">
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0)); border-radius: 10px; padding: 15px; width: 100%; text-align: center;">
                    <h3 style="margin: 0; font-family: 'Arial', sans-serif; font-weight: bold;">{row.dt_txt}</h3>
                </div>
                <div style="background-color: white; padding: 8px; border-radius: 30%; margin-top: 10px;">
                    <img src='{icon_url}' alt='Weather icon' style='width: 100px; height: auto;'>
                </div>                
                <p style="margin: 7px 0;"><b>Temperature :</b> {row.temp}°C</p>
                <p style="margin: 7px 0;"><b>Weather Description :</b> {row.description}</p>
                <p style="margin: 7px 0;"><b>Min Temp :</b> {row.temp_min}°C</p>
                <p style="margin: 7px 0;"><b>Max Temp :</b> {row.temp_max}°C</p>
                <p style="margin: 7px 0;"><b>Humidity :</b> {row.humidity}%</p>
            </div>
        """
        cards_html += card_html
    cards_html += '</div>'
    return cards_html


def main():
    # Set page configuration
    st.set_page_config(page_title="City Finder", layout="wide")

    # Title and introduction text
    st.title('🌍 City Latitude and Longitude Finder')
    st.markdown("""
        Welcome to the City Latitude and Longitude Finder. 
        Enter the name of a city and find its geographical coordinates and weather information.
    """)

    # Input form
    with st.form(key='city_form'):
        city_name = st.text_input('Enter the name of a city')
        submit_button = st.form_submit_button(label='Find and Process')

    # Input form for federated query
    with st.form(key='federated_query_form'):
        city_name_query = st.text_input('Enter the name of a city for details')
        get_info_button = st.form_submit_button(label='Get Infos')

    if get_info_button:
        if city_name_query:
            # Run federated query
            federated_results = run_federated_query(city_name_query)
            # You'll need to decide how to display these results.
            # This is an example using markdown, you might want to format it into a table or differently
            st.markdown("## Federated Query Results")
            for row in federated_results:
                st.markdown(f"- Organizer: {row.organizer}, Theme: {row.theme}, Description: {row.description}")
        else:
            st.error("Please enter a city name for details")

    if submit_button:
        if city_name:
            # Get coordinates
            coord_result = call_bash_script(city_name)
            st.markdown("## Coordinates Results")
            st.text_area("Coordinates Output:", value=coord_result, height=150)

            # Get weather information
            weather_results = get_weather_info(city_name)
            st.markdown("## Weather Information")

            # Generate and display weather cards
            weather_cards_html = create_weather_cards(weather_results)
            components.html(weather_cards_html, height=400)

        else:
            st.error("Please enter a city name")

    # Footer
    st.markdown("---")
    st.markdown("City Latitude and Longitude Finder © 2024. All Rights Reserved.")

if __name__ == "__main__":
    main()