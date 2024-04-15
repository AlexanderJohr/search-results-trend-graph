import requests
from bs4 import BeautifulSoup

# Basis-URL und Startparameter für die Seitennummer
base_url = "https://alternativeto.net/software/survey-js/"
page_number = 1

# Liste zur Speicherung der extrahierten Texte
h2_texts = []

# Benutzeragent für die Anfrage
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
           'Cookie': 'a2=443%7Cfalse; __cf_bm=_7FcudZaGN63gODpMQF4HTKf4quBqv1lOJRtge1oWu0-1712665984-1.0.1.1-LS8TxNOepe.lhbvR0eOJ.Ra3vqox52Sq5JqJg9psQ5tWoQj68nO.mdETTs5K4BjtI_KSXQqYMctZkzZ53XmBxw; cf_clearance=feRXjOG00aHm2RY9WQD1qJp8ibnf3IY.wHxvvoto.1s-1712665986-1.0.1.1-v.GJU92cUE7tvLeBzjRYo8lMbGu31j0yXKuQzwbFFJH.0C3LnZQkq6yqQq8RJkT.kmsG3ujECzyORBl2tn7c5w; _ga=GA1.1.1679211772.1712665988; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP8zTIAP8zTIAEsACCENAvEgAAAAAEPgACQgAAAOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEgCAAQQAEAAAAAAAQAAAAAAAAAAABAAA.YAAAAAAAAAA%22%2C%222~~dv.2072.70.89.93.108.122.149.196.2253.2299.259.2357.311.313.323.2373.338.358.2415.415.449.2506.2526.486.494.495.2568.2571.2575.540.574.2624.609.2677.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1896.1958%22%2C%2234506567-0E44-4B47-9693-27EB39C53906%22%5D%5D; __eoi=ID=ce8a6828965a381d:T=1712665990:RT=1712665990:S=AA-AfjYdB6RUfMMgkpqi5qiRp35F; _ga_LBPG8X9HFM=GS1.1.1712665987.1.1.1712666134.47.0.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'Accept-Encoding': 'gzip, deflate, br, zstd',
           'Accept-Language': 'en'
           }




# Schleife zum Durchlaufen der Seiten und Extrahieren der h2-Elemente
while True:
    # URL für die aktuelle Seite erstellen
    url = base_url
    if page_number > 1:
        url += "?p=" + str(page_number)
    

    # Webseite abrufen
    response = requests.get(url, headers=headers)
    
    # Überprüfen, ob die Seite erfolgreich abgerufen wurde
    if response.status_code == 200:
        # HTML-Inhalt der Seite extrahieren
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Alle h2-Elemente auf der Seite finden und ihre Texte zur Liste hinzufügen
        h2_elements = soup.find_all('h2')
        for h2 in h2_elements:
            h2_texts.append(h2.get_text())
        
        # Wenn keine h2-Elemente gefunden wurden, breche die Schleife ab
        if not h2_elements:
            break
        
        # Inkrementiere die Seitennummer für den nächsten Durchlauf
        page_number += 1
    else:
        # Wenn ein Fehler beim Abrufen der Seite auftritt, breche die Schleife ab
        print("Fehler beim Abrufen der Seite.")
        break

# Ausgabe der gesammelten h2-Texte
for text in h2_texts:
    print(text)
