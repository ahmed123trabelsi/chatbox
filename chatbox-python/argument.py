import openai
import pandas as pd
import sys
from openai.embeddings_utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
import re
openai.api_key = ""
sys.stdout = open('output10.txt', 'w', encoding='utf-8')

dataargument = [
    "abonnement illimité",
    "appels illimités.",
    "une garantie de vitesse de connexion ultra-rapide.",
    "une garantie de service client disponible 24/7.",
    "autres options de divertissement exclusives.",
    "l'installation gratuite.",
    "promotion exclusive pour les nouveaux clients.",
    "une réduction spéciale pour votre première commande.",
    "un cadeau gratuit avec votre achat.",
    "essai gratuit de notre service.",
    "tarifs compétitifs.",
    "programme de fidélité - bénéficiez d'avantages exclusifs.",
    "offrir un  cadeau",
    "mettre à disposition des rabais"
]

embeddings = []

for argument in dataargument:
    response = openai.Embedding.create(
        input=argument,
        model="text-embedding-ada-002"
    )
    embeddings.append(response["data"][0]["embedding"])

url = "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"

transcript = "customer:[0:00:00]Oui allo?  agent:[0:00:01]Madame Romanance?  customer:[0:00:02]Oui?  agent:[0:00:03]C'est de la part de Yalow, l'opérateur téléphonique mobile.  customer:[0:00:07]Pardon?  agent:[0:00:08]C'est Yalow, l'opérateur mobile Yalow.  customer:[0:00:11]Oui?  agent:[0:00:12]On t'ait permis de vous contacter puisque vous avez consulté le site Sapiens qui va vendre,  agent:[0:00:16]donc on revient vers vous avec les offres de Yalow.  agent:[0:00:19]Par rapport à votre abonnement actuellement, madame, celui qui se termine par 62,65, vous êtes avec Swisscal, c'est ça?  customer:[0:00:25]Oui.  customer:[0:00:00.008001]Oui  agent:[0:00:00.024997] Vous avez profité d'une offre avec Yalow ou pas encore, madame?  customer:[0:00:31]Non, mais je vais changer tout tout prochainement, là.  agent:[0:00:34]C'est-à-dire?  customer:[0:00:36]Je vais changer d'abonnement, mais ce ne sera pas chez vous, donc ce sera peut-être plus tard chez vous.  customer:[0:00:40]Là, je vais changer d'abonnement sur tous.  agent:[0:00:00.016409]Vous avez passé avec qui  agent:[0:00:00.028269] Excusez-moi, je n'ai pas entendu.  customer:[0:00:48]Mais je ne vous ai pas dit avec qui vous avez passé, parce que… qu'est-ce que vous me proposez?  customer:[0:00:52]Allez-y, dites-moi ce que vous me proposez.  agent:[0:00:00.020339]D'accord. Dites-moi, qu'est-ce que vous, vous cherchez  agent:[0:00:00.032297] Est-ce que vous cherchez uniquement en Suisse  customer:[0:00:00.032297]  customer:[0:00:00.013081]Moi, je ne cherche rien  customer:[0:00:00.036994] Moi, je ne cherche rien du tout  customer:[0:00:00.068994] Je n'ai besoin de rien  agent:[0:00:00.068994]  agent:[0:01:03]Si vous trouvez une formule intéressante, ça ne pourra pas vous intéresser?  customer:[0:01:08]Parlez-moi de votre formule.  agent:[0:00:00.008890]Oui, madame  agent:[0:00:00.014889] D'accord  agent:[0:00:00.034909] Vous avez besoin d'une offre, c'est-à-dire en Suisse seulement ou bien vers l'Europe aussi?  customer:[0:01:17]Non.  agent:[0:00:00.015997]J'ai voulu… Voilà  agent:[0:00:00.030094] Vous avez besoin uniquement en Suisse?  customer:[0:01:22]Oui.  agent:[0:01:24]Je vous propose dans ce cas-là un abonnement de tout illimité en Suisse, que ce soit les appels, Internet et SMS à 23 francs.  customer:[0:01:31]Mais là, je viens de faire un abonnement à 12 francs.  agent:[0:01:34]À 12 francs avec Internet illimité et tout ça, madame?  customer:[0:01:39]Tout.  agent:[0:00:00.009999]Si vous le dites  agent:[0:00:00.020087] Vérifiez le contrat, tout simplement  agent:[0:00:00.027003] Voilà  agent:[0:00:00.037998] Il n'y a pas de problème  customer:[0:00:00.046004] Merci  customer:[0:00:00.047002]  customer:[0:00:00.008040]Merci à vous  customer:[0:00:00.008040]"


