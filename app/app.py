import streamlit as st
import subprocess
from rdflib import Graph, Namespace, ConjunctiveGraph
import streamlit.components.v1 as components

# Function to call the Bash script for coordinates
def call_bash_script(city_name):
    try:
        process = subprocess.Popen(
            ['C:\\Program Files\\Git\\git-bash.exe', 'C:\\Users\\user\\Desktop\\projet 100%\\projet-final-IDC-WS\\api_lifitng\\services\\utils\\data-script.sh', city_name],
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
def run_venueCategory_query(venueCategory, city_name):
    try:
        # Load the local .ttl file into a graph
        g = ConjunctiveGraph()
        g.parse(r"C:\Users\user\Desktop\projet 100%\projet-final-IDC-WS\api_lifitng\data\city_venues.ttl", format="turtle")
        g.parse(r"C:\Users\user\Desktop\projet 100%\projet-final-IDC-WS\csv_lifitng\services_providers.ttl", format="turtle")

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
        return results

    except Exception as e:
        st.write(f"An error occurred: {e}")


# Function to create HTML for the weather cards
def create_weather_cards(weather_results):
    cards_html = '<div style="display: flex; overflow-x: auto;">'
    for row in weather_results:
        # print the icon code
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


# Function to create HTML for the venue cards
def create_venue_cards(venue_results, category):
    # Utiliser un chemin relatif pour le dossier des images
    image_folder_path = "./images/" 

    # Construire le chemin de l'image en fonction de la catégorie
    category_image_filename = category.lower().replace(" ", "_") + ".jpg"
    category_image_url = image_folder_path + category_image_filename
    category_image_url = f"https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

    # Création du HTML pour les cartes
    cards_html = '<div style="display: flex; overflow-x: auto;">'
    for venue in venue_results:
        card_html = f"""
            <div style="min-width: 310px; margin: 10px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #e1f5fe; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,.2); font-family: 'Arial', sans-serif;">
                <img src="{category_image_url}" alt="{category}" style="width: 100px; height: auto; margin-bottom: 10px;">
                <h3 style="text-align: center; margin: 0; font-weight: bold;">{venue[0]}</h3>
                <p style="text-align: center; margin: 7px 0;"><b>Adresse :</b> {venue[1]}</p>
                <p style="text-align: center; margin: 7px 0;"><b>Ville :</b> {venue[2]}</p>
            </div>
        """
        cards_html += card_html
    cards_html += '</div>'
    return cards_html


# Function to create HTML for the provider cards
def create_provider_cards(provider_results):
    cards_html = '<div style="display: flex; overflow-x: auto;">'
    for provider in provider_results:
        card_html = f"""
            <div style="min-width: 310px; margin: 10px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #ffe0b2; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,.2); font-family: 'Arial', sans-serif;">
                <h3 style="text-align: center; margin: 0; font-weight: bold;">{provider[0]}</h3>
                <p style="text-align: center; margin: 7px 0;"><b>Prix moyen :</b> {provider[1]}</p>
                <p style="text-align: center; margin: 7px 0;"><b>Téléphone :</b> {provider[2]}</p>
                <p style="text-align: center; margin: 7px 0;"><b>Ville :</b> {provider[3]}</p>
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

    # Initialize session state variables if they don't exist
    if 'city_name' not in st.session_state:
        st.session_state.city_name = ""
    if 'city_selected' not in st.session_state:
        st.session_state.city_selected = False
    if 'category_selected' not in st.session_state:
        st.session_state.category_selected = False

    # Define venue categories with unique key numbers
    venue_categories = {
        "restaurant": 1,
        "cinema": 2,
        "beach Club": 3,
        "museum": 4,
        "stadium": 5,
        "hotel": 6,
        "theater": 7,
        "café Pub": 8,
        "banquet Rooms": 9,
        "convention Center": 10,
    }

    # Input for city name
    city_name = st.text_input('Enter the name of a city', key="city_name_input", value=st.session_state.city_name)
    submit_button = st.button(label='Find and Process', key="submit_button")

    if submit_button:
        st.session_state.city_name = city_name
        st.session_state.city_selected = True
        st.success(f"City name '{city_name}' received.")
        call_bash_script(city_name)

        # Get weather information
        weather_results = get_weather_info(city_name)
        st.markdown("## Weather Information")

        # Generate and display weather cards
        weather_cards_html = create_weather_cards(weather_results)
        components.html(weather_cards_html, height=400)

    # If a city is selected, show category selection form
    if st.session_state.city_selected and not st.session_state.category_selected:
        selected_category = st.selectbox('Select your desired category', list(venue_categories.keys()), key="category_select")
        category_submit_button = st.button(label='View Choices', key="category_submit_button")

        if category_submit_button:
            st.session_state.category_selected = True
            # Call the function and get the results
            category_results = run_venueCategory_query(selected_category, city_name)
            # Check if results is a string (an error message)
            if isinstance(category_results, str):
                st.error(category_results)
            else:
                # Initialisation des listes pour les lieux et les prestataires
                venues = []
                providers = []

                # Parcourir chaque résultat et les classer dans les listes appropriées
                for row in category_results:
                    if row.providerName is None:
                        venues.append((row.venueName, row.venueAddress, row.venueCity))
                    elif row.venueName is None:
                        providers.append((row.providerName, row.providerPrice, row.providerPhone, row.provviderCity))

                # Génération et affichage des cartes pour les lieux
                if venues:
                    st.markdown("### Liste des Lieux (Venues)")
                    venue_cards_html = create_venue_cards(venues, selected_category)
                    components.html(venue_cards_html, height=400)
                else:
                    st.markdown("Aucun lieu trouvé.")

                # Génération et affichage des cartes pour les prestataires
                if providers:
                    st.markdown("### Liste des Prestataires de Services")
                    provider_cards_html = create_provider_cards(providers)
                    components.html(provider_cards_html, height=400)
                else:
                    st.markdown("Aucun prestataire trouvé.")
    # Footer
    st.markdown("---")
    st.markdown("City Latitude and Longitude Finder © 2024. All Rights Reserved.")


if __name__ == "__main__":
    main()



# # Define venue categories with unique key numbers
# venue_categories = {
#     "restaurant": 1,
#     "cinema": 2,
#     "beach Club": 3,
#     "museum": 4,
#     "stadium": 5,
#     "hotel": 6,
#     "theater": 7,
#     "café/Pub": 8,
#     "banquet Rooms": 9,
#     "convention Center": 10,
# }
