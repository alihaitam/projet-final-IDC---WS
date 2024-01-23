import streamlit as st
from PIL import Image
import os

def main():
    st.title('Streamlit Image Display')

    # Chemin de l'image
    image_path = r"C:\Users\user\Desktop\projet 100%\projet-final-IDC-WS\app\images\banquet Rooms.jpg"

    # Vérifier si le fichier existe
    if os.path.isfile(image_path):
        # Ouvrir et afficher l'image
        image = Image.open(image_path)
        st.image(image, caption='Banquet Rooms', use_column_width=True)
    else:
        st.error("Image not found. Please check the path.")

if __name__ == "__main__":
    main()
