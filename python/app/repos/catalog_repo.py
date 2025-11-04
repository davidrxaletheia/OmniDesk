from python.Classes.repos.catalog_repo import CatalogRepo as LegacyCatalogRepo


class CatalogRepo:
    """Wrapper around legacy CatalogRepo."""
    def __init__(self):
        self._legacy = LegacyCatalogRepo()

    def list(self, limit: int = 50, offset: int = 0):
        return self._legacy.list(limit=limit, offset=offset)

    def get(self, catalog_id: int):
        return self._legacy.get(catalog_id)

    def actives(self):
        return self._legacy.actives()

    def create(self, data: dict):
        return self._legacy.create(data)

    def update(self, catalog_id: int, data: dict):
        return self._legacy.update(catalog_id, data)

    def delete(self, catalog_id: int):
        return self._legacy.delete(catalog_id)
