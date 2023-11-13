from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Connect to MongoDB
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["Agent_arguments"]

# Find the document containing the URL
document = collection.find_one({"url": "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"})

if document:
    # Retrieve the embedding field
    embedding = document.get("embedding")

    if embedding:
        # Print the embedding
        print(embedding)
    else:
        print("Embedding not found in the document.")
else:
    print("Document not found.")

# Close the MongoDB connection
client.close()
