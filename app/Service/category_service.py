from fastapi import HTTPException
from app.Repository.category_repository import CategoryRepository
from app.schemas.category import CursorPage
from app.utils.pagination import encode_cursor, decode_cursor
from app.core.logger import logger


class CategoryService:

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    # ── helpers ───────────────────────────────────────────────────────────────

    def _build_page(self, rows: list, limit: int, cursor_key: str) -> tuple:
        """
        Receives up to limit+1 rows from the DB.
        Returns (trimmed_rows, next_cursor, has_next).
        """
        has_next = len(rows) > limit
        if has_next:
            rows = rows[:limit]

        next_cursor = (
            encode_cursor({"after": getattr(rows[-1], cursor_key)})
            if has_next and rows
            else None
        )

        return rows, next_cursor, has_next

    def _parse_cursor(self, cursor: str | None) -> int | None:
        """Decodes cursor and returns after_id (or after_order)."""
        if not cursor:
            return None
        return decode_cursor(cursor).get("after")

    # ── non-paginated endpoints ───────────────────────────────────────────────

    def create_category(self, category):
        existing = self.repo.get_by_name_and_section(
            category.name, category.section_id
        )
        if existing:
            logger.warning(
                f"Duplicate category: {category.name} in section {category.section_id}"
            )
            raise HTTPException(
                status_code=400,
                detail="Category already exists in this section"
            )
        return self.repo.create(category)

    def get_category(self, category_id: int):
        category = self.repo.get_by_id(category_id)
        if not category:
            logger.warning(f"Category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def update_category(self, category_id: int, updates):
        category = self.repo.get_by_id(category_id)
        if not category:
            logger.warning(f"Update failed, category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")
        return self.repo.update(category, updates)

    def delete_category(self, category_id: int):
        category = self.repo.get_by_id(category_id)
        if not category:
            logger.warning(f"Delete failed, category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")
        self.repo.delete(category)
        return {"message": "Category deleted successfully"}

    # ── paginated endpoints ───────────────────────────────────────────────────

    def get_categories(
        self,
        section_id: int | None = None,
        cursor: str | None = None,
        limit: int = 10,
    ) -> CursorPage:
        after_id = self._parse_cursor(cursor)

        if section_id:
            rows = self.repo.get_by_section_paginated(section_id, after_id, limit)
        else:
            rows = self.repo.get_all_paginated(after_id, limit)

        rows, next_cursor, has_next = self._build_page(rows, limit, "id")

        for category in rows:
            if category.image_url:
                category.image_url = f"/static/{category.image_url}"

        return CursorPage(items=rows, next_cursor=next_cursor, has_next=has_next)

    def get_sections_with_categories(
        self,
        cursor: str | None = None,
        limit: int = 10,
    ) -> CursorPage:
        after_order = self._parse_cursor(cursor)
        rows = self.repo.get_sections_paginated(after_order, limit)
        rows, next_cursor, has_next = self._build_page(rows, limit, "display_order")

        for section in rows:
            if section.image_url:
                section.image_url = f"/static/{section.image_url}"
            for category in section.categories:
                if category.image_url:
                    category.image_url = f"/static/{category.image_url}"

        return CursorPage(items=rows, next_cursor=next_cursor, has_next=has_next)