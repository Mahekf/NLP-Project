# =========================================================
# entrainement_modele.py
# Projet NLP - Saisie prédictive téléphone
# =========================================================

print("FICHIER ENTRAINEMENT_MODELE2 LANCÉ")

import pandas as pd
import re
from sklearn.model_selection import train_test_split

from completion_freq_user import PredictiveSystem
from n_gramme_freq_user import NGramPredictor


# =========================================================
# 1. CHARGEMENT DU CORPUS SMS
# =========================================================


print("\n--- Initialisation du cerveau SMS ---")

print("Avant read_csv")
df = pd.read_excel(
    "88milsms.ods",
    engine="odf"
)

print("Après read_csv")
print(df.columns)

# On récupère uniquement les SMS non vides
if "SMS_ANON" not in df.columns:
    raise ValueError(f"Colonne SMS_ANON absente. Colonnes dispo: {df.columns}")

messages = df["SMS_ANON"].dropna().astype(str).tolist()

print(f"{len(messages)} SMS chargés.")


# =========================================================
# 2. SÉPARATION TRAIN / TEST
# =========================================================

train_sms, test_sms = train_test_split(
    messages,
    test_size=0.1,
    random_state=42
)

print(f"\nTrain : {len(train_sms)} SMS")
print(f"Test  : {len(test_sms)} SMS")


# =========================================================
# 3. INITIALISATION DES MODÈLES
# =========================================================

trie = PredictiveSystem()

# trigramme
ngram = NGramPredictor(n=2)


# =========================================================
# 4. ENTRAÎNEMENT : lit les SMS du corpus et à construit les deux modèles : complétion (Trie) et prédiction (n-grammes).
# =========================================================

print("\n--- Apprentissage en cours... ---")

for sms in train_sms:

    # apprentissage complétion
    trie.train_on_corpus(sms)

    # apprentissage prédiction
    ngram.generate_ngrams(sms)

print("--- Apprentissage terminé ! ---")


# =========================================================
# 5. ÉVALUATION SIMPLE DU MODÈLE
# =========================================================

print("\n--- Évaluation du modèle ---")

total_tests = 0
correct_predictions = 0

for sms in test_sms:

    # Tokenisation
    words = re.findall(r'\b\w+\b', sms.lower())

    # Besoin d'au moins 2 mots pour bigramme
    if len(words) < 2:
        continue

    for i in range(1, len(words)):

        contexte = words[i-1:i]
        vrai_mot = words[i]

        predictions = ngram.predict(contexte)

        if predictions:

            # top prediction
            prediction_principale = predictions[0][0]

            if prediction_principale == vrai_mot:
                correct_predictions += 1

            total_tests += 1


# Accuracy
if total_tests > 0:

    accuracy = (correct_predictions / total_tests) * 100

    print(f"Tests effectués : {total_tests}")
    print(f"Bonnes prédictions : {correct_predictions}")
    print(f"Accuracy : {accuracy:.2f}%")

else:
    print("Pas assez de données pour tester.")


# =========================================================
# 6. MODE INTERACTIF
# =========================================================

phrase_en_cours = []

print("\n=================================================")
print(" MODE CLAVIER INTELLIGENT ")
print("=================================================")

print("\nInstructions :")
print("- Tapez un mot")
print("- Tapez un numéro pour choisir une suggestion")
print("- Tapez 'exit' pour quitter")


while True:

    print("\n----------------------------------")
    print("Phrase :", " ".join(phrase_en_cours))

    saisie = input("> ").strip().lower()

    if saisie == "exit":
        break

    # =====================================================
    # COMPLÉTION DE MOT
    # =====================================================

    completions = trie.get_suggestions(saisie)

    # =====================================================
    # PRÉDICTION MOT SUIVANT
    # =====================================================

    #predictions_suite = ngram.predict(phrase_en_cours + [saisie])

    if phrase_en_cours:
        predictions_suite = ngram.predict([phrase_en_cours[-1]])
    else:
        predictions_suite = []
        
    # =====================================================
    # AFFICHAGE
    # =====================================================

    numero = 1
    dictionnaire_choix = {}

    print("\nSuggestions :")

    # ----- Complétions -----

    if completions:

        print("\n[Compléter le mot]")

        for mot, freq in completions[:3]:

            print(f"{numero}. {mot} ({freq})")

            dictionnaire_choix[str(numero)] = mot

            numero += 1

    # ----- Mot suivant -----

    if predictions_suite:

        print("\n[Mot suivant]")

        for mot, freq in predictions_suite[:3]:

            print(f"{numero}. {mot} ({freq})")

            dictionnaire_choix[str(numero)] = mot

            numero += 1

    # =====================================================
    # CHOIX UTILISATEUR
    # =====================================================

    choix = input("\nVotre choix : ").strip().lower()

    # Choix via numéro
    if choix in dictionnaire_choix:

        mot_final = dictionnaire_choix[choix]

    # Nouveau mot tapé
    else:

        mot_final = choix if choix else saisie

    # =====================================================
    # APPRENTISSAGE TEMPS RÉEL
    # =====================================================

    # ajout au trie
    trie.insert(mot_final)

    # ajout au modèle n-gramme
    if len(phrase_en_cours) >= ngram.n - 1:

        contexte = tuple(
            phrase_en_cours[-(ngram.n - 1):]
        )

        ngram.update_model(
            contexte,
            mot_final
        )

    # =====================================================
    # AJOUT À LA PHRASE
    # =====================================================

    phrase_en_cours.append(mot_final)


print("\n--- Fin du programme ---")