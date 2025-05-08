from inventaire.session import InventaireSession
from inventaire.utils.common import dict_merge, str_bool

from .paths import InventairePaths as Paths


class EndpointTemplate:
    """Class with basic constructor for endpoint classes"""

    def __init__(self, session: InventaireSession):
        self.session = session


class AuthEndpoints(EndpointTemplate):
    """
    Api wrapper for Auth. Login and stuffs. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/auth/auth.js
    """

    def login_user(self, username: str, password: str):
        """
        Authenticate a user with the provided credentials.

        Args:
            username (str): The user's username.
            password (str): The user's password.

        Returns:
            Response: The response object resulting from the POST request to the authentication endpoint.
        """
        json = {"username": username, "password": password}
        return self.session.post(Paths.AUTH, json=json)


class UserEndpoints(EndpointTemplate):
    """
    Api wrapper for Users. Read and edit authentified user data. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/user/user.js
    """

    def get_authentified_user(self):
        """
        Get the authentified user data.
        """
        return self.session.get(Paths.USERS)

    def update_authentified_user(self, attribute: str, value: str):
        """
        Update the authentified user.
        """
        json = {"attribute": attribute, "value": value}
        return self.session.put(Paths.USERS, json=json)


class ItemsEndpoints(EndpointTemplate):
    """
    Api wrapper for Items. What users' inventories are made of. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/items/items.js
    """

    def create_item(self, **params):
        """
        Create an item.
        """
        raise NotImplementedError

    def update_item(self, **params):
        """
        Update an item.
        """
        raise NotImplementedError

    def get_items_by_ids(self, **params):
        """
        Items by ids.
        """
        raise NotImplementedError

    def get_items_by_users(self, **params):
        """
        Items by users ids.
        """
        raise NotImplementedError

    def get_items_by_entities(self, **params):
        """
        Items by entities URIs.
        """
        raise NotImplementedError

    def get_last_public_items(self, **params):
        """
        Last public items.
        """
        return self.session.get(Paths.ITEMS_LAST_PUBLIC, params=params)

    def get_nearby_items(self, **params):
        """
        Last nearby items.
        """
        raise NotImplementedError

    def delete_item(self, **params):
        """
        Delete an item.
        """
        raise NotImplementedError


class EntitiesEndpoints(EndpointTemplate):
    """
    Api wrapper for Entities. Think books, authors, series data. See:
    - entities map: https://inventaire.github.io/entities-map/
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/entities/entities.js
    """

    def create_entity(self, **params):
        """
        Create an entity.
        """
        raise NotImplementedError

    def resolve_entity(self, **params):
        """
        Find if some entries match existing entities, and optionnaly update and/or enrich the existing entities, and/or create the missing ones.
        """
        raise NotImplementedError

    def update_label(self, **params):
        """
        Update an entity's label.
        """
        raise NotImplementedError

    def update_claim(self, **params):
        """
        Update an entity's claim.
        """
        raise NotImplementedError

    def revert_merge(self, **params):
        """
        Revert a merge. Requires to have dataadmin rights.
        """
        raise NotImplementedError

    def get_entities_by_uris(
        self,
        uris: str,
        refresh: bool | None = None,
        autocreate: bool | None = None,
        data: dict | None = None,
    ):
        """
        Get entities by URIs.

        Parameters:
            uris (str): A title, author, or ISBN (e.g. 'wd:Q3203603|isbn:9782290349229')
            refresh (bool, optional): Request non-cached data.
            autocreate (bool, optional): If True, create an item if it doesn't exist.
            data (dict, optional): Additional parameters to include in the request.

        Returns:
            Response: The HTTP response object from the POST request.
        """
        if data is None:
            data = {}

        params = {
            "uris": uris,
            **{
                k: v
                for k, v in {
                    "refresh": str_bool(refresh),
                    "autocreate": str_bool(autocreate),
                }.items()
                if v is not None
            },
        }
        params = dict_merge(data, params)
        return self.session.get(Paths.ENTITY_BY_URIS, params=params)

    def get_last_changes(self, **params):
        """
        Get entities last changes.
        """
        raise NotImplementedError

    def get_entities_by_claims(self, **params):
        """
        Get entities URIs by their claims.
        """
        raise NotImplementedError

    def get_popularity(self, **params):
        """
        Get popularity score of an entity.
        """
        raise NotImplementedError

    def get_history(self, **params):
        """
        Get entities history as snapshots and diffs.
        """
        raise NotImplementedError

    def get_author_works(self, **params):
        """
        Get an author's works.
        """
        raise NotImplementedError

    def get_serie_parts(self, **params):
        """
        Get a serie's parts.
        """
        raise NotImplementedError

    def get_publisher_publications(self, **params):
        """
        Get the publications of a publisher.
        """
        raise NotImplementedError

    def revert_edit(self, **params):
        """
        Revert an entity edit.
        """
        raise NotImplementedError

    def restore_version(self, **params):
        """
        Restores an entity to a past version.
        """
        raise NotImplementedError


