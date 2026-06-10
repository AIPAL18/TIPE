# Delta Compression: A practical guide to diff algorithms and delta file formats

From:

* [Delta Compression: A practical guide to diff algorithms and delta file formats](https://dev.to/dominikelmiger/delta-compression-a-practical-guide-to-diff-algorithms-and-delta-file-formats-23bi)

Traduit par (pour la forme):

* [ChatGPT](chatgpt.com)

---

## Correction chaîne-à-chaîne (*String-to-String Correction*) ou insertion/suppression (*Insert/Delete*)

La première génération d'algorithmes de différenciation (*diff algorithms*) résolvait le problème de la **correction chaîne-à-chaîne** (*string-to-string correction*) et est apparue dans les années 1960 et 1970.

Chacune des deux entrées est interprétée comme une chaîne de caractères composée de symboles appartenant à un alphabet donné. La sortie est une séquence d'opérations d'édition (*edit operations*) sur les caractères — le plus souvent des opérations d'insertion et de suppression — pouvant être appliquées à l'une des entrées afin de la transformer en l'autre.

Cette famille d'algorithmes est particulièrement adaptée à la génération de *diffs* lisibles par des humains lorsque les données d'entrée sont elles-mêmes lisibles par des humains, par exemple différentes versions d'un même texte ou d'un même code source résultant de modifications réelles effectuées au fil du temps.

Un autre avantage est que, en théorie et très souvent en pratique, il existe plusieurs séquences minimales d'opérations d'édition permettant d'obtenir le même résultat. Diverses heuristiques peuvent alors être utilisées afin de sélectionner la séquence qui ressemble le plus aux modifications réellement effectuées par un être humain.

L'algorithme de Robert A. Wagner et Michael J. Fischer (*Wagner-Fischer*) a posé les fondations de cette génération d'algorithmes de *diff*. L'algorithme de Eugene W. Myers (*Myers Algorithm*) constitue l'amélioration la plus récente et est devenu le standard de facto de cette génération. Il est aujourd'hui utilisé dans plusieurs outils de comparaison de fichiers, notamment l'utilitaire GNU diff.

Cette génération d'algorithmes cherche généralement soit :

* la **plus longue sous-séquence commune** (*Longest Common Subsequence – LCS*) ;
* la **distance d'édition minimale** (*minimal edit distance*), généralement la **distance de Levenshtein** ;

puis utilise ce résultat pour construire la séquence de modifications nécessaire afin de transformer une entrée en l'autre.

## Déplacement de blocs ou copie/insertion (*Block Move or Copy/Insert*)

### Déplacement pur de blocs (*Pure Block Move*)

La génération suivante d'algorithmes de *diff* repose sur ce qui semblait initialement n'être que de petites optimisations de la génération précédente.

Les opérations portant sur des caractères individuels ont été remplacées par des opérations portant sur des **blocs de caractères**.

Autrement dit, au lieu d'exprimer la différence sous la forme d'opérations appliquées à des caractères isolés, celle-ci est exprimée sous la forme d'opérations appliquées à des segments entiers de données.

Les opérations utilisées sont généralement :

* **copie** (*copy*) ;
* **insertion** (*insert*).

Les blocs de données présents dans les deux entrées sont enregistrés dans le delta comme étant copiés d'une entrée vers l'autre. Les blocs n'apparaissant que dans l'une des deux entrées sont enregistrés comme des insertions.

Cette approche a été proposée pour la première fois par Walter F. Tichy.

### Déplacement de blocs basé sur la compression (*Compression-Based Block Move*)

#### Comment Ably génère des deltas dans sa plateforme de messagerie *pub/sub* en utilisant l'approche par déplacement de blocs

À première vue, l'approche par déplacement de blocs semble n'être qu'une optimisation mineure. Pourtant, ses conséquences deviennent considérables dès lors que l'on tient compte de la possibilité qu'un ou plusieurs blocs de caractères se répètent dans l'une ou les deux entrées.

Le fait de considérer la génération d'un *diff* comme un problème de copie de blocs de données, tout en recherchant les blocs apparaissant plusieurs fois, ouvre la voie à l'utilisation d'algorithmes de compression pour produire des fichiers de *diff* et de *delta*.

Les algorithmes de compression font précisément cela : ils recherchent les plus grands blocs répétitifs possibles et remplacent chaque occurrence ultérieure par une référence à la première occurrence.

Les blocs qui n'apparaissent qu'une seule fois sont copiés directement dans la sortie.

Ainsi, d'une certaine manière, les algorithmes de compression peuvent être vus comme des algorithmes de déplacement de blocs.

Il apparaît alors clairement que si l'analyse de déplacement de blocs effectuée par un algorithme de compression est appliquée simultanément aux deux entrées d'un algorithme de *diff*, elle identifiera facilement les parties communes aux deux fichiers.

Elle permettra également de déterminer quels blocs sont spécifiques à chaque entrée, c'est-à-dire les portions réellement différentes.

À partir de ces informations, il devient relativement simple de construire une séquence d'opérations de copie et de suppression de blocs permettant de transformer une entrée en l'autre.

Le principal avantage de l'utilisation d'algorithmes de compression réside dans la réduction importante de la taille du delta.

Un bloc de données n'apparaîtra jamais plus d'une fois dans le delta :

* il pourra être référencé plusieurs fois ;
* mais son contenu réel ne sera stocké qu'une seule fois.

Cela constitue une différence majeure par rapport aux approches précédentes.

Il convient également de noter que cette réduction de taille s'obtient au prix d'une moindre lisibilité humaine du résultat produit.

Les implémentations xDelta, zDelta et l'algorithme de Jon Bentley / M. Douglas McIlroy sont largement utilisées et constituent les standards de facto de cette génération.

## Améliorations les plus récentes (*Latest Upgrades*)

Cette catégorie correspond à la génération la plus récente d'algorithmes de *diff*.

La plupart de ses représentants n'existent encore que sous forme d'articles de recherche et ne disposent pas, à ce jour, d'implémentations commerciales largement diffusées.

Ces algorithmes restent principalement fondés sur l'approche par déplacement de blocs, mais introduisent des optimisations substantielles dans leur mise en œuvre.

Ces améliorations permettent d'annoncer des gains de performance pouvant atteindre plusieurs dizaines de pourcents, voire des accélérations par facteurs supérieurs à dix (*double-digit factor improvements*), par rapport à la génération précédente.

Ces optimisations visent principalement à identifier efficacement les blocs correspondants entre les deux entrées.

Pour cela, diverses techniques sont employées :

* hachage incrémental (*incremental hashing*) ;
* méthodes inspirées de la compression ;
* structures de données spécialisées telles que les **arbres de suffixes** (*suffix trees*).

Les algorithmes **edelta**, **ddelta** et **bsdiff** peuvent être rattachés à cette génération.

## Algorithmes de génération de deltas actuellement utilisés

Cette section fournit un bref aperçu des outils et bibliothèques spécialisés dans la génération efficace de fichiers **delta** et **patch**, disponibles au moment de la rédaction de l'article.

De nombreuses implémentations d'algorithmes de *diff* généralistes existent dans différents langages de programmation, mais ne sont pas mentionnées ici.

L'exhaustivité n'est pas revendiquée, même si la probabilité qu'un outil ou une bibliothèque populaire ait été omis reste relativement faible.

Après tout, par définition, ce qui est populaire est censé être facile à rencontrer.

### Notes terminologiques importantes

Dans ce contexte :

* **Diff** = description des différences entre deux versions.
* **Delta** = ensemble minimal d'informations permettant de reconstruire une version à partir d'une autre.
* **Patch** = fichier contenant un delta destiné à être appliqué.
* **Edit distance** = coût minimal de transformation entre deux chaînes.
* **Block move** est généralement mieux traduit par **déplacement de blocs**, mais dans la littérature informatique française on rencontre aussi **copie de blocs avec références**.
* **String-to-string correction** est parfois traduit par **problème de correction entre chaînes**, **transformation de chaînes** ou **édition de chaînes**. Le terme anglais reste cependant très courant dans les publications scientifiques.