def extract_agent_arguments(conversation):
    # Extract text segments starting with "agent:[" as potential arguments
    agent_arguments = re.findall(r"agent:\[\d+:\d+:\d+\](.*?)(?=\s*agent:|$)", conversation, flags=re.DOTALL)

    # Define the keywords for filtering agent arguments
    keywords = [
        "rabais",
        "illimité",
        "garantie",
        "divertissement",
        "gratuit",
        "promotion",
        "réduction",
        "cadeau",
        "essai gratuit",
        "offres groupées",
        "tarifs compétitifs",
        "offre limitée",
        "programme de fidélité",
        "coût",
        "limitation",
        "qualité",
        "engagement",
        "compatibilité",
        "conditions",
        "contrat",
        "À vie pour toujours",
        "options",
        "service client",
        "disponibilité",
        "flexibilité",
        "Facture gratuite chaque mois"
    ]

    # Filter agent arguments based on keywords using OpenAI's model
    filtered_arguments = []
    for argument in agent_arguments:
        # Generate response using OpenAI's API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=argument,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7
        )
        
        text = response.choices[0].text.strip()
        if any(keyword in text.lower() for keyword in keywords):
            filtered_arguments.append(text)

    return filtered_arguments

url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["Agent_arguments"]
document = collection.find_one({"url": "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"})
"""input_embedding = get_embedding(str(transcript))
embedding_data = {
    "url": url,
    "embedding": input_embedding
}
collection.insert_one(embedding_data)"""
if document:
    # Retrieve the embedding field
    embedding = document.get("embedding")
n_clusters = len(dataargument)

kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
kmeans.fit(np.array(embeddings).reshape(-1, 1))
data = [{'Review': transcript, 'Score': 5}]
df = pd.DataFrame(data)
df = df[df.Score != 3]
df['sentiment'] = df.Score.replace({1: 'negative', 2: 'negative', 4: 'positive', 5: 'positive'})
labels = ['negative', 'positive']
label_embeddings = [get_embedding(label) for label in labels]

def label_score(review_embedding, label_embeddings):
    if isinstance(review_embedding, tuple):
        review_embedding = review_embedding[0]  # Extract the desired string from the tuple

    review_embedding = get_embedding(review_embedding)
    review_embedding = np.array(review_embedding)  # Convert to NumPy array

    label_embeddings = [np.array(embedding) for embedding in label_embeddings]  # Convert label embeddings to NumPy arrays

    return (
        cosine_similarity(review_embedding.reshape(1, -1), label_embeddings[1].reshape(1, -1))
        - cosine_similarity(review_embedding.reshape(1, -1), label_embeddings[0].reshape(1, -1))
    )

prediction_score = label_score(df['Review'].values[0], label_embeddings)
if prediction_score > 0:
    prediction = 'positive'
elif prediction_score < 0:
    prediction = 'negative'
else:
    prediction = 'neutre'
arguments = extract_agent_arguments(transcript)
arguments = [arg.replace('\n', '') for arg in arguments]
predicted_cluster = kmeans.fit_predict(np.array(embedding).reshape(-1, 1))[0]
predicted_cluster_name = dataargument[predicted_cluster]
print(f"L'argument est  : {arguments}.")
print(f"L'input appartient au cluster : {predicted_cluster_name}.")
print(f"Prediction: {prediction}")
excel_file = 'fr.xlsx'
df = pd.read_excel(excel_file)
if url in df["recording_url"].values:
    index = df[df["recording_url"] == url].index[0]
    duration = df.loc[index, "duration"]
    print(f"url: {url}")
    print(f"Duration: {duration} seconds")
print("-----------------")


