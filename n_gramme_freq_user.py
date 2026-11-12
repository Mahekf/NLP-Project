import re

# Cet code fonctionne bien : compte les fréquences + ajout des nouveaux mots 

class NGramPredictor:
    def __init__(self, n=2):
        self.n = n
        self.model = {}

    """ def generate_ngrams(self, text):
        words = re.findall(r'\b\w+\b', text.lower()) # résout le problème de "Ponctuation" + Unification (tout en minuscule) + le problème de Tokenisation (Par ex : chou-fleur --> deux mots)
        if len(words) < self.n:
            return
        for i in range(len(words) - self.n + 1):
            window = words[i : i + self.n]
            context = tuple(window[:-1])
            target = window[-1]
            self.update_model(context, target) """
    
    def generate_ngrams(self, text):
        # 1. On découpe d'abord le texte en phrases (en utilisant le point, ! ou ?)
        # On utilise une expression régulière pour couper proprement. Pour ne pas prendre en compte les mots suivants dont la phrase se termine par . / ? / !
        phrases = re.split(r'[.!?]+', text)
        
        for phrase in phrases:
            # 2. Pour chaque phrase, on extrait les mots 
            words = re.findall(r'\b\w+\b', phrase.lower())
            
            # 3. On ne crée des n-grammes que si la phrase est assez longue
            if len(words) < self.n:
                continue

            # 4. On fait glisser la fenêtre UNIQUEMENT à l'intérieur de cette phrase
            for i in range(len(words) - self.n + 1):
                window = words[i : i + self.n]
                context = tuple(window[:-1])
                target = window[-1]
                self.update_model(context, target)


    def update_model(self, context, target, count=1):
        if context not in self.model:
            self.model[context] = {}
        if target not in self.model[context]:
            self.model[context][target] = 0
        self.model[context][target] += count

    def predict(self, prev_words_list):
        if len(prev_words_list) < self.n - 1:
            return []
        # Unification (tout en minuscule)
        context = tuple(w.lower() for w in prev_words_list[-(self.n-1):])
        
        if context not in self.model:
            return []
        
        predictions = self.model[context]
        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)

# --- PROGRAMME INTERACTIF ---

# On utilise n=3 pour que ce soit plus réactif (besoin de seulement 2 mots de contexte)
predictor = NGramPredictor(n=3)
corpus = "Le chat mange une souris. Le chat dort sur le tapis. Le chat mange du poisson. Le chat est gris. Le chat saute haute. Il est beau"
predictor.generate_ngrams(corpus)

phrase_en_cours = []

#print("=== CLAVIER INTELLIGENT (n=3) ===")
print("Instructions : Tapez un mot, ou le chiffre de la suggestion.")
print("Tapez 'exit' pour quitter.")

while True:
    # 1. Affichage de la phrase actuelle
    current_phrase = " ".join(phrase_en_cours)
    print(f"\nPhrase : {current_phrase if phrase_en_cours else '[Vide]'}")
    
    # 2. On récupère les suggestions basées sur les derniers mots
    suggestions = predictor.predict(phrase_en_cours)
    
    if suggestions:
        print("Suggestions : ", end="")
        for i, (mot, score) in enumerate(suggestions[:3]): # On montre le top 3
            print(f"{i+1}. {mot} ({score})  ", end="")
        print()
    else:
        print("[Aucune suggestion]")

    # 3. Saisie de l'utilisateur
    saisie = input("> ").strip()

    if saisie.lower() == 'exit':
        break

    # 4. Traitement du choix (chiffre ou nouveau mot)
    if saisie.isdigit() and suggestions:
        idx = int(saisie) - 1
        if 0 <= idx < len(suggestions):
            mot_final = suggestions[idx][0]
        else:
            print("Chiffre invalide.")
            continue
    else:
        mot_final = saisie.lower()

    # 5. APPRENTISSAGE EN TEMPS RÉEL
    # Si on a assez de mots pour créer un contexte, on apprend le lien
    if len(phrase_en_cours) >= predictor.n - 1:
        # On prend les n-1 derniers mots de la phrase comme contexte
        dernier_contexte = tuple(w.lower() for w in phrase_en_cours[-(predictor.n-1):])
        # On lie ce contexte au mot que l'utilisateur vient de valider
        predictor.update_model(dernier_contexte, mot_final)
        print(f" (Appris : {dernier_contexte} -> {mot_final})")

    # 6. On ajoute le mot à la phrase
    phrase_en_cours.append(mot_final)