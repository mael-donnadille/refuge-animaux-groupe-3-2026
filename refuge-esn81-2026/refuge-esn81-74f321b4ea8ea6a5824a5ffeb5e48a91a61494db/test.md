# Tests du projet Refuge

Ce document explique les tests du backend : comment les lancer, comment ils sont organisés et ce que vérifie chaque test.

## Lancer les tests

Depuis le dossier qui contient `pyproject.toml` :

```bash
poetry install
poetry run pytest -v
```

Lancer un seul fichier :

```bash
poetry run pytest tests/test_animal_service.py -v
```

Voir le taux de couverture (pourcentage de lignes de code exécutées par les tests) :

```bash
poetry add --group dev pytest-cov
poetry run pytest --cov=refuge_esn81 --cov-report=term-missing
```

Résultat actuel : **26 tests, tous au vert.**

Il n'y a pas besoin de MySQL ni de `DATABASE_URL` pour lancer les tests (voir plus bas).

## Organisation

```
tests/
├── conftest.py                       # préparation commune (base de test, client API)
├── test_species_service.py           # tests unitaires du service des espèces
├── test_animal_service.py            # tests unitaires du service des animaux
├── test_integration_species_api.py   # tests d'intégration des routes /api/species
├── test_integration_animals_api.py   # tests d'intégration des routes /api/animals
└── test_api.py                       # tests d'intégration complémentaires (genre, CORS)
```

On distingue deux types de tests, comme vu en cours :

- **Test unitaire** : il teste un seul élément, ici une méthode d'un service, directement en Python.
- **Test d'intégration** : il vérifie que plusieurs modules fonctionnent ensemble. On appelle une route HTTP avec le `TestClient` de FastAPI, et la requête traverse toute la chaîne : router → service → modèle → base de données.

Chaque test suit la même structure en 3 parties :

- `# Setup` : on prépare les données
- `# Action` : on lance ce qu'on veut tester
- `# Assert` : on vérifie que le résultat est celui attendu

Les cas d'erreur sont testés en plus des cas de succès. Pour vérifier qu'une erreur est bien levée, on utilise `with pytest.raises(...)`.

## conftest.py : la préparation commune

pytest charge automatiquement ce fichier avant les tests.

- Il définit `DATABASE_URL` sur SQLite, parce que `database.py` lit cette variable dès son import.
- La fixture **`db`** crée une base **SQLite en mémoire**, vide, pour chaque test. Les tests ne touchent donc jamais à la vraie base MySQL et ne dépendent pas les uns des autres.
- La fixture **`client`** crée un `TestClient` de l'API, et remplace `get_db` par la base de test grâce à `app.dependency_overrides` (injection de dépendances de FastAPI).

## test_species_service.py : service des espèces (unitaire)

| Test | Ce qu'il vérifie |
|---|---|
| `test_create_specie` | Une espèce créée reçoit un `id` et garde son nom. |
| `test_get_species_empty` | La liste est vide quand il n'y a aucune espèce. |
| `test_get_species` | Toutes les espèces créées sont renvoyées, dans l'ordre. |
| `test_get_species_limit` | Le paramètre `limit` limite bien le nombre de résultats (pagination). |
| `test_create_specie_duplicate_name_error` | La base refuse deux espèces avec le même nom (`IntegrityError`), car `name` est unique. |

## test_animal_service.py : service des animaux (unitaire)

| Test | Ce qu'il vérifie |
|---|---|
| `test_create_animal` | Un animal créé reçoit un `id`, et tous ses champs (nom, âge, genre, espèce) sont enregistrés. |
| `test_create_animal_relation_species` | La relation SQLAlchemy fonctionne dans les deux sens : `animal.species` donne l'espèce, et l'animal apparaît dans `espece.animals`. |
| `test_get_animals_empty` | La liste est vide quand il n'y a aucun animal. |
| `test_get_animals` | Tous les animaux créés sont renvoyés, dans l'ordre. |
| `test_get_animals_skip_limit` | `skip` et `limit` renvoient la bonne "page" d'animaux. |
| `test_create_animal_age_type_error` | Un âge qui n'est pas un nombre est refusé par le schéma Pydantic (`ValidationError`), et le message cite le champ `age`. |
| `test_create_animal_missing_field_error` | Un animal sans nom est refusé par le schéma Pydantic, et le message cite le champ `name`. |

## test_integration_species_api.py : routes des espèces (intégration)

| Test | Requête | Résultat attendu |
|---|---|---|
| `test_create_species_route` | `POST /api/species/` avec `{"name": "Chat"}` | 200, `{"id": 1, "name": "Chat"}` |
| `test_list_species_route_empty` | `GET /api/species/` sur une base vide | 200, `[]` |
| `test_list_species_route` | `GET /api/species/` après 2 créations | 200, les 2 espèces |
| `test_create_species_route_missing_name` | `POST /api/species/` avec `{}` | 422 (données invalides) |

## test_integration_animals_api.py : routes des animaux (intégration)

Données utilisées pour un animal :

```json
{
  "name": "Nouk",
  "age": 3,
  "description": "Chien tres gentil",
  "gender": "Mâle",
  "photo_url": "https://placedog.net/400",
  "species_id": 1
}
```

| Test | Requête | Résultat attendu |
|---|---|---|
| `test_create_animal_route` | `POST /api/animals/` avec une espèce existante | 200, l'animal avec son `id` et son espèce complète |
| `test_create_animal_route_unknown_species` | `POST /api/animals/` sans espèce en base | 404, `"Espece introuvable"` |
| `test_list_animals_route_empty` | `GET /api/animals/` sur une base vide | 200, `[]` |
| `test_list_animals_route` | `GET /api/animals/` après 2 créations | 200, les 2 animaux avec leur espèce |
| `test_create_animal_route_age_type_error` | `POST /api/animals/` avec `"age": "trois"` | 422 |
| `test_create_animal_route_missing_field` | `POST /api/animals/` sans `species_id` | 422 |

## test_api.py : tests complémentaires (intégration)

| Test | Ce qu'il vérifie |
|---|---|
| `test_species_can_be_created_and_listed` | Une espèce créée apparaît ensuite dans la liste. |
| `test_animal_can_be_created_and_listed_with_its_species` | Un animal créé est renvoyé avec tous ses champs et son espèce, puis apparaît dans la liste. |
| `test_animal_rejects_gender_outside_frontend_options` | Un genre autre que `Mâle`, `Femelle` ou `Inconnu` (les valeurs du front) est refusé avec une 422. |
| `test_frontend_origin_is_allowed_by_cors` | Le front (`http://localhost:3000`) a le droit d'appeler l'API (CORS). |

## Couverture

| Partie | Couverture |
|---|---|
| models, schemas, services, routers | 100 % |
| `main.py` | 92 % : seule la ligne `uvicorn.run(...)` n'est pas exécutée, car elle ne sert qu'à lancer le vrai serveur. |
| `database.py` | 67 % : `get_db` n'est pas exécutée, car les tests la remplacent par la base SQLite. |

## Limites connues

- Créer deux fois la même espèce **par l'API** renvoie aujourd'hui une erreur 500. La base refuse bien le doublon (testé dans `test_create_specie_duplicate_name_error`), mais la route ne transforme pas encore cette erreur en 400. Le test API correspondant sera ajouté quand la route sera corrigée.
- Les tests ne vérifient pas le front. La correspondance des noms de champs (`photo_url`) et des URL (`/api/animals`) se vérifie à la main avec le front.
