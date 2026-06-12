# Algorithmes de différenciation par delta

[*@llm*](./_diffs1.md)

[source 1](https://hackernoon.com/delta-compression-diff-algorithms-and-delta-file-formats-practical-guide-7v1p3uhz)

[source 1 bis](https://dev.to/dominikelmiger/delta-compression-a-practical-guide-to-diff-algorithms-and-delta-file-formats-23bi)

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
