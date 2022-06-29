# bms_nlp
Fonctions développées afin d'extraire les éléments qui compose le score bacterial meningitis score et de le calculer.
- algo_bms: regroupe la fonction permettant de réaliser l'ensemble de la pipe d'extraction et de calcule.
- bms_nlp_pipe: déclare la pipe basé sur eds_nlp 
    en y ajoutant la pipe "isin_spanparagraph" développée spécifiquement pour le projet afin 
    d'identifier les éléments ce rapportant à une ponction lombaire
- bms_agragate: sélectionne les entités à partir de règle logique 
    afin de ne garder qu'une entité par label et par document
- bms_calc_score: se charge de normaliser les entités extraites notamment numériques 
    afin de calculer le score BMS selon 3 modalités. 
    Il peut aussi intégrer dans un second temps des données structurées 
    et recalculer le score en gardant les 2 résultats afin de pouvoir les comparer.
- main regroupe l'ensemble des modules nécessaire à l'exécution de l'algorithme
- isin_spanparagraph regroupe l'ensemble de la pipe eds_nlp permettant l'ajout d'attribut aux entités compris entre une entité d'un label d'intérêt
    dans notre cas: ponction lombaire (''pl''), et un token identifié comme un changement de paragraphe ('\n *\n').
- dictionnaire: regroupe l'ensemble des dictionnaires utilisés pour ce projet avec leurs différentes versions.
