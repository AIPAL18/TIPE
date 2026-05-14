# Cahier de Bord

## 03/02/2026

### TL;DR

Je me suis intéressé au principe de Coupling/Cohesion (par intérêt personnel), notamment du côté de la modularité (AppShell, injection de dépendances, IoC, ...). Cela m'a amené à considérer plusieurs problème courent en architecture logiciel:

* L'abstraction entre machine et logiciel \
  => coûts supplémentaires car l'OS doit faire l'intermédiaire.
  => Les ordinateurs sont des machines à calculer, mais aujourd'hui, son usage s'est divisé en deux grandes catégories :
  * Manipulation de données avec une une partie lecture/écriture de la mémoire.
  * Affichage de ces données (interfaces UI/UX)
* Les langages d'assembleurs semblent limités
  * Les opérations changent d'un système à un autre (e.g. x86 et ARM) et elles ne sont pas toujours pertinentes vis-à-vis de l'usage qu'on en fait
  * Les system calls sont peu efficaces, le système manque un peu de flexibilité

Je me suis donc intéressé aux modèles de calculs et aux paradigmes:

---
ChatGPT

### Classification synthétique des paradigmes

| Paradigme            | Famille                | Principe central         | Modèle de calcul        | Forces                     | Limites                  |
| -------------------- | ---------------------- | ------------------------ | ----------------------- | -------------------------- | ------------------------ |
| Procédural           | Impératif              | Séquence d’instructions  | Machine de von Neumann  | Simplicité, performance    | Scalabilité conceptuelle |
| Orienté objet        | Impératif              | Objets = état + méthodes | Objets + messages       | Modélisation métier        | Couplage, complexité     |
| Fonctionnel          | Déclaratif             | Fonctions pures          | λ-calcul                | Raisonnement, parallélisme | Courbe d’apprentissage   |
| Logique              | Déclaratif             | Faits + règles           | Logique du 1er ordre    | Expressivité, IA           | Performance, contrôle    |
| Déclaratif (général) | Déclaratif             | Décrire le résultat      | Dépend du moteur        | Abstraction maximale       | Moins de contrôle        |
| Événementiel         | Impératif              | Réaction aux événements  | Boucle d’événements     | UI, systèmes réactifs      | Flux non linéaire        |
| Concurrent           | Impératif / Déclaratif | Tâches simultanées       | Threads / acteurs / CSP | Scalabilité                | Synchronisation          |
| Orienté composants   | Architecture           | Composants indépendants  | Assemblage              | Réutilisabilité            | Overhead                 |
| Orienté aspects      | Transversal            | Séparation des concerns  | Tissage                 | Modularité                 | Lisibilité               |
| Data-oriented        | Impératif              | Données avant objets     | Accès mémoire           | Performance brute          | Expressivité métier      |

### Mapping paradigme → cas d’usage

| Cas d’usage         | Paradigmes dominants             | Pourquoi                   |
| ------------------- | -------------------------------- | -------------------------- |
| UI / Frontend       | Événementiel, déclaratif         | Interaction utilisateur    |
| Backend web         | Objet, événementiel, fonctionnel | Lisibilité + scalabilité   |
| Systèmes temps réel | Concurrent, data-oriented        | Déterminisme, perf         |
| IA symbolique       | Logique, déclaratif              | Raisonnement automatique   |
| Calcul scientifique | Fonctionnel, parallèle           | Immuabilité, parallélisme  |
| Game engine         | Data-oriented, impératif         | Cache, performance         |
| Microservices       | Composants, services, acteurs    | Isolation, résilience      |
| Systèmes distribués | Acteurs, CSP                     | Tolérance aux pannes       |
| DevOps / infra      | Déclaratif                       | Reproductibilité (ex: IaC) |

### 3. Zoom technique (choix ciblés)

#### A. Programmation fonctionnelle (angle rigoureux)

Fondement théorique

* λ-calcul
* Fonctions totales, équational reasoning

Concepts clés

* Immuabilité
* Fonctions d’ordre supérieur
* Monades (gestion des effets)
* Lazy vs eager evaluation

Avantage clé

* *La correction devient une propriété mathématique.*

#### B. Programmation concurrente par acteurs

Modèle

* Acteurs isolés
* Communication par messages
* Pas d’état partagé

Langages

* Erlang, Elixir, Scala (Akka)

Avantage clé

* *Scalabilité et tolérance aux pannes par construction.*

#### C. Data-oriented programming (très bas niveau)

Principe

* Structurer les données pour le CPU, pas pour l’humain
* SoA > AoS

Utilisation

* Game engines
* Simulations physiques
* HPC

Avantage clé

* *Performance mémoire > élégance syntaxique.*

---

Ce qui m'amène à repenser la machine en tant que telle.

Créer plusieurs parties d'une même machine (*Cf. supra*) en utilisant divers méthodes/système, et ce en les combinant pour faire valoir leurs points fort et diminuer leurs points faible.

1. Calcul ([UAL](https://fr.wikipedia.org/wiki/Unit%C3%A9_arithm%C3%A9tique_et_logique))
2. Affichage
3. Mémoire
4. Modularité

### Bibliographie

* **Neurocomix - Voyage fantastique dans le cerveau** (2014) - Dunod \
  Matteo Farinella, Han Roš (ISBN: *9782100708543*)
* **C3RV34U** (2014) - Edition de la Martinière \
  Stanislas Dehaene (ISBN: *9782732462578*)
* **Applied Mathematical Science (126) - Weakly Connected Neural Networks** (1997) - Springer \
  Frank C. Hoppensteadt, Eugene M. Izhikevich (ISBN: *0387949488*)

## 10/02/2026

Objectif: get rid of OSs

The neuromorphic hardware

* [Model of computation](https://en.wikipedia.org/wiki/Model_of_computation)

## Vacances (14/02/2026 - 01/03/2026)

Méthodologie:

1. Choisir des solutions techniques pour chaque fonction de la machine et créer une architecture avec.
2. Confronter ce modèle à la littérature scientifique et aux concepts déjà existants
3. Choisir un axe de TIPE (voire une problématique)

Tout d'abord: analyse fonctionnelle d'un ordinateur.

## 03/03/2026

Changement de sujet: La compilation de modules ()
