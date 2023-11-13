import openai
import sys
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
sys.stdout = open('output12.txt', 'w', encoding='utf-8')
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["Agent_arguments"]
document = collection.find_one({"url": "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"})

# Initialize OpenAI API client (Assuming you have the correct setup for openai)
openai.api_key = ""

dataargument = [
    "une garantie de vitesse de connexion ultra-rapide.",
    "l'installation gratuite.",
    "abonnement illimité",
    "promotion exclusive pour les nouveaux clients.",
    "une réduction spéciale pour votre première commande.",
    "un cadeau gratuit avec votre achat.",
    "essai gratuit de notre service.",
    "tarifs compétitifs.",
    "programme de fidélité - bénéficiez d'avantages exclusifs.",
    "offrir un cadeau",
    "mettre à disposition des rabais"
]

# Create embeddings for each argument
embeddings = []

for argument in dataargument:
    response = openai.Embedding.create(
        input=argument,
        model="text-embedding-ada-002"
    )
    embedding_vector = response["data"][0]["embedding"]
    embeddings.append(embedding_vector)  # Append the embedding to the list
    
    embedding_data = {
        "argument": argument,
        "embedding_argument": embedding_vector
    }
    
    db["Argument_embeddings"].insert_one(embedding_data)
    
# Fit KMeans using the embeddings
n_clusters = len(dataargument)
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
kmeans.fit(np.array(embeddings).reshape(-1, 1))

# Predict the cluster for the provided embedding (from your document)
if document:
    embedding = document.get("embedding")
    predicted_cluster = kmeans.predict(np.array([embedding]).reshape(-1, 1))[0]  # Corrected prediction
    predicted_cluster_name = dataargument[predicted_cluster]
    print(f"L'input appartient au cluster : {predicted_cluster_name}.")
