# Content

## Page de garde (1)

## Contextualisation (2)

* Bibliothèque partagée: fichier qui contient du code redondant et très utilisé
* Liaison dynamique -> Dépendance à la compilation
* Mise à jour d'un bib -> impacte programme qui est dépendant
* version 32 bits vs 64 bits
* Résolution: avoir plusieurs version d'un même fichier

## Problématique (3)

## Compression de données (4)

* Compression des fichiers en un seul par juxtaposition
* Propriétés de la compression

## Compression par delta (5)

* force: beaucoup de répétition
* Garder un objet, et noter les opérations pour aller vers l'autre objet
* Insertion/suppression
* Déplacement de blocs (copie/insertion) ; plus moderne

## Segments ELF (6)

* La résolution est fait à l'exécution par liaison paresseuse.
* appel d'une fonction remplacé par un appel à une procedure de résolution
* appel du lieur dynamique qui résout la dépendance :
  * cherche dans les dépendances dynamiques la fonction appelée
* écriture dans la Global Offset Table

## Recherche (7)

* En résumé: plusieurs versions coexistent dans le même fichier
* On peut exclure tous les symboles qui ne se rapportent pas à la version de laquelle le programme dépend
* Recherche par plage

## Conclusion (8)

* Force : l'impacte à l'exécution devrait être minime:
  * La compression est une union ensembliste de fichiers
* Faiblesses : La différence en mémoire n'est pas significative
  * Les programmes moderne 
