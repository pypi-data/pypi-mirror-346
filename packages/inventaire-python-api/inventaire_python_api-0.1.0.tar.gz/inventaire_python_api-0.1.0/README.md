# Inventaire

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/inventaire-python-api)
![PyPI](https://img.shields.io/pypi/v/inventaire-python-api)
![PyPI - License](https://img.shields.io/pypi/l/inventaire-python-api)

### Project description

The package is a set of python wrappers for Inventaire.
Interact with Inventaire using python and create automation scripts to keep your library and database up-to-date.

For more detailed information please see [the project's documentation](https://inventaire-python-api.readthedocs.io/en/latest/index.html).

To be done:

- More usage examples
- Increase the tests coverage
- Convenient docs
- Implementing higher level wrappers

## Installation

```
pip install inventaire-python-api
```

## Authentication

Inventaire auth requires either the username or password or a cookie ([see the how-to](https://api.inventaire.io/#!/Auth/post_auth_action_login))

```python
from inventaire import Inventaire

auth = {"username": "demo-user", "password": "abcde1-fghij2-klmno3"}
inv = Inventaire.server_api(**auth)
```

## Usage

Then it is possible to interact with the low-level api wrappers:

```python
# Get information about the authenticated user
auth_data = inv.api.user.get_authentified_user()

# Get the last public items modified
last_items = inv.api.items.get_last_public_items()

# Get shelves information based on their ids
shelves_ids = inv.api.shelves.get_shelves_by_ids(
    ["b30491238f4a79a466c27418a2280c12", "0c490f3bc5ea9ab450bc24ff55151814"]
)

# Create a new shelf
new_shelf = inv.api.shelves.create_shelf(
    name="demo", listing="private", description="something"

# Get entity details and if it doesn't exist, try to create it
uri_details = inv.api.entities.get_entities_by_uris(
    uris="isbn:9789735087180",
    autocreate=True,
    refresh=True,
)
```

Each Inventaire API wrapper group could be accessed as a property:

```python
iapi = inv.api

# Items
items = iapi.items

# Shelves
shelves = iapi.shelves
```

## Troubleshooting

For troubleshooting see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## License

This library is licensed under the Apache 2.0 License.

## Links

[Inventaire docs](https://api.inventaire.io/)
