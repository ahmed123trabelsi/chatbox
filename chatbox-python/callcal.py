import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import spacy
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import sys

sys.stdout = open('output4.txt', 'w', encoding='utf-8')

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

# Preprocessing and Classification
def preprocess_text(text):
    # Clean the text
    text = re.sub(r'[^a-zA-Zéçèàê:,\s\']', '', text)
    text = text.replace(":::", ":")
    text = text.lower()

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    stopwords_fr = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stopwords_fr]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(lemmas)

def classify_text(transcription):
    preprocessed_text = preprocess_text(transcription)

    train_data = [
        ("Cette offre est vraiment avantageuse pour vous.", "Acceptation d interaction"),
        ("Ne manquez pas cette occasion unique !", "Acceptation d interaction"),
        ("Notre offre exclusive vous fera économiser de l'argent.", "Acceptation d interaction"),
        ("Nous avons les meilleurs prix sur le marché.", "Acceptation d interaction"),
        ("Malheureusement, nous ne pouvons pas offrir de réduction supplémentaire.", "rejet"),
        ("Le prix de notre offre est fixe et non négociable.", "rejet"),
        ("Nous ne pouvons pas répondre à votre demande de réduction.", "rejet"),
        ("Nous n'avons pas d'offres spéciales en ce moment.", "rejet")
    ]

    # Convertir les données en DataFrame pandas
    df_train = pd.DataFrame(train_data, columns=['text', 'label'])

    # Séparer les données en features (X) et labels (y)
    X_train = df_train['text']
    y_train = df_train['label']

    # Créer une instance du vectoriseur TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    # Appliquer le vectoriseur TF-IDF sur les données d'entraînement
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

    # Créer un modèle SVM
    svm_model = LinearSVC()

    # Entraîner le modèle SVM sur les données d'entraînement
    svm_model.fit(X_train_tfidf, y_train)

    # Prétraiter le texte d'entrée
    preprocessed_text = preprocess_text(transcription)

    # Appliquer le vectoriseur TF-IDF sur le texte d'entrée prétraité
    text_tfidf = tfidf_vectorizer.transform([preprocessed_text])

    # Prédire le label du texte d'entrée avec le modèle entraîné
    predicted_label = svm_model.predict(text_tfidf)

    # Return the predicted label or class
    return predicted_label[0]


# Named Entity Recognition (NER)
# def extract_entities(transcription):
#     doc = nlp(transcription)

#     entities = []
#     for ent in doc.ents:
#         entities.append((ent.text, ent.label_))

#     return entities


# Load data from MongoDB and perform classification and NER
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collections = db["Call_Records_Transcripts"]
excel_file = 'fr.xlsx'
df = pd.read_excel(excel_file)
duree_appels = {}
threshold = 0.5 
for document in collections.find():
    transcript = document.get("transcript")
    url = document.get("url")

    if url in df["recording_url"].values:
        index = df[df["recording_url"] == url].index[0]
        duration = df.loc[index, "duration"]

        if transcript and duration:
            # Classification
            predicted_label = classify_text(transcript)
            doc_classification = nlp_classification(transcript)

            if predicted_label == "Acceptation d interaction":
                classification_label = "Acceptation d interaction"
            else:
                classification_label = "rejet"

            # NER
          
        duree_appels[url] = {
            'transcript': transcript,
            'duration': duration,
            'classification': classification_label
        }

# Sort recordings by duration
recording_duration = sorted(duree_appels.items(), key=lambda x: x[1]['duration'], reverse=True)

# Display the results
for url, info in recording_duration:
    print(f"url: {url}")
    print(f"Recording: {info['transcript'].strip()}")
    print(f"Duration: {info['duration']} seconds")
    print(f"Classification: {info['classification']}")
    print()
