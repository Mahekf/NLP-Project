## Ce program fonctionne bien 
import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class PredictiveSystem:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, count=1):
        if not word: 
            return
        node = self.root
        for char in word.lower():
            if char not in node.children : 
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += count

    def train_on_corpus(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        for word in words:
            self.insert(word)
        print(f"--- {len(words)} mots analysés ---")

    def get_suggestions(self, prefix):
        node = self.root

        # 1. Naviguer jusqu'au bout du préfixe
        for char in prefix.lower():
            if char not in node.children: 
                return []
            node = node.children[char]

        # 2. Collecter toutes les terminaisons possibles
        results = []
        self._dfs(node, prefix.lower(), results)

        # 3. Trier par fréquence décroissante (le plus fréquent en premier)
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    # Ici, on utilise l'algorithme de parcours en profondeur 
    def _dfs(self, node, current_prefix, results):
        if node.is_end_of_word:
            results.append((current_prefix, node.frequency))
        for char, next_node in node.children.items():
            self._dfs(next_node, current_prefix + char, results)


## MAIN - TEST ##
def main():
    system = PredictiveSystem()

    system.train_on_corpus(" Bonjour à tous. Bonjour tout le monde. Le chat est noir. Le chat dort sur le tapis. Demain il fera beau. Bonjour encore, le soleil brille")

    while True:
        saisie = input("\nEntrez un préfixe : ").strip().lower()
        if saisie == 'exit': break
        
        suggestions = system.get_suggestions(saisie)
        
        if suggestions:
            for i, (mot, freq) in enumerate(suggestions[:5]):
                print(f"  {i+1}. {mot} (score: {freq})")
            
            choix = input("n° ou mot complet : ").strip().lower()
            if choix.isdigit():
                idx = int(choix) - 1
                if 0 <= idx < len(suggestions):
                    system.insert(suggestions[idx][0])
            elif choix != "":
                system.insert(choix)
        else:
            print("Inconnu. J'ajoute...")
            system.insert(saisie)

if __name__ == "__main__":
    main()