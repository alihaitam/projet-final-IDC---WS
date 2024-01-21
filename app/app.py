import streamlit as st
import subprocess

# Function to call the Bash script
def call_bash_script(city_name):
    try:
        # Replace 'path/to/git-bash.exe' with the actual path of Git Bash or similar tool
        process = subprocess.Popen(['C:\\Program Files\\Git\\git-bash.exe', 'C:\\Users\\user\\Desktop\\projet 100%\\projet-final-IDC-WS\\api_lifitng\\services\\utils\\script.sh', city_name],
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout.decode()
        else:
            return f"Error: {stderr.decode()}"
    except Exception as e:
        return str(e)

# Streamlit application
def main():
    st.title('City Latitude and Longitude Finder')

    city_name = st.text_input('Enter the name of a city')

    if st.button('Find and Process'):
        if city_name:
            result = call_bash_script(city_name)
            st.text(result)
        else:
            st.error("Please enter a city name")

if __name__ == "__main__":
    main()
