import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import requests
from time import sleep
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.svm import LinearSVC
from pymongo import MongoClient
from nltk.sentiment import SentimentIntensityAnalyzer
import sys

sys.stdout = open('output8.txt', 'w', encoding='utf-8')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('vader_lexicon')

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z1-9éçèàê:%,\s\']', '', text)
    text = text.replace(":::", ":")
    text = text.replace("[:::]", "")
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    stopwords_fr = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stopwords_fr]
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmas)

dataraison = [
    ("Je viens de changer de fournisseur.", "changement_abonnement"),
    ("J'ai des problèmes à téléphone.", "téléphone en panne"),
    ("Je n'ai pas besoin de ce service.", "pas_besoin"),
    ("Le prix est trop élevé pour moi.", "prix_élevé"),
    ("Je parle pas français, anglais, allemand, espagnol", "autre_langue"),
    ("Je suis occupé.", "client occupé"),
    ("Pourquoi m'avez-vous appelé alors?", "client mécontent : demande de justification de la source du numéro de téléphone"),
    ("J'ai déjà un abonnement avec un autre opérateur.", "abonnement existant"),
    ("Je préfère une connexion filaire plutôt que WiFi.", "préférence connexion filaire"),
    ("Je suis en déplacement fréquent et n'ai pas besoin d'un abonnement fixe.", "déplacement fréquent"),
]

data_argument = [
    (" mettre à disposition des rabais "),
    (" appels illimités."),
    (" une garantie de vitesse de connexion ultra-rapide."),
    (" une garantie de service client disponible 24/7."),
    ("autres options de divertissement exclusives."),
    ("l'installation gratuite."),
    (" accès premium."),
    (" promotion exclusive pour les nouveaux clients."),
    ("une réduction spéciale  première commande."),
    ("un cadeau gratuit  votre achat."),
    ("essai gratuit de notre service."),
    ("économisez de l'argent avec nos offres groupées."),
    (" un bon de réduction."),
    (" tarifs compétitifs."),
    ("Offre limitée dans le temps occasion."),
    (" programme de fidélité  bénéficiez d'avantages exclusifs."),
]

transcriptionsraison, raisons_rejet = zip(*dataraison)

transcriptions = []
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collections = db["Call_Records_Transcripts"]
excel_file = 'fr.xlsx'
df = pd.read_excel(excel_file)
duree_appels = {}

vectorizer = TfidfVectorizer(preprocessor=preprocess_text)

X_train = vectorizer.fit_transform(transcriptionsraison)
# Extraction des mots-clés pour chaque transcription
vectorizer_y = TfidfVectorizer(preprocessor=preprocess_text)
X_train_y = vectorizer_y.fit_transform(data_argument)

num_clusters = len(transcriptionsraison)  # Nombre de clusters à former
kmeans = KMeans(n_clusters=num_clusters, n_init=5)
kmeans.fit(X_train_y)

feature_names_y = vectorizer_y.get_feature_names_out()
sorted_centroids_y = kmeans.cluster_centers_.argsort()[:, ::-1]

arguments = []
for cluster_id in range(num_clusters):
    top_words = [feature_names_y[idx] for idx in sorted_centroids_y[cluster_id, :8]]
    arguments.append(top_words)

model_rejection_reason = LinearSVC()
model_rejection_reason.fit(X_train, raisons_rejet)

model_ARGUMENT = LinearSVC()
model_ARGUMENT.fit(X_train_y, data_argument)

sia = SentimentIntensityAnalyzer()

for document in collections.find():
    transcript = document.get("transcript")
    url = document.get("url")

    if url in df["recording_url"].values:
        index = df[df["recording_url"] == url].index[0]
        duration = df.loc[index, "duration"]

        transcriptions.append(transcript)

        if transcript and duration:
            X_transcript = vectorizer.transform([preprocess_text(transcript)])
            prediction_rejet = model_rejection_reason.predict(X_transcript)
            rejection_reason = prediction_rejet[0]

            X_transcript_y = vectorizer_y.transform([preprocess_text(transcript)])
            cluster_id = kmeans.predict(X_transcript_y)[0]
            agent_argument = arguments[cluster_id]

            sentiment_score = sia.polarity_scores(transcript)
            sentiment = sentiment_score['compound']

            duree_appels[url] = {
                'transcript': transcript,
                'duration': duration,
                'rejection_reason': rejection_reason,
                'agent_arguments': agent_argument,
                'sentiment': sentiment
            }

recording_duration = sorted(duree_appels.items(), key=lambda x: x[1]['duration'], reverse=True)

for url, info in recording_duration:
    print(f"url: {url}")
    print(f"Duration: {info['duration']} seconds")
    print("Rejection Reason:", info['rejection_reason'])
    print("Agent Arguments:")
    print("-   ", info['agent_arguments'])
    print("score sentiment:",info['sentiment'])
    sentiment = info['sentiment']
    if sentiment > 0:
        print("Sentiment: Positive")
    elif sentiment < 0:
        print("Sentiment: Negative")
    else:
        print("Sentiment: Neutre")
    print()

