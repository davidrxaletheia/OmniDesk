from python.Classes.repos.category_repo import CategoryRepo as LegacyCategoryRepo


class CategoryRepo:
    """Wrapper around legacy `Classes.repos.category_repo.CategoryRepo`.

    Delegates common CRUD and convenience methods to the legacy repo so the
    rest of the application can import a stable interface from
    `python.app.repos`.
    """
    def __init__(self):
        self._legacy = LegacyCategoryRepo()

    def create(self, data: dict):
        return self._legacy.create(data)

    def get(self, category_id: int):
        return self._legacy.get(category_id)

    def list(self, limit: int = 50, offset: int = 0, **kwargs):
        return self._legacy.list(limit=limit, offset=offset)

    def update(self, category_id: int, data: dict):
        return self._legacy.update(category_id, data)

    def delete(self, category_id: int):
        return self._legacy.delete(category_id)

    def children(self, parent_id: int):
        return self._legacy.children(parent_id)

    def roots(self):
        return self._legacy.roots()
