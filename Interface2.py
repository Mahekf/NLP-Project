import pandas as pd
import re
import tkinter as tk
import customtkinter as ctk
from completion_freq_user import PredictiveSystem 
from n_gramme_freq_user import NGramPredictor 

# =========================================================================
# 1. INITIALISATION ET CHARGEMENT DU CERVEAU IA
# =========================================================================
print("--- Chargement des données et entraînement de l'IA ---")

# Chargement du fichier .ods avec l'engine odf
df = pd.read_excel('88milsms.ods', engine='odf')
messages = df['SMS_ANON'].dropna().astype(str).tolist()

trie = PredictiveSystem()
ngram = NGramPredictor(n=3)

# Entraînement sur tout ton corpus de SMS
for sms in messages:
    trie.train_on_corpus(sms)  
    ngram.generate_ngrams(sms)

print("--- IA prête pour l'interface graphique ! ---")

# =========================================================================
# 2. CONFIGURATION DE L'INTERFACE GRAPHIQUE (CustomTkinter)
# =========================================================================
ctk.set_appearance_mode("dark")  # Mode Sombre
ctk.set_default_color_theme("blue")  # Boutons bleus par défaut

class ApplicationPredictive(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clavier Prédictif SMS - Projet TAL")
        self.geometry("600x480")  # Hauteur légèrement augmentée pour l'espace des smileys
        self.resizable(False, False)

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(self, text="Editeur de Texte", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=15)

        # --- ZONE DE TEXTE (Champ de saisie) ---
        self.text_label = ctk.CTkLabel(self, text="Tapez votre message ici :", font=ctk.CTkFont(size=14))
        self.text_label.pack(anchor="w", padx=25, pady=(10, 2))

        self.textbox = ctk.CTkTextbox(self, width=550, height=150, font=ctk.CTkFont(size=15))
        self.textbox.pack(padx=20, pady=5)
        
        # Écoute le clavier en temps réel pendant la frappe
        self.textbox.bind("<KeyRelease>", self.analyser_saisie)

        # --- ZONE D'AFFICHAGE DES SUGGESTIONS (Placée en dessous du texte) ---
        self.suggestions_frame = ctk.CTkFrame(self)
        self.suggestions_frame.pack(pady=10, fill="x", padx=20)

        # Création des 3 boutons pour les suggestions de mots
        self.boutons_suggestions = []
        for i in range(3):
            btn = ctk.CTkButton(self.suggestions_frame, text="-", width=160, height=35, font=ctk.CTkFont(size=13), command=lambda idx=i: self.inserer_suggestion(idx))
            btn.pack(side="left", expand=True, padx=5, pady=10)
            self.boutons_suggestions.append(btn)

        # --- ZONE DES SMILEYS (Tout en bas) ---
        self.smileys_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.smileys_frame.pack(pady=(10, 5), fill="x", padx=20)

        # Ta liste de smileys préférés
        liste_smileys = ["😂", "😊", "👍", "😉", "😍", "🙏", "😎", "🎉", "😢", "🔥", "👍", "❤️"]
        
        # Boucle sécurisée (s=sml) pour que chaque bouton envoie son propre émoji
        for sml in liste_smileys:
            btn_smiley = ctk.CTkButton(
                self.smileys_frame, 
                text=sml, 
                width=35, 
                height=30, 
                font=ctk.CTkFont(size=16), 
                fg_color="#3a3a3a", 
                hover_color="#505050", 
                command=lambda s=sml: self.inserer_smiley(s)
            )
            btn_smiley.pack(side="left", expand=True, padx=2)

        # --- COMPACT INFO LABEL ---
        self.info_label = ctk.CTkLabel(self, text="Les suggestions s'adaptent en temps réel pendant la frappe.", text_color="gray", font=ctk.CTkFont(size=11, slant="italic"))
        self.info_label.pack(pady=(5, 10))

        self.mots_valides = []
        self.suggestions_actuelles = []

        # Premier calcul initial à vide
        self.mettre_a_jour_suggestions()

    def analyser_saisie(self, event=None):
        """ Analyse le texte en temps réel pour extraire le mot en cours et le contexte """
        contenu = self.textbox.get("1.0", "end-1c")
        mots = re.findall(r'\b\w+\b', contenu.lower())
        si_espace_final = contenu.endswith(" ") if contenu else False

        if not contenu.strip():
            self.mots_valides = []
            mot_en_cours = ""
        elif si_espace_final:
            self.mots_valides = mots
            mot_en_cours = ""
        else:
            self.mots_valides = mots[:-1] if mots else []
            mot_en_cours = mots[-1] if mots else ""

        # Récupération des données depuis tes algorithmes IA
        completions = [mot for mot, _ in trie.get_suggestions(mot_en_cours)[:3]]
        predictions_suite = [mot for mot, _ in ngram.predict(self.mots_valides)[:3]]

        if mot_en_cours:
            self.suggestions_actuelles = completions
            while len(self.suggestions_actuelles) < 3 and predictions_suite:
                p = predictions_suite.pop(0)
                if p not in self.suggestions_actuelles:
                    self.suggestions_actuelles.append(p)
        else:
            self.suggestions_actuelles = predictions_suite

        self.mettre_a_jour_suggestions()

    def mettre_a_jour_suggestions(self):
        """ Modifie visuellement le texte des boutons avec les nouvelles suggestions """
        for i in range(3):
            if i < len(self.suggestions_actuelles):
                self.boutons_suggestions[i].configure(text=self.suggestions_actuelles[i], state="normal")
            else:
                self.boutons_suggestions[i].configure(text="-", state="disabled")

    def inserer_suggestion(self, index):
        """ Insère le mot de l'IA cliqué directement dans la zone de texte """
        if index >= len(self.suggestions_actuelles):
            return

        mot_a_ajouter = self.suggestions_actuelles[index]
        contenu = self.textbox.get("1.0", "end-1c").rstrip()
        
        mots = re.findall(r'\b\w+\b', contenu.lower())
        if mots and not self.textbox.get("1.0", "end-1c").endswith(" "):
            mots.pop() 
        
        mots.append(mot_a_ajouter)
        
        nouveau_texte = " ".join(mots) + " "
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", nouveau_texte)
        
        self.textbox.mark_set("insert", "end")
        self.analyser_saisie()

    def inserer_smiley(self, smiley):
        """ Insère le smiley cliqué à la position actuelle du curseur """
        self.textbox.insert("insert", smiley + " ")
        self.textbox.focus()  # Redonne la priorité de frappe au clavier principal
        self.analyser_saisie()  # Met à jour les suggestions IA après le smiley

# --- Lancement du programme ---
if __name__ == "__main__":
    app = ApplicationPredictive()
    app.mainloop()