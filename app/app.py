import streamlit as st
import subprocess

# Function to call the Bash script
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

# Streamlit application with improved design
def main():
    # Set page configuration
    st.set_page_config(page_title="City Finder", layout="wide")

    # Title and introduction text
    st.title('🌍 City Latitude and Longitude Finder')
    st.markdown("""
        Welcome to the City Latitude and Longitude Finder. 
        Enter the name of a city and find its geographical coordinates.
    """)

    # Input form
    with st.form(key='city_form'):
        city_name = st.text_input('Enter the name of a city')
        submit_button = st.form_submit_button(label='Find and Process')

    if submit_button:
        if city_name:
            result = call_bash_script(city_name)
            st.markdown("## Results")
            st.text_area("Output:", value=result, height=150)
        else:
            st.error("Please enter a city name")

    # Footer
    st.markdown("---")
    st.markdown("City Latitude and Longitude Finder © 2024. All Rights Reserved.")

if __name__ == "__main__":
    main()
