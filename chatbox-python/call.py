import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from pymongo import MongoClient
import sys

# ...
sys.stdout = open('output.txt', 'w', encoding='utf-8')

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
            # Clean the transcript
            transcription = re.sub(r'[^a-zA-Zéçèàê:,\s\']', '', transcript)
            transcription = transcription.replace(":::", ":")
# Format the transcript
            transcription = re.sub(r'(\bagent:)', r'\nAgent:', transcription)
            transcription = re.sub(r'(\bcustomer:)', r'\nCustomer:', transcription)
            transcription = transcription.lower()
            duree_appels[transcription] = duration

# Tri des enregistrements par durée
recording_duration = sorted(duree_appels.items(), key=lambda x: x[1], reverse=True)

# Affichage des enregistrements et des durées
for Enregistrement, duration_sec in recording_duration:
    print(f"Enregistrement : {Enregistrement.strip()}")
    print(f"Durée : {duration_sec} secondes")
    print()



