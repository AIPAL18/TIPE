# Recherches

Problématique : Comment garantir la rétrocompatibilité d'une bibliothèque partagée en optimisant l'espace et la performance ?

## Cadre

On suppose travailler avec une bibliothèque dont: \
    - on a modifié l'ABI, \
    - d'horloge à fréquence fixée à 1 GHz \
    - d'une RAM de 8 Gio/GiB \
    - de disque de 128 Gio/GiB \
exécutant un OS UNIX-like

## Shared library

**[Shared Library](https://en.wikipedia.org/wiki/Shared_library)**

**[Executable and Linkable Format](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format)**

**[In-depth: ELF - The Extensible & Linkable Format](https://www.youtube.com/watch?v=nC1U1LJQL8o)**

Processus de résolution des symboles à l’exécution : \
  [https://guy-grave.developpez.com/articles/assemblage-edition-liens/](https://guy-grave.developpez.com/articles/assemblage-edition-liens/) \
  [Global Offset Table (GOT) and Procedure Linkage Table (PLT) [YTB]](https://www.youtube.com/watch?v=kUk5pw4w0h4)

**[Address space layout randomisation](https://en.wikipedia.org/wiki/Address_space_layout_randomization)**

**[GOT & PLT](https://reverseengineering.stackexchange.com/questions/1992/what-is-plt-got)**

## Data differencing

[source](https://hackernoon.com/delta-compression-diff-algorithms-and-delta-file-formats-practical-guide-7v1p3uhz)

### Delta

**[Delta encoding (wiki)](https://en.wikipedia.org/wiki/Delta_encoding)** :
  coucou

**[VCDIFF](https://en.wikipedia.org/wiki/VCDIFF)**

**[Xdelta](https://github.com/jmacd/xdelta)**

## Signature

Efficient for search, we don't care about how complexe it is to make.

### Database IDs

(*Le chat*)

| Concept/Field | Uniqueness Guarantee | Search Efficiency | Use Case | Example Tools/Algorithms |
| --- | --- | --- | --- | --- |
| Database Primary Keys | Yes | O(1) or O(log n) | Relational databases | Auto-increment, UUID |
| Hash Indexes | No* | O(1) | In-memory databases | Redis, Memcached |
| B-trees/B+ trees | Yes | O(log n) | Disk-based databases | MySQL, PostgreSQL |
| Distributed ID Generation | Yes | Varies | Microservices, global systems | Snowflake, ULID, UUID |
| Content-Addressable Storage | Yes** | O(1) | Version control, distributed FS | Git, IPFS |
| Perfect Hashing | Yes*** | O(1) | Static datasets, compilers | CMPH, CHD |

**[UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)** :

**Fingerprints**

**Data Fingerprinting**
