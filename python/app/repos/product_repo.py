from python.Classes.repos.product_repo import ProductRepo as LegacyProductRepo


class ProductRepo:
    """Wrapper around legacy ProductRepo."""
    def __init__(self):
        self._legacy = LegacyProductRepo()

    def list(self, limit: int = 50, offset: int = 0):
        return self._legacy.list(limit=limit, offset=offset)

    def get(self, product_id: int):
        return self._legacy.get(product_id)

    def search(self, q: str, limit: int = 50):
        return self._legacy.search(q, limit=limit)

    def create(self, data: dict):
        return self._legacy.create(data)

    def update(self, product_id: int, data: dict):
        return self._legacy.update(product_id, data)

    def delete(self, product_id: int):
        return self._legacy.delete(product_id)
