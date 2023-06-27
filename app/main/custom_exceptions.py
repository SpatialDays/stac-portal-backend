class Error(Exception):
    pass


class StoredSearchParametersDoesNotExistError(Error):
    pass


class CatalogDoesNotExistError(Error):
    pass

class PublicCatalogNotPublicOrValidError(Error):
    pass

class PublicCatalogDoesNotExistError(CatalogDoesNotExistError):
    pass


class CatalogAlreadyExistsError(Error):
    pass


class MicroserviceIsNotAvailableError(Error):
    pass


class ConvertingTimestampError(Error):
    pass


class TemporalExtentError(Error):
    pass


class CollectionAlreadyExistsError(Error):
    pass


class PrivateCollectionAlreadyExistsError(CollectionAlreadyExistsError):
    pass


class InvalidCollectionPayloadError(Error):
    pass


class CollectionDoesNotExistError(Error):
    pass


class PublicCollectionDoesNotExistError(CollectionDoesNotExistError):
    pass


class PrivateCollectionDoesNotExistError(CollectionDoesNotExistError):
    pass


class ItemAlreadyExistsError(Error):
    pass


class PrivateItemAlreadyExistsError(ItemAlreadyExistsError):
    pass


class ItemDoesNotExistError(Error):
    pass


class APIMUserAlreadyExistsError(Exception):
    pass


class APIMUserNotFoundError(Exception):
    pass


class APIMUserCreationError(Exception):
    pass


class APIMSubscriptionCreationError(Exception):
    pass


class APIMSubscriptionAlreadyExistsError(Exception):
    pass


class APIMSubscriptionNotFoundError(Exception):
    pass


class APIMSubscriptionKeyRefreshError(Exception):
    pass
