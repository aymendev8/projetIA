from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_leboncoin(ville):
    # Configuration de Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécute Chrome en mode sans tête (sans interface graphique)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('/path/to/chromedriver')  # Remplacez par le chemin vers votre chromedriver
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # URL de base pour les annonces immobilières sur Leboncoin
    base_url = f"https://www.leboncoin.fr/recherche?category=9&locations={ville}&real_estate_type=1,2"
    driver.get(base_url)
    
    # Attendre que les annonces soient chargées
    time.sleep(5)
    
    # Extraire les annonces
    ads = driver.find_elements(By.CLASS_NAME, '_3DFQ-')
    
    # Initialiser une liste pour stocker les données
    data = []
    
    # Extraire les informations de chaque annonce
    for ad in ads:
        try:
            price = ad.find_element(By.CLASS_NAME, '_1F5u3').text
            title = ad.find_element(By.CLASS_NAME, 'd71sj').text
            surface_habitable = ad.find_element(By.CLASS_NAME, '_2qeuk').text
            
            if 'appartement' in title.lower():
                property_type = 'Appartement'
            elif 'maison' in title.lower():
                property_type = 'Maison'
            else:
                property_type = 'Autre'
                
            pieces = next((int(word) for word in title.split() if word.isdigit()), 'N/A')
            
            data.append({
                'prix': price,
                'n_pieces': pieces,
                'Ville': ville,
                'type_batiment': property_type,
                'surface_habitable': surface_habitable
            })
        except Exception as e:
            print(f"Erreur lors de l'extraction des données d'une annonce: {e}")
            continue
    
    # Fermer le navigateur
    driver.quit()
    
    # Créer un DataFrame pandas à partir des données
    df = pd.DataFrame(data)
    
    # Enregistrer le DataFrame dans un fichier CSV
    df.to_csv(f"{ville}_annonces.csv", index=False)
    print(f"Fichier {ville}_annonces.csv créé avec succès.")

# Exemple d'utilisation
scrape_leboncoin('nice')
