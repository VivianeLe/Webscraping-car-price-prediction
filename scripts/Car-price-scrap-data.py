# !pip install user_agent
# !pip install requests
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time
import random
import csv

csv_filename = 'data/car-price2.csv'
def save_to_csv(data, filename):
    # save a list of dict to csv
        headers = data[0].keys()
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, headers)
            if file.tell() == 0:
              writer.writeheader()
            writer.writerows(data)

pages = 150  # Set the desired number of pages to scrape the data

#Input base url and page
for page in range(1, pages+1):
  # Input base url and page
    page_url = f"https://www.aramisauto.com/achat/recherche?page={page}"
    print(f"\nScraping reviews for {page_url}")

    # Introduce a random delay between 5 and 15 seconds
    delay_seconds = random.uniform(5, 15)
    time.sleep(delay_seconds)

    try:
        # Create a user agent
        user_agent = generate_user_agent()

        # Send a GET request with a user agent
        headers = {"User-Agent": user_agent}
        response = requests.get(page_url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract review information
        list = []

        # Input message tag and class
        parent = soup.find_all("div", class_="vehicle-container") 
        print(len(parent))

        for temp in parent:
            transmission_elem = temp.find("div", class_="vehicle-transmission")
            km_elem = temp.find("div", class_="vehicle-zero-km")
            price_elem = temp.find("span", class_="vehicle-loa-offer")

            transmission = transmission_elem.text.strip() if transmission_elem else "N/A"
            km = km_elem.text.strip() if km_elem else "N/A"
            price = price_elem.text.strip().replace('€', '').strip() if price_elem else "N/A"
            carburant = transmission.split('-')[0].strip()

            for a in temp.find_all('a', class_="real-link vehicle-info-link", href=True):
                car_url = f"https://www.aramisauto.com{a['href']}"
                response1 = requests.get(car_url, headers=headers)
                soup1 = BeautifulSoup(response1.text, "html.parser") 

                name = ""     
                for temp in soup1.find_all('div', class_="price-information"):
                    name = temp.find('li', class_="subtitle-1 bold").text.strip()

                for b in soup1.find_all('div', class_="product-key-points-list"):
                    row_title = b.find_all('div', class_="labels-title subtitle-1")
                    row = b.find_all('div', class_="labels-body")
                    print(len(row))
                    
                    consommation = ""
                    co2 = ""
                    color = ""
                    porte = ""

                    # for i in range(1, len(row_title)):
                    #     consommation = row[i].text.strip() if row_title[i].text.strip() == 'Consommation' else "N/A"
                    #     co2 = row[i].text.strip() if 'Émission' in row_title[i].text.strip() else "N/A"
                    #     color = row[i].text.strip() if row_title[i].text.strip() == 'Couleur' else "N/A"
                    #     porte = row[i].text.strip() if row_title[i].text.strip() == 'Nombre de portes' else "N/A"
                    # if len(row)==13:
                    #     consommation = row[7].text.strip() if row_title[7].text.strip() == 'Consommation' else "N/A"
                    #     co2 = row[10].text.strip() if 'Émission' in row_title[10].text.strip() else "N/A"
                    #     color = row[11].text.strip() if row_title[11].text.strip() == 'Couleur' else "N/A"
                    #     porte = row[12].text.strip() if row_title[12].text.strip() == 'Nombre de portes' else "N/A"

                    if len(row)==14:
                        consommation = row[7].text.strip() if row_title[7].text.strip() == 'Consommation' else "N/A"
                        co2 = row[10].text.strip() if 'Émission' in row_title[10].text.strip() else "N/A"
                        color = row[11].text.strip() if row_title[11].text.strip() == 'Couleur' else "N/A"
                        porte = row[12].text.strip() if row_title[12].text.strip() == 'Nombre de portes' else "N/A"

                    elif len(row)==15:
                        consommation = row[8].text.strip() if row_title[8].text.strip() == 'Consommation' else "N/A"
                        co2 = row[11].text.strip() if 'Émission' in row_title[11].text.strip() else "N/A"
                        color = row[12].text.strip() if row_title[12].text.strip() == 'Couleur' else "N/A"
                        porte = row[13].text.strip() if row_title[13].text.strip() == 'Nombre de portes' else "N/A"
                    
                    elif len(row)==16:
                        consommation = row[9].text.strip() if row_title[9].text.strip() == 'Consommation' else "N/A"
                        co2 = row[12].text.strip() if 'Émission' in row_title[12].text.strip() else "N/A"
                        color = row[13].text.strip() if row_title[13].text.strip() == 'Couleur' else "N/A"
                        porte = row[14].text.strip() if row_title[14].text.strip() == 'Nombre de portes' else "N/A"
                    
                    elif len(row)==17:
                        consommation = row[10].text.strip() if row_title[10].text.strip() == 'Consommation' else "N/A"
                        co2 = row[13].text.strip() if 'Émission' in row_title[13].text.strip() else "N/A"
                        color = row[14].text.strip() if row_title[14].text.strip() == 'Couleur' else "N/A"
                        porte = row[15].text.strip() if row_title[15].text.strip() == 'Nombre de portes' else "N/A"
                    
                    elif len(row)==18:
                        consommation = row[8].text.strip() if row_title[8].text.strip() == 'Consommation' else "N/A"
                        co2 = row[14].text.strip() if 'Émission' in row_title[14].text.strip() else "N/A"
                        color = row[15].text.strip() if row_title[15].text.strip() == 'Couleur' else "N/A"
                        porte = row[16].text.strip() if row_title[16].text.strip() == 'Nombre de portes' else "N/A"

                        # Input function
                    if ((price != "N/A") & (name!="N/A") & (transmission!="N/A") & (km!="N/A")):
                        list.append(
                            {"Name": name,
                            "Brand": name.split(' ')[0].strip(),
                            "Color": color,
                            "Fuel": carburant,
                            "Gearbox": transmission.split('-')[1].strip(),
                            "Year": km.split('-')[0].strip(),
                            "Km": km.split('-')[1].strip().replace(' km', '').replace(' ',''),
                            "Fuel_consumption": 0.0 if carburant=='Electrique' else consommation.split(' L')[0].replace(',', '.').strip(),
                            "Co2_emission": 0 if carburant=='Electrique' else co2.split(' g')[0].strip(),
                            "Doors": porte,
                            "Price": price.replace(r'\D', '')})
        # if list:
        #     for index, temp in enumerate(list, start=1):
        #         print(f"Car no: {index}")
        #         print(f"Name: {temp['Name']}")
        #         print(f"Motorisation: {temp['Motorisation']}")
        #         print(f"Carburant: {temp['Carburant']}")
        #         print(f"Boite de vitesse: {temp['Boite_de_vitesse']}")
        #         print(f"Year: {temp['Year']}")
        #         print(f"Km: {temp['Km']}")
        #         print(f"Color: {temp['Color']}")
        #         print(f"Price: {temp['Price']}")
        #         print("---------------")

        save_to_csv(list, csv_filename)
        print("Data is saved in csv")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page {page_url}. Exception: {e}")