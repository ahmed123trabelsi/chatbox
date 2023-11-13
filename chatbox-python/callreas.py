import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from pymongo import MongoClient
import sys

sys.stdout = open('output1.txt', 'w', encoding='utf-8')

# Charger le modèle pré-entraîné de classification de texte en français
nlp_classification = spacy.load("fr_core_news_sm")

# Charger le modèle pré-entraîné de reconnaissance d'entités nommées en français
nlp_ner = spacy.load("fr_core_news_sm")

# Download required resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Load French language model for spaCy
nlp = spacy.load('fr_core_news_sm')

# Prétraitement et classification
def preprocess_text(text):
    # Nettoyer le texte
    text = re.sub(r'[^a-zA-Zéçèàê:,\s\']', '', text)
    text = text.replace(":::", ":")
    text = text.lower()

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Supprimer les mots vides
    stopwords_fr = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stopwords_fr]

    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(lemmas)

def extract_entities(transcript):
    doc = nlp_ner(transcript)

    rejection_reasons = []
    agent_arguments = []

    for ent in doc.ents:
        if ent.label_ == "REJET_REASON":
            rejection_reasons.append(ent.text)
        elif ent.label_ == "AGENT_ARGUMENT":
            agent_arguments.append(ent.text)

    return rejection_reasons, agent_arguments

# Données annotées
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

dataargument = [
    ("J'ai des offres spéciales juste pour vous.", "proposition offre spéciale"),
    ("Je mets à disposition des rabais allant jusqu'à 70 %.", "offre avec réduction de prix"),
    ("J'ai des appels illimités.", "offre avec appels illimités"),
    ("Je t'offre une garantie de vitesse de connexion ultra-rapide.", "offre avec vitesse de connexion élevée"),
    ("Je t'offre une garantie de service client disponible 24/7.", "offre avec assistance client disponible en tout temps"),
    ("J'ai d'autres options de divertissement exclusives.", "offre avec options de divertissement exclusives"),
    ("Je t'offre l'installation gratuite.", "offre avec installation sans frais"),
    ("Je t'offre un forfait tout-en-un.", "offre avec services regroupés"),
    ("J'ai un autre accès premium.", "offre avec accès à des chaînes haut de gamme"),
]



# Charger les transcriptions, les raisons de rejet et les arguments de l'agent
transcriptionsraison, raisons_rejet = zip(*dataraison)
transcriptionsargument, argumentagent = zip(*dataargument)

# Vectorisation des transcriptions
vectorizer = TfidfVectorizer(preprocessor=preprocess_text)

# Transformer les données d'entraînement
X_train = vectorizer.fit_transform(transcriptionsraison)
Y_train = vectorizer.transform(transcriptionsargument)

# Entraînement du modèle de classification
model_rejection_reason = LinearSVC()
model_rejection_reason.fit(X_train, raisons_rejet)

model_agent_argument = LinearSVC()
model_agent_argument.fit(Y_train, argumentagent)



# Load data from MongoDB and perform classification and NER
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collections = db["Call_Records_Transcripts"]
excel_file = 'fr.xlsx'
df = pd.read_excel(excel_file)
duree_appels = {}


for document in collections.find():
    transcript = document.get("transcript")
    url = document.get("url")

    if url in df["recording_url"].values:
        index = df[df["recording_url"] == url].index[0]
        duration = df.loc[index, "duration"]

        if transcript and duration:
            # Classification
            X_transcript = vectorizer.transform([preprocess_text(transcript)])  # Appliquer le prétraitement
            predictionrejet = model_rejection_reason.predict(X_transcript)
            rejection_reason = predictionrejet[0]
            predictionargument = model_agent_argument.predict(X_transcript)
            agent_arguments = predictionargument[0]
            # NER
        
            

            duree_appels[url] = {
                'transcript': transcript,
                'duration': duration,
                'rejection_reason': rejection_reason,
                'agent_arguments': agent_arguments
            }

# Sort recordings by duration
recording_duration = sorted(duree_appels.items(), key=lambda x: x[1]['duration'], reverse=True)

# Display the results
for url, info in recording_duration:
    print(f"url: {url}")
   # print(f"Recording: {info['transcript'].strip()}")
    print(f"Duration: {info['duration']} seconds")
    print("Rejection Reason:", info['rejection_reason'])
  
    print("agent argument:", info['agent_arguments'])
    print()