class UsersEndpoints(EndpointTemplate):
    """
    Api wrapper for Users. Read and edit authentified user data. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/users/users.js
    """

    def get_users_by_ids(self, **params):
        """
        Users by ids.
        """
        raise NotImplementedError

    def get_users_by_usernames(self, **params):
        """
        Users by usernames.
        """
        raise NotImplementedError

    def search(self, **params):
        """
        Search users.
        """
        raise NotImplementedError


class GroupsEndpoints(EndpointTemplate):
    """
    Api wrapper for Groups. Read and edit users groups data. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/groups/groups.js
    """

    def get_groups(self, **params):
        """
        Get all the groups the authentified user is a member of.
        """
        raise NotImplementedError


class TransactionsEndpoints(EndpointTemplate):
    """
    Api wrapper for Transactions. When users request each others items. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/transactions/transactions.js
    """

    def get_transactions(self, **params):
        """
        Get the authentified user transactions data.
        """
        raise NotImplementedError

    def get_transaction_messages(self, **params):
        """
        Get messages associated to a transaction.
        """
        raise NotImplementedError


class SearchEndpoints(EndpointTemplate):
    """
    Api wrapper for Search. The generalist search endpoint. See:
    - code: https://github.com/inventaire/inventaire/blob/master/server/controllers/search/search.js
    """

    def search(
        self,
        search: str,
        types: str = "works|series|humans",
        limit: int | None = None,
        lang: str | None = None,
        exact: bool | None = None,
        min_score: int | None = None,
        data: dict | None = None,
    ):
        """
        Search for entities (works, humans, genres, publishers, series, collections), users, or groups.

        Parameters:
            search (str): The search term or query string.
            types (str): A pipe-separated string of entity types to search for
                         (possible values: works, humans, genres, publishers, series, collections, genres, movements, languages, users, groups, shelves, lists). Defaults to "works|series|humans".
            limit (int, optional): Maximum number of results to return.
            lang (str, optional): Language code to filter results by language.
            exact (bool, optional): If True, perform an exact match search.
            min_score (int, optional): Minimum relevance score for filtering results.
            data (dict, optional): Additional parameters to include in the request.

        Returns:
            Response: The HTTP response object from the POST request.
        """
        if data is None:
            data = {}

        params = {
            "search": search,
            "types": types,
            **{
                k: v
                for k, v in {
                    "limit": limit,
                    "lang": lang,
                    "exact": str_bool(exact),
                    "min_score": min_score,
                }.items()
                if v is not None
            },
        }
        params = dict_merge(data, params)
        return self.session.get(Paths.SEARCH, params=params)


