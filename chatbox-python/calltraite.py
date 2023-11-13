import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ...
import pandas as pd
from pymongo import MongoClient
import sys

# Rediriger la sortie vers un fichier texte avec encodage UTF-8
sys.stdout = open('output3.txt', 'w', encoding='utf-8')

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
            # Prétraitement de la transcription
            transcription = re.sub(r'[^a-zA-Zéçèàê:,\s\']', '', transcript)
            transcription = transcription.replace(":::", ":")
# Format the transcript
            transcription = re.sub(r'(\bagent:)', r'\nAgent:', transcription)
            transcription = re.sub(r'(\bcustomer:)', r'\nCustomer:', transcription)
            transcription = transcription.lower()
          

            stopwords_fr = set(stopwords.words('french'))
            transcription = ' '.join([word for word in transcription.split() if word not in stopwords_fr])

            lemmatizer = WordNetLemmatizer()
            transcription = ' '.join([lemmatizer.lemmatize(word) for word in transcription.split()])
            transcription = ' '.join([word for word in transcription.split() if len(word) > 2])

            duree_appels[transcription] = duration

# Tri des enregistrements par durée
recording_duration = sorted(duree_appels.items(), key=lambda x: x[1], reverse=True)

# Affichage des enregistrements et des durées
for transcript_text, duration_sec in recording_duration:
    print(f"Enregistrement : {transcript_text.strip()}")
    print(f"Durée : {duration_sec} secondes")
    print()
