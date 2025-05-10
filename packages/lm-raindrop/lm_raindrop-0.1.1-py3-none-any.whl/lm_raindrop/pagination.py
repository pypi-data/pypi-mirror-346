# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional, cast
from typing_extensions import override

from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["SearchPagePagination", "SyncSearchPage", "AsyncSearchPage"]

_T = TypeVar("_T")


class SearchPagePagination(BaseModel):
    has_more: Optional[bool] = None

    total: Optional[int] = None

    total_pages: Optional[int] = None


class SyncSearchPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    results: List[_T]
    pagination: Optional[SearchPagePagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        results = self.results
        if not results:
            return []
        return results

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        last_page = cast("int | None", self._options.params.get("page")) or 1

        return PageInfo(params={"page": last_page + 1})


class AsyncSearchPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    results: List[_T]
    pagination: Optional[SearchPagePagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        results = self.results
        if not results:
            return []
        return results

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        last_page = cast("int | None", self._options.params.get("page")) or 1

        return PageInfo(params={"page": last_page + 1})
