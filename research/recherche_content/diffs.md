# Algorithmes de différenciation par delta

[llm](./_diffs1.md)

## Insertion/suppression

Cette génération d'algorithmes cherche généralement soit :

* la **plus longue sous-séquence commune** (*Longest Common Subsequence – LCS*) ;
* la **distance d'édition minimale** (*minimal edit distance*), généralement la **distance de Levenshtein** ;

puis utilise ce résultat pour construire la séquence de modifications nécessaire afin de transformer une entrée en l'autre

Ainsi, la distance d'édition est optimale en le nombre d'opération nécessaire à la modification

## Déplacement de blocs basé sur la compression

Prendre en compte qu'une décompression locale nécessite un certain nombre d'opération supplémentaire pour se déplacer vers un bloc déjà répété.

## Stocker 2 fichiers en un (puis *n* en un)

* [VCDiff](https://datatracker.ietf.org/doc/html/rfc3284#section-3)
