# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["SyncOffsetPage", "AsyncOffsetPage"]

_T = TypeVar("_T")


class SyncOffsetPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        count = self.count
        if count is None:
            return None

        length = len(self._get_page_items())
        current_count = count + length

        count = self.count
        if count is None:
            return None

        if current_count < count:
            return PageInfo(params={"offset": current_count})

        return None


class AsyncOffsetPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        count = self.count
        if count is None:
            return None

        length = len(self._get_page_items())
        current_count = count + length

        count = self.count
        if count is None:
            return None

        if current_count < count:
            return PageInfo(params={"offset": current_count})

        return None
