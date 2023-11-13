import openai
import pandas as pd
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
import re

openai.api_key = ""
sys.stdout = open('output1embcustomer.txt', 'w', encoding='utf-8')

url = "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["Agent_arguments"]
document = collection.find_one({"url": "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"})
if document:
    # Retrieve the embedding field
    embedding = document.get("embedding")

transcript = "customer:[0:00:00]Oui allo?  agent:[0:00:01]Madame Romanance?  customer:[0:00:02]Oui?  agent:[0:00:03]C'est de la part de Yalow, l'opérateur téléphonique mobile.  customer:[0:00:07]Pardon?  agent:[0:00:08]C'est Yalow, l'opérateur mobile Yalow.  customer:[0:00:11]Oui?  agent:[0:00:12]On t'ait permis de vous contacter puisque vous avez consulté le site Sapiens qui va vendre,  agent:[0:00:16]donc on revient vers vous avec les offres de Yalow.  agent:[0:00:19]Par rapport à votre abonnement actuellement, madame, celui qui se termine par 62,65, vous êtes avec Swisscal, c'est ça?  customer:[0:00:25]Oui.  customer:[0:00:00.008001]Oui  agent:[0:00:00.024997] Vous avez profité d'une offre avec Yalow ou pas encore, madame?  customer:[0:00:31]Non, mais je vais changer tout tout prochainement, là.  agent:[0:00:34]C'est-à-dire?  customer:[0:00:36]Je vais changer d'abonnement, mais ce ne sera pas chez vous, donc ce sera peut-être plus tard chez vous.  customer:[0:00:40]Là, je vais changer d'abonnement sur tous.  agent:[0:00:00.016409]Vous avez passé avec qui  agent:[0:00:00.028269] Excusez-moi, je n'ai pas entendu.  customer:[0:00:48]Mais je ne vous ai pas dit avec qui vous avez passé, parce que… qu'est-ce que vous me proposez?  customer:[0:00:52]Allez-y, dites-moi ce que vous me proposez.  agent:[0:00:00.020339]D'accord. Dites-moi, qu'est-ce que vous, vous cherchez  agent:[0:00:00.032297] Est-ce que vous cherchez uniquement en Suisse  customer:[0:00:00.032297]  customer:[0:00:00.013081]Moi, je ne cherche rien  customer:[0:00:00.036994] Moi, je ne cherche rien du tout  customer:[0:00:00.068994] Je n'ai besoin de rien  agent:[0:00:00.068994]  agent:[0:01:03]Si vous trouvez une formule intéressante, ça ne pourra pas vous intéresser?  customer:[0:01:08]Parlez-moi de votre formule.  agent:[0:00:00.008890]Oui, madame  agent:[0:00:00.014889] D'accord  agent:[0:00:00.034909] Vous avez besoin d'une offre, c'est-à-dire en Suisse seulement ou bien vers l'Europe aussi?  customer:[0:01:17]Non.  agent:[0:00:00.015997]J'ai voulu… Voilà  agent:[0:00:00.030094] Vous avez besoin uniquement en Suisse?  customer:[0:01:22]Oui.  agent:[0:01:24]Je vous propose dans ce cas-là un abonnement de tout illimité en Suisse, que ce soit les appels, Internet et SMS à 23 francs.  customer:[0:01:31]Mais là, je viens de faire un abonnement à 12 francs.  agent:[0:01:34]À 12 francs avec Internet illimité et tout ça, madame?  customer:[0:01:39]Tout.  agent:[0:00:00.009999]Si vous le dites  agent:[0:00:00.020087] Vérifiez le contrat, tout simplement  agent:[0:00:00.027003] Voilà  agent:[0:00:00.037998] Il n'y a pas de problème  customer:[0:00:00.046004] Merci  customer:[0:00:00.047002]  customer:[0:00:00.008040]Merci à vous  customer:[0:00:00.008040]"
customer_statements = re.split(r"customer:\[\d+:\d+:\d+\](.*?)(?=\s*customer:|$)", transcript, flags=re.DOTALL)
customer_embeddings = []

for idx in range(1, len(customer_statements), 2):
    customer_text = customer_statements[idx]
    customer_index = transcript.find(customer_text)
    if customer_index != -1:
        customer_embedding = embedding[customer_index:customer_index + len(customer_text)]
        customer_embeddings.append(customer_embedding)
    else:
        print(f"Customer statement not found in transcript: {customer_text}")

for idx, customer_embedding in enumerate(customer_embeddings):
    print(f"Customer {idx+1} embedding: {customer_embedding}")
print(f"Customer  {transcript}")