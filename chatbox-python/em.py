import openai
import pandas as pd
import sys
from openai.embeddings_utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
import re
dataargument = [
    ("mettre à disposition des rabais"),
    ("appels illimités."),
    ("une garantie de vitesse de connexion ultra-rapide."),
    ("une garantie de service client disponible 24/7."),
    ("autres options de divertissement exclusives."),
    ("l'installation gratuite."),
    ("accès premium."),
    ("promotion exclusive pour les nouveaux clients."),
    ("une réduction spéciale pour votre première commande."),
    ("un cadeau gratuit avec votre achat."),
    ("essai gratuit de notre service."),
    ("économisez de l'argent avec nos offres groupées."),
    ("un bon de réduction."),
    ("tarifs compétitifs."),
    ("Offre limitée dans le temps."),
    ("programme de fidélité - bénéficiez d'avantages exclusifs."),
    ("offrir un petit cadeau"),
    ("abonnement illimité")
]