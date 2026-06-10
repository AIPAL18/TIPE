# GOT et PLT

**User:** Anonymous  
**Created:** 4/29/2026 19:42:12  
**Updated:** 4/29/2026 21:18:40  
**Exported:** 4/29/2026 21:22:38  
**Link:** [https://chatgpt.com/g/g-p-69e628c914308191b48db766faa5a62b-tipe/c/69f242c7-d2dc-83eb-9d38-fa2409a8f4c6](https://chatgpt.com/g/g-p-69e628c914308191b48db766faa5a62b-tipe/c/69f242c7-d2dc-83eb-9d38-fa2409a8f4c6)  

### *Response:*

4/29/2026, 7:42:12 PM

Les **GOT** (*Global Offset Table*) et **PLT** (*Procedure Linkage Table*) sont au cœur du mécanisme de **liaison dynamique** dans les exécutables ELF (typiquement sous Linux). Leur rôle principal est de permettre à un programme compilé d’appeler des fonctions et d’accéder à des variables **dont l’adresse n’est connue qu’au moment de l’exécution**.

Je vais structurer ça proprement, comme on le ferait en architecture logicielle.

---

## 1. Problème à résoudre

Quand tu compiles avec une bibliothèque dynamique (`.so`) :

- les adresses des fonctions externes **ne sont pas connues à la compilation**
- elles ne sont même pas forcément connues au chargement (ASLR, relocation, etc.)

Donc :
👉 il faut un mécanisme **indirect** pour accéder aux symboles.

---

## 2. La GOT (Global Offset Table)

### Rôle

La GOT est une table en mémoire contenant des **adresses réelles** :

- fonctions externes
- variables globales externes

👉 C’est une table de **résolution d’adresses**.

### Principe

Au lieu de faire :

```asm
call printf
```

On fait :

```asm
call [adresse_dans_GOT]
```

Donc :

- la GOT contient des pointeurs
- ces pointeurs sont remplis par le linker dynamique (`ld-linux.so`)

### Types d’entrées

On distingue généralement :

- `.got` → variables globales
- `.got.plt` → fonctions (utilisées avec la PLT)

---

## 3. La PLT (Procedure Linkage Table)

### Rôle
La PLT sert à appeler des fonctions externes **de manière paresseuse (lazy binding)**.

👉 Elle agit comme un **stub (trampoline)**.

### Idée clé

La première fois que tu appelles une fonction externe :

1. tu passes par la PLT
2. la PLT appelle le linker dynamique
3. le linker résout l’adresse réelle
4. la GOT est mise à jour
5. les appels suivants vont directement à la bonne adresse

---

## 4. Interaction PLT ↔ GOT (le cœur du mécanisme)

### Appel d’une fonction externe

Prenons `printf`.

#### Premier appel

1. Le code appelle `printf@plt`
2. L’entrée PLT fait :
   - un saut indirect via la GOT
   - MAIS la GOT pointe encore vers la PLT elle-même (fallback)
3. On arrive dans un resolver (`ld-linux`)
4. Le resolver :
   - trouve l’adresse réelle de `printf`
   - écrit cette adresse dans la GOT
5. Retour à l’appelant

#### Appels suivants

- `printf@plt` → GOT → adresse réelle directe
- donc plus de coût de résolution

---

## 5. Structure typique d’une entrée PLT

Une entrée PLT ressemble à ça (simplifié) :

```asm
jmp *GOT[printf]
push index
jmp PLT[0]
```

- `jmp *GOT[...]` → appel indirect
- `push index` → identifiant du symbole
- `PLT[0]` → point d’entrée du resolver

---

## 6. Lazy binding vs eager binding

### Lazy binding (par défaut)

- résolution **au premier appel**
- plus rapide au démarrage
- mais overhead au premier call

### Eager binding (`LD_BIND_NOW=1`)

- toutes les adresses sont résolues au lancement
- startup plus lent
- appels ensuite plus rapides

---

## 7. Relocations associées

Deux types principaux :

- `R_X86_64_JUMP_SLOT` → pour la PLT (fonctions)
- `R_X86_64_GLOB_DAT` → pour la GOT (variables)

Ces entrées disent au linker dynamique :
👉 "remplis cette case de la GOT avec l’adresse réelle"

---

## 8. Sécurité (très important)

### Attaques classiques

#### GOT overwrite

- si un attaquant modifie une entrée GOT
- il redirige un appel de fonction

👉 utilisé dans les exploits type **ret2plt**

### Contre-mesures

- **RELRO (Read-Only Relocations)** :
  - partiel : GOT encore modifiable
  - complet : GOT en lecture seule après init

- **ASLR**
- **PIE**

---

## 9. Avantages du mécanisme

- partage mémoire entre processus
- réduction taille des binaires
- mise à jour des libs sans recompiler
- chargement paresseux (performance)

---

## 10. Résumé mental (très utile)

Tu peux voir ça comme :

- **PLT = point d’entrée contrôlé (stub)**
- **GOT = table de pointeurs réels**

👉 Pipeline :

```
code → PLT → GOT → adresse réelle
```

---

## 11. Vision bas niveau (important pour ton TIPE)

- La PLT est du **code exécutable**
- La GOT est des **données modifiables**
- Le linker dynamique (`ld.so`) fait :
  - parsing ELF
  - résolution symbolique
  - patch de la GOT

---

## 12. Si tu veux aller encore plus loin

On peut creuser :

- désassemblage réel avec `objdump -d`
- inspection GOT/PLT avec `readelf -r`
- comportement avec/ sans `-fPIC`
- impact sur les performances
- exploitation (ret2plt, GOT hijacking)

---

Si tu veux, je peux te faire :

- un schéma mémoire ultra propre (niveau CPGE)
- ou analyser un binaire réel ligne par ligne (très formateur pour ton TIPE)

### *Prompt:*

4/29/2026, 7:48:52 PM

Est-ce que l'une ou l'autre est contenu dans l'executable, ou bien est-elle construite par le loader ou linker ?

### *Response:*

4/29/2026, 7:48:55 PM

Bonne question - c’est exactement le point qui fait basculer d’une compréhension “conceptuelle” à une compréhension **réellement système**.

### Réponse courte

- **PLT** → **présente dans l’exécutable** (générée à la compilation/link)
- **GOT** → **présente dans l’exécutable**, mais **remplie/modifiée à l’exécution**

👉 Donc :

- aucune des deux n’est “créée” par le loader
- mais **la GOT est dynamiquement patchée par le linker dynamique**

---

### 1. Ce qui est dans le binaire ELF (au moment du link)

Quand tu compiles avec une librairie dynamique (`-shared`, ou linkage standard avec glibc) :

#### Le linker statique (`ld`) génère :

#### ✔ La PLT

- section `.plt`
- contient du **code assembleur**
- une entrée par fonction externe

#### ✔ La GOT

- section `.got` et `.got.plt`
- contient des **pointeurs (initialement incomplets ou factices)**

👉 À ce stade :

- les adresses réelles **ne sont pas connues**
- mais toute l’infrastructure est en place

---

### 2. Ce que fait le loader (`ld-linux.so`) au lancement

Le loader ne crée pas la GOT/PLT - il va :

#### ✔ Mapper le binaire en mémoire

- sections `.plt`, `.got`, `.got.plt` incluses
- avec ASLR → adresses changent

#### ✔ Appliquer les relocations

Il lit :

- `.rela.plt`
- `.rela.dyn`

Et pour chaque entrée :

- soit il remplit directement la GOT (**eager binding**)
- soit il prépare le lazy binding

---

### 3. État initial de la GOT

C’est là que c’est subtil.

#### Pour les fonctions (GOT liée à la PLT) :

Au démarrage :

```text
GOT[printf] → adresse dans la PLT (pas la vraie fonction)
```

👉 Donc :

- la GOT contient **une adresse valide**
- mais ce n’est **pas encore la vraie**

---

### 4. Ce qui se passe à l’exécution

#### Premier appel

1. appel → `printf@plt`
2. PLT → lit GOT
3. GOT → pointe vers PLT fallback
4. appel du resolver (`ld.so`)
5. résolution de `printf`
6. écriture dans la GOT :

```text
GOT[printf] → vraie adresse de printf dans libc
```

---

#### Appels suivants

```text
PLT → GOT → libc مباشرة
```

👉 plus de passage par le resolver

---

### 5. Cas particulier : variables globales

Pour les variables :

- pas de PLT
- accès direct via la GOT

Et souvent :

- résolues **immédiatement au chargement** (pas lazy)

---

### 6. Synthèse claire

| Élément | Présent dans l’exécutable | Modifié à l’exécution |
|--------|--------------------------|------------------------|
| PLT    | ✔ oui (code)             | ❌ non                 |
| GOT    | ✔ oui (table)            | ✔ oui (remplie/patchée)|

---

### 7. Vision architecture (important)

Tu peux voir ça comme une séparation des responsabilités :

- **linker (ld)** :
  - construit les tables (PLT + GOT)
  - insère les stubs

- **loader (ld.so)** :
  - résout les symboles
  - écrit dans la GOT

👉 donc :
**structure statique, contenu dynamique**

---

### 8. Détail avancé (utile pour ton TIPE)

Même si la GOT est “dans le binaire” :

- elle est placée dans une section **writable**
- puis éventuellement protégée avec **RELRO**

Donc :

- avant init → modifiable
- après init → potentiellement read-only

---

### 9. Piège classique

On pourrait croire :

> “La GOT est construite dynamiquement”

❌ Faux

👉 Elle est :

- **allouée et positionnée dans l’ELF**
- mais **remplie dynamiquement**

---

Si tu veux aller plus loin, je peux te montrer :

- un `readelf -S` + `-r` réel avec GOT/PLT visibles
- ou un désassemblage PLT ligne par ligne (très instructif pour comprendre le trampoline)

### *Response:*

4/29/2026, 9:05:12 PM

Une **relocation** est une opération qui consiste à **corriger une adresse dans le code ou les données** une fois que l’emplacement réel en mémoire est connu.

C’est un mécanisme central dès que tu perds l’hypothèse “tout est à adresse fixe”, ce qui est précisément le cas avec :

- les bibliothèques dynamiques
- le code position-independent (PIC)
- l’ASLR

---

## 1. Intuition simple

À la compilation, tu peux écrire :

```c
printf("hello");
```

Mais :

- `printf` est dans une autre librairie
- son adresse réelle est inconnue

👉 Donc le compilateur génère :
> “je mettrai l’adresse ici plus tard”

Une **relocation**, c’est exactement :
> “voici où il faut écrire l’adresse quand tu la connaîtras”

---

## 2. Définition plus formelle

Une relocation est une **entrée de métadonnées dans l’ELF** qui décrit :

- **où** écrire (offset dans le binaire)
- **quoi** écrire (adresse d’un symbole)
- **comment** calculer la valeur

---

## 3. Structure d’une relocation (conceptuellement)

Une entrée contient :

- une **adresse cible** (où patcher)
- un **symbole** (ex : `printf`)
- un **type de relocation**
- parfois un **addend** (constante)

---

## 4. Exemple concret

Imaginons :

```asm
call printf
```

En réalité, dans un binaire dynamique, ça devient :

- un appel indirect via PLT
- et une relocation associée

Exemple typique (x86_64) :

- type : `R_X86_64_JUMP_SLOT`
- symbole : `printf`
- cible : entrée GOT

👉 Le linker dynamique va faire :

```text
GOT[printf] = adresse réelle de printf
```

---

## 5. Qui applique les relocations ?

### À la compilation (linker statique `ld`)

- crée les entrées de relocation
- ne les résout pas (si dynamique)

### À l’exécution (loader `ld-linux.so`)

- lit les tables :
  - `.rela.dyn`
  - `.rela.plt`
- applique les relocations

---

## 6. Types de relocations (important)

### 1. Relocations de données

Ex :

- `R_X86_64_GLOB_DAT`

👉 pour :

- variables globales
- pointeurs dans la GOT

---

### 2. Relocations de fonctions (PLT)

Ex :

- `R_X86_64_JUMP_SLOT`

👉 utilisées pour :

- lazy binding
- appels via PLT

---

### 3. Relocations relatives

Ex :

- `R_X86_64_RELATIVE`

👉 très fréquentes avec PIC

Forme :

```text
valeur = base_du_binaire + offset
```

👉 rapide car pas besoin de résolution de symbole

---

## 7. Lien direct avec GOT/PLT

Relocations = mécanisme  
GOT/PLT = structures utilisées

#### Typiquement :

- relocation → “remplir cette case”
- GOT → “la case à remplir”
- PLT → “utilise cette case”

---

## 8. Deux moments possibles

### Eager binding

- toutes les relocations sont appliquées au lancement
- plus lent au démarrage

### Lazy binding

- certaines relocations (PLT) sont différées
- résolues au premier appel

---

## 9. Exemple mental complet

```text
Compilation :
→ "printf" inconnu
→ création relocation

Exécution :
→ loader lit relocation
→ trouve printf dans libc
→ écrit adresse dans GOT
```

---

## 10. Vision bas niveau

Une relocation, c’est littéralement :

> une instruction pour modifier un octet/une adresse dans la mémoire du programme

👉 sans relocation :

- impossible de faire du code dynamique
- impossible de partager des librairies
- impossible d’avoir ASLR

---

## 11. Analogie utile

Imagine :

- ton programme = un texte avec des trous
- relocations = des post-it :
  > “mettre l’adresse de printf ici”

- loader = quelqu’un qui remplit les trous au dernier moment

---

## 12. À retenir pour ton TIPE

- une relocation n’est **pas du code**
- c’est une **donnée décrivant une correction à appliquer**
- elle est essentielle pour :
  - GOT
  - PLT
  - PIC
  - ASLR

---

Si tu veux, je peux te faire :

- un vrai dump `readelf -r` et te décoder chaque champ
- ou un exemple mémoire avant/après relocation (très parlant pour comprendre)

### *Response:*

4/29/2026, 9:11:07 PM

Le **PIC (Position-Independent Code)** est une technique de génération de code machine qui permet d’exécuter un binaire **à n’importe quelle adresse mémoire sans modification préalable**.

C’est un pilier de :

- la liaison dynamique (GOT/PLT)
- les bibliothèques partagées (`.so`)
- l’ASLR (sécurité)

---

## 1. Problème de départ

Code “classique” (non-PIC) :

```asm
mov rax, [0x400123]
```

👉 adresse **codée en dur**

Problème :

- si le programme est chargé ailleurs → tout casse
- il faudrait **relocaliser tout le code**
- coûteux + empêche le partage mémoire

---

## 2. Idée du PIC

👉 Ne jamais utiliser d’adresses absolues.

À la place :

- utiliser des **adresses relatives**
- ou passer par des **indirections (GOT)**

---

## 3. Accès aux données en PIC

### Principe

On utilise une adresse relative au pointeur d’instruction (RIP sur x86_64) :

```asm
mov rax, [rip + offset]
```

👉 “va lire à une distance fixe par rapport à moi”

Donc :

- peu importe où le code est chargé
- ça fonctionne toujours

---

## 4. Accès aux symboles externes

C’est là que la GOT intervient.

Au lieu de :

```asm
call printf
```

On fait :

```asm
call [rip + offset_vers_GOT]
```

👉 puis :

- GOT contient l’adresse réelle
- remplie via relocations

---

## 5. PIC et bibliothèques partagées

Sans PIC :

- chaque processus doit avoir **sa propre copie du code**
- car les adresses doivent être patchées

Avec PIC :

- le code est **identique pour tous**
- donc **partagé en mémoire (read-only)**

👉 énorme gain :

- RAM
- performances (cache)

---

## 6. PIC vs PIE

### PIC

- utilisé pour les bibliothèques (`.so`)
- compilé avec `-fPIC`

### PIE (Position Independent Executable)

- même principe mais pour un exécutable
- permet ASLR sur le main binary
- compilé avec `-fPIE` + `-pie`

👉 aujourd’hui :

- presque tous les exécutables Linux modernes sont PIE

---

## 7. Rôle des relocations en PIC

Même avec PIC, certaines valeurs doivent être ajustées :

#### Exemple :

```text
adresse = base_du_module + offset
```

👉 relocation de type :

- `R_X86_64_RELATIVE`

Avantage :

- très rapide (pas de lookup symbole)

---

## 8. Coût du PIC

Il y a un compromis.

### Inconvénients

- plus d’indirections (via GOT)
- instructions un peu plus complexes
- légère perte de performance

### Avantages

- partage mémoire
- sécurité (ASLR)
- flexibilité (chargement dynamique)

👉 en pratique :
le gain global est largement positif

---

## 9. Lien avec GOT/PLT

Sans PIC :

- appels directs possibles

Avec PIC :

- tout passe par :
  - GOT (données)
  - PLT (fonctions)

👉 PIC rend GOT/PLT indispensables

---

## 10. Exemple concret (chaîne complète)

#### Code source

```c
printf("hello");
```

#### Compilation PIC

- appel → PLT
- adresse → GOT
- résolution → relocation

#### Exécution

```text
code PIC → PLT → GOT → libc
```

---

## 11. Détail intéressant (x86 vs x86_64)

### x86 (32 bits)

- pas de RIP-relative addressing
- nécessite un registre dédié (souvent `ebx`)
- plus coûteux

### x86_64

- support natif RIP-relative
- PIC beaucoup plus efficace

---

## 12. Résumé mental

PIC =

> “du code qui ne dépend jamais de son adresse absolue”

Implémenté via :

- adressage relatif (`rip`)
- GOT (indirection)
- relocations (ajustement final)

---

## 13. Vision système (important pour toi)

PIC permet :

- loader simple (pas besoin de patcher tout le code)
- pages code en lecture seule → partage entre processus
- compatibilité avec ASLR

👉 sans PIC :

- la liaison dynamique moderne serait impraticable

---

Si tu veux pousser encore plus loin, on peut :

- comparer le même code compilé avec et sans `-fPIC` (désassemblage)
- analyser les différences de performance
- ou relier ça à des attaques type ROP / ret2plt (très lié au PIC)

### *Response:*
4/29/2026, 9:16:26 PM

Voici une vue synthétique mais rigoureuse du **cycle de vie des sections ELF liées à la liaison dynamique**, avec *qui les crée*, *quand*, et *comment elles sont utilisées*.

---

## 1. Vue d’ensemble

|Section / Élément|Créée quand|Par qui|Rôle|Modifiée quand|
|------------------|------------|--------|------|----------------|
|`.plt`| Link       | Linker (`ld`) | Stubs d’appel de fonctions | ❌ jamais |
| `.got`           | Link       | Linker | Table d’adresses (données) | ✔ load |
| `.got.plt`       | Link       | Linker | GOT pour fonctions (PLT) | ✔ load + runtime |
| `.rela.dyn`      | Link       | Linker | Relocations générales | ❌ (consommée au load) |
| `.rela.plt`      | Link       | Linker | Relocations des fonctions | ❌ (consommée lazy/runtime) |
| `.dynamic`       | Link       | Linker | Infos pour le loader | ❌ |
| `.text`          | Compile    | Compilateur | Code machine | ❌ |
| `.data/.bss`     | Compile    | Compilateur | Données globales | ✔ initialisation |

---

## 2. Phase 1 - Compilation (`gcc -c`)

### Créé par le compilateur :

- `.text`
- `.data`, `.bss`
- symboles non résolus
- **relocations partielles** (dans `.o`)

👉 À ce stade :

- pas de PLT
- pas de GOT globale
- pas de `.rela.plt` final

---

## 3. Phase 2 - Link (`ld`)

C’est ici que tout se structure.

### Le linker construit :

#### ✔ `.plt`

- génère un **stub par fonction externe**
- encode les appels indirects

#### ✔ `.got` et `.got.plt`

- réserve les emplacements mémoire
- initialise certaines entrées

#### ✔ `.rela.dyn`

- relocations pour :
  - variables globales
  - adresses relatives
  - GOT

#### ✔ `.rela.plt`

- relocations pour fonctions externes
- utilisées pour lazy binding

#### ✔ `.dynamic`

- table de configuration pour le loader :
  - adresse des relocations
  - dépendances (`.so`)
  - pointeurs GOT/PLT

👉 À ce stade :

- tout est **structurellement prêt**
- mais **aucune adresse réelle externe n’est résolue**

---

## 4. Phase 3 - Chargement (loader `ld-linux.so`)

### Étape 1 : mapping mémoire

- map toutes les sections :
  - `.text` → RX
  - `.got` → RW
  - `.plt` → RX

---

### Étape 2 : traitement de `.rela.dyn`

👉 **eager binding partiel**

Pour chaque entrée :

- `R_X86_64_RELATIVE`
  - calcul rapide : `base + offset`

- `R_X86_64_GLOB_DAT`
  - résolution symbole
  - écriture dans `.got`

👉 Résultat :

- variables globales prêtes
- GOT partiellement remplie

---

### Étape 3 : préparation de la PLT

- `.got.plt` initialisée avec :
  - pointeurs vers PLT fallback
  - adresse du resolver (`ld.so`)

👉 aucune résolution réelle encore pour les fonctions

---

## 5. Phase 4 - Exécution (runtime)

### Lazy binding (si activé)

#### Premier appel d’une fonction :

1. appel → `.plt`
2. `.plt` lit `.got.plt`
3. `.got.plt` pointe vers resolver
4. resolver :
   - cherche symbole (dans libc, etc.)
   - écrit adresse réelle dans `.got.plt`

#### Appels suivants :

- `.plt` → `.got.plt` → adresse directe

👉 `.got.plt` est **modifiée à runtime**

---

## 6. Cas eager binding (`LD_BIND_NOW=1`)

- `.rela.plt` est traitée **au load**
- toutes les entrées `.got.plt` sont remplies immédiatement

👉 pas de lazy binding

---

## 7. Récapitulatif par responsabilité

### Compilateur

- produit code + relocations intermédiaires

### Linker (`ld`)

- construit :
  - `.plt`
  - `.got`
  - `.rela.*`
  - `.dynamic`

👉 **met en place le mécanisme**

---

### Loader (`ld-linux.so`)

- lit `.dynamic`
- applique :
  - `.rela.dyn` (toujours)
  - `.rela.plt` (lazy ou eager)
- remplit la GOT

👉 **donne les vraies adresses**

---

## 8. Vision pipeline complète

```text
Compilation
  ↓
obj (.o) avec relocations partielles
  ↓
Link
  → construit .plt, .got, .rela.*
  ↓
Executable ELF
  ↓
Load (ld.so)
  → applique .rela.dyn
  → prépare lazy binding
  ↓
Runtime
  → .plt déclenche résolution
  → .got.plt patchée dynamiquement
```

---

## 9. Résumé ultra-condensé

- `.plt` → **créée au link**, jamais modifiée
- `.got` → **créée au link**, remplie au load
- `.got.plt` → **créée au link**, modifiée au runtime
- `.rela.dyn` → **créée au link**, consommée au load
- `.rela.plt` → **créée au link**, consommée au runtime (lazy)

---

## 10. Lecture “système”

- **linker = architecte**
- **loader = exécutant**
- **GOT = mémoire mutable**
- **PLT = interface d’appel**
- **relocations = instructions de patch**

---

Si tu veux, on peut aller encore plus loin :

- faire correspondre chaque entrée `.rela.plt` à une entrée `.plt`
- ou analyser un vrai ELF (avec `readelf` + `objdump`) pour voir tout ça concrètement
