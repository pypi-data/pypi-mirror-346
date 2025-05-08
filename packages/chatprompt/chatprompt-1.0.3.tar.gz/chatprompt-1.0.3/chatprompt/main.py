from bs4 import BeautifulSoup
import requests


description = ""

def personalization(desc):
    global description
    description = desc + "\n"

def prompt(message):

    url = 'https://ile-reunion.org/gpt3/resultat'

    if(description is not None):
        data = {
                'D1': 'Option sortie audio',
                'exemple-prompt': 'Exemples de prompt',
                'xscreen': '1280',
                'yscreen': '800',
                'question': f"Here is some information about me. Please do not respond to this introduction as it is only to help you understand me better and make your responses more relevant. Do not say 'thank you' for the introduction or anything unnecessary. Just focus on responding directly to my message: {description} and here is my message: {message}"
            }
    else:
        data = {
                'D1': 'Option sortie audio',
                'exemple-prompt': 'Exemples de prompt',
                'xscreen': '1280',
                'yscreen': '800',
                'question': message
            }
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'fr-FR',
            'Referer': 'https://ile-reunion.org/gpt3/',
        }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        for center in soup.find_all("center"):
                center.decompose()

        div_message = soup.find("div", class_="affichage")

        if div_message:
            for br in div_message.find_all("br"):
                br.replace_with("\n")

            texte_final = div_message.get_text(separator="\n", strip=True)

            lignes = texte_final.split("\n")
            
            lignes = [ligne for ligne in lignes if "Résultat :" not in ligne and "Posez une autre question" not in ligne and "Requêtes" not in ligne]

            texte_final_filtré = "\n".join(lignes)

            return texte_final_filtré
        else:
            print("Div avec class 'affichage' non trouvée")

    else:
        print(f"Erreur lors de la requête : {response.status_code}")