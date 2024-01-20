import requests
from bs4 import BeautifulSoup
import csv

# URL de la page à scraper
url = 'https://www.lemagdelevenementiel.com/prestations-region-11.html'

# Faites une requête GET pour récupérer le contenu de la page
response = requests.get(url)
html = response.content

# Parsez le HTML avec BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Trouvez les éléments qui contiennent les informations des prestations
prestations = soup.find_all('span', class_='titre')

# Créez ou ouvrez votre fichier CSV
csv_data = [['Nom de la prestation', 'À propos de l\'organisateur']]

# Parcourez tous les éléments de prestation et extrayez les informations
for prestation in prestations:
    # Extrayez le texte et le lien vers la prestation
    nom_prestation = prestation.find('a').text.strip()
    lien_prestation = prestation.find('a')['href']
    
    # Faites une nouvelle requête GET pour la page de détails de la prestation
    response_detail = requests.get(lien_prestation)
    soup_detail = BeautifulSoup(response_detail.content, 'html.parser')

    # Trouver le div avec l'id "tabs-1"
    div_1 = soup_detail.find('div', id='tabs-1')
    if div_1 :
        # Trouvez le span avec la classe "box-texte" et extrayez le contenu du tag div
        box_d = div_1.find('div', class_='box-texte')
        # g_box = soup_detail.find('div', class_='g-box')
        if box_d:
            text_about_organizer = box_d.find('p').text.strip()
            print(text_about_organizer)
        # elif g_box:
        #     text_about_organizer = g_box.find('p').text.strip()
        else:
            text_about_organizer = 'Information non trouvée'     
    
        # Ajoutez les informations extraites au CSV
        csv_data.append([nom_prestation, text_about_organizer])
    else:
        csv_data.append([nom_prestation, 'Information non trouvée'])

# Écrivez toutes les données dans le fichier CSV
with open('prestataires_et_organisateurs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)

# ajouter aux CSV trois colonnes : tarif, adresse, téléphone, région toutes remplis par "Will be added soon"
