# Recherches

Problématique : Comment garantir la rétrocompatibilité d'une bibliothèque partagée en optimisant l'espace et la performance ?

## Cadre

On suppose travailler avec une bibliothèque dont: \
    - on a modifié l'ABI, \
    - d'horloge à fréquence fixée à 1 GHz \
    - d'une RAM de 8 Gio/GiB \
    - de disque de 128 Gio/GiB \
exécutant un OS UNIX-like

## ld

[@ld](./recher  che_content/ld.md)

## Shared library/ELF

* [@elf](./recherche_content/elf.md)
* [@memory](./recherche_content/memory.md)

## Compression et recherche

* [@comp](./recherche_content/comp.md)
* [@search](./recherche_content/search.md)
* [@diffs](./recherche_content/diffs.md)

<s>
<details>
<summary>

## Signature

</summary>

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

</details></s>
