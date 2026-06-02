# TIPE

Problématique : Comment garantir la rétrocompatibilité d'une bibliothèque partagée en optimisant l'espace sans sacrifier les performances.

Objectif: étude des qualités/propriétés de fonctions de compression sans perte.

Sous-objectif: étude d'algorithme de recherche sur des données compressées sans perte.

Thèmes : Compressed pattern matching, Compression, Data differencing, Search algorithm, Lossless Compression, <s>signature/identification</s>

Mots clés : <s>Problématique de modularité, library, optimisation de l'espace en garantissant des performances similaire.</s> Algorithme de compression sans perte, recherche sur des données compressées sans perte, bibliothèque partagée, elf, linux

## (Cadre)<sup style="color: grey; font-weight: normal !important;" title="Uniquement nécessaire pour les approximation de temps">&#x1F6C8;</sup>

<s>On suppose travailler avec une bibliothèque dont on a modifié l'ABI, \
    - d'horloge à fréquence fixée à 1 GHz \
    - d'une RAM de 8 Gio/GiB \
    - de disque de 128 Gio/GiB \
exécutant un OS UNIX-like</s>

## Objectif(s)

### Comparaison d'algorithme de compression (propriétés/qualités)

* Myers Algorithm
* Bentley-McIlroy
* Xdelta
* BSDiff

### Comparaison de format pour la compression (pour des caractéristiques donnée)

* VCDiff[<sup>(wiki)</sup>](https://en.wikipedia.org/wiki/VCDIFF)
* Unix .patch
* ...

### Recherche dans des donnée compressées[<sup>(wiki)</sup>](https://en.wikipedia.org/wiki/Compressed_pattern_matching)

* <s>signature</s>

## Bibliographie / SOTA (non exhaustive)

### Myers

MYERS, EUGENE W. “An O(ND) Difference Algorithm and Its Variations.” Algorithmica, vol. 1, Nov. 1986, pp. 251–266, https://doi.org/10.1007/BF01840446.

### Bentley–McIlroy

Bentley, J.L. and McIlroy, M.D. (1993), Engineering a sort function. Softw: Pract. Exper., 23: 1249-1265. https://doi.org/10.1002/spe.4380231105

#### Implémentations

* [Bentley–McIlroy algorithm (GitHub)](https://github.com/aprescott/bentley_mcilroy)
* [open-vcdiff - Google (GitHub)](https://github.com/google/open-vcdiff)

### Xdelta

https://doi.org/10.17487/RFC3284

https://github.com/jmacd/xdelta
