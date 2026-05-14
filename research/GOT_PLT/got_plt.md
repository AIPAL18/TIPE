# Global Offset Table (GOT) and Procedure Linkage Table (PLT)

Les **GOT** (*Global Offset Table*) et **PLT** (*Procedure Linkage Table*) sont au cœur du mécanisme de **liaison dynamique** dans les exécutables ELF (typiquement sous Linux). Leur rôle principal est de permettre à un programme compilé d’appeler des fonctions et d’accéder à des variables **dont l’adresse n’est connue qu’au moment de l’exécution**.

Je vais structurer ça proprement, comme on le ferait en architecture logicielle.

---

# 1. Problème à résoudre

Quand tu compiles avec une bibliothèque dynamique (`.so`) :

* les adresses des fonctions externes **ne sont pas connues à la compilation**
* elles ne sont même pas forcément connues au chargement (ASLR, relocation, etc.)

Donc :
👉 il faut un mécanisme **indirect** pour accéder aux symboles.

---

# 2. La GOT (Global Offset Table)

## Rôle

La GOT est une table en mémoire contenant des **adresses réelles** :

* fonctions externes
* variables globales externes

👉 C’est une table de **résolution d’adresses**.

## Principe

Au lieu de faire :

```asm
call printf
```

On fait :

```asm
call [adresse_dans_GOT]
```

Donc :

* la GOT contient des pointeurs
* ces pointeurs sont remplis par le linker dynamique (`ld-linux.so`)

## Types d’entrées

On distingue généralement :

* `.got` → variables globales
* `.got.plt` → fonctions (utilisées avec la PLT)

---

# 3. La PLT (Procedure Linkage Table)

## Rôle

La PLT sert à appeler des fonctions externes **de manière paresseuse (lazy binding)**.

👉 Elle agit comme un **stub (trampoline)**.

## Idée clé

La première fois que tu appelles une fonction externe :

1. tu passes par la PLT
2. la PLT appelle le linker dynamique
3. le linker résout l’adresse réelle
4. la GOT est mise à jour
5. les appels suivants vont directement à la bonne adresse

---

# 4. Interaction PLT ↔ GOT (le cœur du mécanisme)

## Appel d’une fonction externe

Prenons `printf`.

### Premier appel

1. Le code appelle `printf@plt`
2. L’entrée PLT fait :

   * un saut indirect via la GOT
   * MAIS la GOT pointe encore vers la PLT elle-même (fallback)
3. On arrive dans un resolver (`ld-linux`)
4. Le resolver :

   * trouve l’adresse réelle de `printf`
   * écrit cette adresse dans la GOT
5. Retour à l’appelant

### Appels suivants

* `printf@plt` → GOT → adresse réelle directe
* donc plus de coût de résolution

---

# 5. Structure typique d’une entrée PLT

Une entrée PLT ressemble à ça (simplifié) :

```asm
jmp *GOT[printf]
push index
jmp PLT[0]
```

* `jmp *GOT[...]` → appel indirect
* `push index` → identifiant du symbole
* `PLT[0]` → point d’entrée du resolver

---

# 6. Lazy binding vs eager binding

## Lazy binding (par défaut)

* résolution **au premier appel**
* plus rapide au démarrage
* mais overhead au premier call

## Eager binding (`LD_BIND_NOW=1`)

* toutes les adresses sont résolues au lancement
* startup plus lent
* appels ensuite plus rapides

---

# 7. Relocations associées

Deux types principaux :

* `R_X86_64_JUMP_SLOT` → pour la PLT (fonctions)
* `R_X86_64_GLOB_DAT` → pour la GOT (variables)

Ces entrées disent au linker dynamique :
👉 "remplis cette case de la GOT avec l’adresse réelle"

---

# 8. Sécurité (très important)

## Attaques classiques

### GOT overwrite

* si un attaquant modifie une entrée GOT
* il redirige un appel de fonction

👉 utilisé dans les exploits type **ret2plt**

## Contre-mesures

* **RELRO (Read-Only Relocations)** :

  * partiel : GOT encore modifiable
  * complet : GOT en lecture seule après init

* **ASLR**

* **PIE**

---

# 9. Avantages du mécanisme

* partage mémoire entre processus
* réduction taille des binaires
* mise à jour des libs sans recompiler
* chargement paresseux (performance)

---

# 10. Résumé mental (très utile)

Tu peux voir ça comme :

* **PLT = point d’entrée contrôlé (stub)**
* **GOT = table de pointeurs réels**

👉 Pipeline :

```
code → PLT → GOT → adresse réelle
```

---

# 11. Vision bas niveau (important pour ton TIPE)

* La PLT est du **code exécutable**
* La GOT est des **données modifiables**
* Le linker dynamique (`ld.so`) fait :

  * parsing ELF
  * résolution symbolique
  * patch de la GOT

---

# 12. Si tu veux aller encore plus loin

On peut creuser :

* désassemblage réel avec `objdump -d`
* inspection GOT/PLT avec `readelf -r`
* comportement avec/ sans `-fPIC`
* impact sur les performances
* exploitation (ret2plt, GOT hijacking)

---

Si tu veux, je peux te faire :

* un schéma mémoire ultra propre (niveau CPGE)
* ou analyser un binaire réel ligne par ligne (très formateur pour ton TIPE)

