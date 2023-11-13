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
sys.stdout = open('output11.txt', 'w', encoding='utf-8')


url = "https://api.twilio.com/2010-04-01/Accounts/AC4fe689d01a8614e6572adb5df245497b/Recordings/RE671ba637f68fe8467f7c9cfa9cfce481"

transcript = "customer:[0:00:00]Oui allo?  agent:[0:00:01]Madame Romanance?  customer:[0:00:02]Oui?  agent:[0:00:03]C'est de la part de Yalow, l'opérateur téléphonique mobile.  customer:[0:00:07]Pardon?  agent:[0:00:08]C'est Yalow, l'opérateur mobile Yalow.  customer:[0:00:11]Oui?  agent:[0:00:12]On t'ait permis de vous contacter puisque vous avez consulté le site Sapiens qui va vendre,  agent:[0:00:16]donc on revient vers vous avec les offres de Yalow.  agent:[0:00:19]Par rapport à votre abonnement actuellement, madame, celui qui se termine par 62,65, vous êtes avec Swisscal, c'est ça?  customer:[0:00:25]Oui.  customer:[0:00:00.008001]Oui  agent:[0:00:00.024997] Vous avez profité d'une offre avec Yalow ou pas encore, madame?  customer:[0:00:31]Non, mais je vais changer tout tout prochainement, là.  agent:[0:00:34]C'est-à-dire?  customer:[0:00:36]Je vais changer d'abonnement, mais ce ne sera pas chez vous, donc ce sera peut-être plus tard chez vous.  customer:[0:00:40]Là, je vais changer d'abonnement sur tous.  agent:[0:00:00.016409]Vous avez passé avec qui  agent:[0:00:00.028269] Excusez-moi, je n'ai pas entendu.  customer:[0:00:48]Mais je ne vous ai pas dit avec qui vous avez passé, parce que… qu'est-ce que vous me proposez?  customer:[0:00:52]Allez-y, dites-moi ce que vous me proposez.  agent:[0:00:00.020339]D'accord. Dites-moi, qu'est-ce que vous, vous cherchez  agent:[0:00:00.032297] Est-ce que vous cherchez uniquement en Suisse  customer:[0:00:00.032297]  customer:[0:00:00.013081]Moi, je ne cherche rien  customer:[0:00:00.036994] Moi, je ne cherche rien du tout  customer:[0:00:00.068994] Je n'ai besoin de rien  agent:[0:00:00.068994]  agent:[0:01:03]Si vous trouvez une formule intéressante, ça ne pourra pas vous intéresser?  customer:[0:01:08]Parlez-moi de votre formule.  agent:[0:00:00.008890]Oui, madame  agent:[0:00:00.014889] D'accord  agent:[0:00:00.034909] Vous avez besoin d'une offre, c'est-à-dire en Suisse seulement ou bien vers l'Europe aussi?  customer:[0:01:17]Non.  agent:[0:00:00.015997]J'ai voulu… Voilà  agent:[0:00:00.030094] Vous avez besoin uniquement en Suisse?  customer:[0:01:22]Oui.  agent:[0:01:24]Je vous propose dans ce cas-là un abonnement de tout illimité en Suisse, que ce soit les appels, Internet et SMS à 23 francs.  customer:[0:01:31]Mais là, je viens de faire un abonnement à 12 francs.  agent:[0:01:34]À 12 francs avec Internet illimité et tout ça, madame?  customer:[0:01:39]Tout.  agent:[0:00:00.009999]Si vous le dites  agent:[0:00:00.020087] Vérifiez le contrat, tout simplement  agent:[0:00:00.027003] Voilà  agent:[0:00:00.037998] Il n'y a pas de problème  customer:[0:00:00.046004] Merci  customer:[0:00:00.047002]  customer:[0:00:00.008040]Merci à vous  customer:[0:00:00.008040]"


def extract_agent_arguments(conversation):
    # Extract text segments starting with "agent:[" as potential arguments
    agent_arguments = re.findall(r"agent:\[\d+:\d+:\d+\](.*?)(?=\s*customer:|\s*agent:|$)", conversation, flags=re.DOTALL)
    
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

    filtered_arguments = []
    for argument in agent_arguments:
        # Check if the argument contains a question from the agent
        if any(keyword in argument.lower() for keyword in keywords) :
            filtered_arguments.append(argument)

    return filtered_arguments

def extract_agent_arguments_with_condition(conversation):
    # Split the conversation by customer statements
    customer_statements = re.split(r"customer:\[\d+:\d+:\d+\](.*?)(?=\s*customer:|$)", conversation, flags=re.DOTALL)

    # Extract agent arguments from each customer statement and apply filtering
    filtered_arguments = []
    for statement in customer_statements:
        arguments = extract_agent_arguments(statement)
        if arguments:
            # Find the index of "mais je fais d'abonnement" in the customer statement
            index = statement.find("Mais là, je viens de faire un abonnement")
            if index != -1:
                # If the index is found, consider all arguments except the one immediately after
                arguments_before = [arg for arg in arguments if statement.find(arg) < index]
                filtered_arguments.extend(arguments_before)
            else:
                # If the index is not found, consider all arguments from the statement
                filtered_arguments.extend(arguments)

    return filtered_arguments

arguments = extract_agent_arguments_with_condition(transcript)
print(f"L'argument est : {arguments}.")
