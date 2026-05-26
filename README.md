# PROJET TAL : Saisie Prédictive

* **Niveau :** L3 Informatique et Linguistique (TAL)
* **Faculté :** Université Paris Cité
* **Noms et Prénoms :** Abo Izhar Mahek Fatma & Chaer Rime 

Ce projet implémente un système complet d'aide à la saisie combinant un arbre de préfixes (Trie) pour la complétion, un modèle statistique N-gramme avec Backoff pour la prédiction contextuelle, et la distance de Levenshtein pour la correction d'erreurs. Il intègre un module d'accessibilité déporté sur iPad (clavier virtuel + trackpad UDP).

---

## PRÉREQUIS ET INSTALLATION

Avant de lancer l'application, assurez-vous d'installer les bibliothèques Python requises à l'aide de la commande suivante :

* pip install customtkinter pandas openpyxl scikit-learn

Note : Le fichier de données '88milSMS.ods' doit impérativement se trouver dans le même répertoire que les scripts pour l'extraction du corpus.

---

## MODES D'EXÉCUTION (Aide en ligne intégrée)

Le script principal gère les arguments en ligne de commande. Pour afficher l'aide depuis votre terminal, exécutez :

* python3 Interface2.py --help

Trois modes opératoires distincts sont disponibles :

### A) Mode Interface Graphique (GUI)
Lance l'IHM customtkinter de saisie prédictive sur l'ordinateur.
* Commande : python3 Interface2.py --mode gui
* *(ou simplement : python3 Interface2.py)*

### B) Mode Évaluation (Calcul de l'Accuracy)
Exécute l'évaluation automatique sur les 10% du corpus de test isolés et calcule l'Accuracy Top-1 et Top-3 sur 77 289 mots.
* Commande : python3 Interface2.py --mode test

### C) Mode Accessibilité Déportée (SERVER / CLIENT)
Permet de lier un iPad et un MacBook sur le même réseau Wi-Fi local.

1. Sur l'ordinateur (MacBook), lancez le serveur d'écoute :
   * Commande : python3 server_mac.py
2. Sur la tablette (iPad, via Pythonista), lancez le client tactile :
   * Commande : python3 client_client.py
3. Entrez l'IP du Mac sur l'iPad pour activer le clavier et le trackpad. *(lancez l'expérience !)*