class ShelvesEndpoints(EndpointTemplate):
    """
    Api wrapper for Shelves. List of items.
    Items must belong to the shelf' owner.
    An owner can add or remove items from their own shelf.
    An owner must be a user.
    """

    def get_shelves_by_ids(self, ids: str | list[str]):
        """
        Retrieve shelf data for the given shelf IDs.

        Args:
            ids (str or list[str]): A shelf ID separated by pipes as a string or a list of shelf IDs.

        Returns:
            Response: The response object resulting from the GET request to the shelves endpoint.
        """
        ids_str = "|".join(ids) if isinstance(ids, list) else ids
        return self.session.get(Paths.SHELVES_BY_IDS, params={"ids": ids_str})

    def get_shelves_by_owners(self, owners: str | list[str]):
        """
        Retrieve shelf data for the given owners ID.

        Args:
            ids (str or list[str]): A owner ID separated by pipes as a string or a list of owner IDs.

        Returns:
            Response: The response object resulting from the GET request to the shelves endpoint.
        """
        owners_str = "|".join(owners) if isinstance(owners, list) else owners
        return self.session.get(Paths.SHELVES_BY_OWNERS, params={"owners": owners_str})

    def create_shelf(
        self, name: str, listing: str, description: str, data: dict | None = None
    ):
        """
        Create a new shelf with the given details.

        Args:
            name (str): The name of the shelf.
            listing (str): The shelf visibility listing: one of private, network, or public.
            description (str): A description of the shelf.
            data (dict, optional): Additional data to merge into the request payload.

        Returns:
            Response: The response object resulting from the POST request to create the shelf.
        """
        if data is None:
            data = {}

        json = {"name": name, "listing": listing, "description": description}
        merged_json = dict_merge(data, json)
        return self.session.post(Paths.SHELVES_CREATE, json=merged_json)

    def update_shelf(
        self,
        id: str,
        name: str,
        listing: str,
        description: str | None = None,
        data: dict | None = None,
    ):
        """
        Update an existing shelf with the given details.

        Args:
            id (str): The shelf ID.
            name (str): The name of the shelf.
            listing (str): The shelf visibility listing: one of private, network, or public.
            description (str, optional): A description of the shelf.
            data (dict, optional): Additional data to merge into the request payload.

        Returns:
            Response: The response object resulting from the POST request to create the shelf.
        """
        if data is None:
            data = {}

        json = {"id": id, "name": name, "listing": listing}
        if description:
            json["description"] = description
        merged_json = dict_merge(data, json)
        return self.session.post(Paths.SHELVES_UPDATE, json=merged_json)

    def delete_shelf(self, id: str, data: dict | None = None):
        """
        Delete an existing shelf.

        Args:
            id (str): The shelf ID.
            data (dict, optional): Additional data to merge into the request payload.

        Returns:
            Response: The response object resulting from the POST request to create the shelf.
        """
        if data is None:
            data = {}

        json = {"id": id}
        merged_json = dict_merge(data, json)
        return self.session.post(Paths.SHELVES_DELETE, json=merged_json)


class DataEndpoints(EndpointTemplate):
    """
    Api wrapper for Data.
    """

    def request_extract_wikipedia(self, title: str, lang: str | None = None):
        """
        Request a summary extract from Wikipedia for a given article title and language.

        Args:
            title (str): The title of the Wikipedia article.
            lang (str, optional): The language code (e.g., 'en', 'fr') for the Wikipedia edition.

        Returns:
            Response: The response object from the GET request to retrieve the extract.
        """
        params = {"title": title}
        if lang:
            params["lang"] = lang
        return self.session.get(Paths.DATA_WP_EXTRACT, params=params)

    def get_isbn_basic_facts(self, isbn: str):
        """
        An endpoint to get basic facts from an ISBN.

        Args:
            isbn (str): 10 or 13, with or without hyphen.

        Returns:
            Response: The response object from the GET request to retrieve the extract.
        """
        params = {"isbn": isbn}
        return self.session.get(Paths.DATA_ISBN, params=params)

    def get_property_values(self, property: str, type: str):
        """
        Return the allowed values per type for a given property.

        Args:
            property (str): A property (e. g., 'wdt:P31').
            type (str): A type from lib/wikidata/aliases (e. g., 'series').

        Returns:
            Response: The response object from the GET request to retrieve the extract.
        """
        params = {"property": property, "type": type}
        return self.session.get(Paths.DATA_PROPERTY_VALUES, params=params)
