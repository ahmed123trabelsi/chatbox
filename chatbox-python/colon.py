from pymongo import MongoClient 
url_mongo = "mongodb+srv://ahmed:ahmed@cluster0.iaanx.mongodb.net/Twilio?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client['Twilio_DB']
collection = db["Agent_arguments"]# Fetch a single document from the collection
document = collection.find_one()

# Get the column names (field names)
column_names = list(document.keys())

# Print the column names
for column in column_names:
    print(column)
