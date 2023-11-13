import pandas as pd
from pymongo import MongoClient
import sys

# Rediriger la sortie vers un fichier texte avec encodage UTF-8
sys.stdout = open('output2.txt', 'w', encoding='utf-8')

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
            duree_appels[transcript] = duration

recording_duration= sorted(duree_appels.items(), key=lambda x: x[1], reverse=True)
# Affichage des contre-arguments classés par qualité
for transcript_text, duration_sec in recording_duration:
    print(f"recordings : {transcript_text}")
    print(f"duration: {duration_sec} secondes")
    print()

