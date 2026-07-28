# TIPE

Problématique : Comment garantir la rétrocompatibilité d'une bibliothèque partagée en optimisant l'espace sans sacrifier les performances.

Objectifs:

* étude des qualités/propriétés de fonctions de compression sans perte.
* étude d'algorithmes de recherche sur des données compressées sans perte.

Thèmes : Compressed pattern matching, Compression, Data differencing, Search algorithm, Lossless Compression

<details>
<summary>

## (Cadre)<sup style="color: grey; font-weight: normal !important;" title="Uniquement nécessaire pour les approximation de temps">&#x1F6C8;</sup>

</summary>

<s>On suppose travailler avec une bibliothèque dont on a modifié l'ABI, \
    - d'horloge à fréquence fixée à 1 GHz \
    - d'une RAM de 8 Gio/GiB \
    - de disque de 128 Gio/GiB \
exécutant un OS UNIX-like</s>

</details>

## Objectif(s)

1. Recherche des qualités d'un algorithme de compression (LossLess, décompressible localement, etc.)
2. Création d'un format pour la compression (pour des caractéristiques données)
3. Recherche dans des donnée compressées (influencé par .2)

## Ressources

* [@recherches](./research/recherche.md)

## TODO

* [ ] Expérience
