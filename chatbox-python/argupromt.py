import openai
import sys
from pymongo import MongoClient

url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["rejection_argument"]
url = "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/REafb1c3c56bd8840ce3c0b663acf2f4cb"
sys.stdout = open('outputargumentdata.txt', 'w', encoding='utf-8')
openai.api_key = ""

contexte = "customer:[0:00:00]Allo?  agent:[0:00:01]Oui, bonjour.  customer:[0:00:02]Bonjour.  agent:[0:00:03]Monsieur Gilles Lindeja?  customer:[0:00:05]Oui, pourquoi?  agent:[0:00:06]C'est l'opérateur téléphonique Yalow, je vous ai contacté l'autre jour, monsieur.  customer:[0:00:10]Ah oui, vous êtes de base, c'est ça?  agent:[0:00:13]Voilà, c'est l'opérateur téléphonique Yalow.  customer:[0:00:16]Oui.  agent:[0:00:17]Je vous ai contacté concernant les nouvelles offres de Yalow, monsieur.  customer:[0:00:24]Oui, mais je vais bientôt avoir le changement au mois de juin, c'est bon.  agent:[0:00:28]D'accord, ça c'est avec Yalow, c'est ça?  customer:[0:00:31]Voilà, c'est ça, oui.  agent:[0:00:33]Et pour Internet à la maison, monsieur, vous êtes avec qui?  customer:[0:00:36]Pour le moment, je suis avec UPC.  agent:[0:00:39]Très très bien.  agent:[0:00:40]Avec UPC, votre abonnement, il vous coûte combien mensuellement, s'il vous plaît?  customer:[0:00:44]Oh, j'ai pu tous les détails, mais le changement va flir bientôt, monsieur, avec Yalow.  customer:[0:00:49]C'est bon.  agent:[0:00:50]Oui, non, non, ça c'est pour la partie Nathel, on est bien d'accord.  agent:[0:00:53]Je parle pour la partie Internet à la maison, parce que pour les personnes qui ont des abonnements avec Yalow,  agent:[0:01:00]ils profiteront des offres très intéressantes pour la partie Internet, et surtout que vous, vous êtes avec UPC,  agent:[0:01:06]donc on garde la même technologie.  agent:[0:01:08]Par contre, pour la partie facturation, on peut vous proposer une formule moins chère par rapport à ce que vous avez.  agent:[0:01:13]Parce que c'est bien plus cher que vous, vous êtes au minimum à 58, 60 francs par mois, pour la partie Internet.  customer:[0:01:19]Oui, c'est plus.  customer:[0:01:20]Oui?  customer:[0:01:21]Oui, je sais plus.  agent:[0:01:22]Oui, voilà, c'est ça, l'offre basique, bien sûr, de UPC.  agent:[0:01:25]Puisque c'est UPC de Sunrise, et nous, on est Yalow de Sunrise.  customer:[0:01:29]Oui, oui, oui, mais j'ai mon vendeur qui va faire le nécessaire au mois de juin, là, c'est bon.  customer:[0:01:36]Le basculement va se faire.  agent:[0:00:00.015989]Vous parlez de quoi, monsieur  agent:[0:00:00.035103] Vous parlez de l'Internet à la maison ou bien du Nathel  customer:[0:00:00.036108]  customer:[0:01:41]De tout, de tout, du tout, l'Internet, la télé et le téléphone, voilà.  agent:[0:01:47]D'accord, il n'y a pas de problème, merci infiniment.  customer:[0:00:00.046537]OK, merci monsieur, c'est gentil, merci  agent:[0:00:00.046537]"


prompt_rejection = f" Voici le contexte :\n\n{contexte}\nau début du contexte afficher uniquement et exactement ce que le client a dit  de sa raison de désintérêt :"
prompt_argument = f" Voici le contexte :\n\n{contexte}\n au début du contexte afficher uniquement et exactement ce que l'agent a dit  juste après la justification de désintérêt du client : "

response_rejection = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_rejection ,
    temperature=0.2,
    max_tokens=100,
)

rejection_reason = response_rejection.choices[0].text.strip()
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_argument,
    temperature=0.2,
    max_tokens=100,
)

contre_arguments = response.choices[0].text.strip()

print(f" le contre_argument est :{contre_arguments}")
print(f" le raison de rejection est :{rejection_reason}")

argument_reason_data = {
    "url": url,
    "contre_arguments":contre_arguments,
    "rejection_reason":rejection_reason,
}
collection.insert_one(argument_reason_data)


document = collection.find_one({"url":"https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/REafb1c3c56bd8840ce3c0b663acf2f4cb"})
if document:
    print(document)

