import requests
from bs4 import BeautifulSoup
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# URL de la page à scraper
url = """https://www.lemagdelevenementiel.com/prestations-region-2.html"""
region = 'Centre-Val de Loire'
city='Orléans'

# Faites une requête GET pour récupérer le contenu de la page
response = requests.get(url)
html = response.content

# Parsez le HTML avec BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Trouvez les éléments qui contiennent les informations des prestations
prestations = soup.find_all('span', class_='titre')

# Créez ou ouvrez votre fichier CSV
csv_data = [['Nom de la prestation', 'À propos de l\'organisateur', 'Tarif', 'Adresse']]

# Parcourez tous les éléments de prestation et extrayez les informations
for prestation in prestations:
    # Extrayez le texte et le lien vers la prestation
    nom_prestation = prestation.find('a').text.strip()
    lien_prestation = prestation.find('a')['href']
    #print(nom_prestation, lien_prestation)
    
    # Faites une nouvelle requête GET pour la page de détails de la prestation
    response_detail = requests.get(lien_prestation)
    soup_detail = BeautifulSoup(response_detail.content, 'html.parser')
    
    # Trouvez le span avec la classe "box-d" et extrayez le contenu du tag <p>
    box_d = soup_detail.find('span', class_='box-d')
    if box_d:
        text_about_organizer = box_d.find('p').text.strip() if box_d.find('p') else 'Information non trouvée'
        
        # Trouvez le deuxième div dans le span "box-d" pour extraire le tarif et l'adresse
        divs = box_d.find_all('div')
        if len(divs) > 1:
            # Extraction des informations du tarif et de l'adresse
            infos = divs[1].get_text(separator='\n').split('\n')
            tarif = infos[1].split(':')[-1].strip() if len(infos) > 1 else 'Tarif non trouvé'
            # stocker les elements de infos a partir de l'indice 8 jusqua lindice 11 dans infos
            adresse = infos[8:11]
            # supprimer l'element qui commence par 'Tél' si il est trouvé dans adresse
            adresse = [x for x in adresse if not x.startswith('Tél')]
            # Join les elements de adresse avec un espace
            adresse = ' '.join(adresse).strip()
            # print(adresse)
            # trouve l'element qui commence par 'Tél' si il est trouvé dans infos et le stocker dans tel
            tel = [x for x in infos if x.startswith('Tél')] if len(infos) > 1 else 'Tél non trouvé'
        else:
            tarif = 'Tarif non trouvé'
            adresse = 'Adresse non trouvée'
            tel = 'Tél non trouvé'
    else:
        text_about_organizer = 'Information non trouvée'
        tarif = 'Tarif non trouvé'
        adresse = 'Adresse non trouvée'
        tel = 'Tél non trouvé'

    # Ajoutez les informations extraites au CSV
    csv_data.append([nom_prestation, text_about_organizer, tarif, adresse, tel, region, city])
    print(adresse)


csv_file_path = 'prestataires_et_organisateurs_details.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)