from abc import ABC, abstractmethod
from typing import Self, Any


def _normalized_idx(idx: int, min_idx: int, max_idx: int) -> int:
    if idx < 0:
        idx = max_idx - idx + 1
    if idx < min_idx or idx > max_idx:
        return None
    return idx


def _normalized_range(idx_0: int, idx_1: int, min_idx: int, max_idx: int) -> list[int]:
    # make sure they're in the right order
    if idx_0 > idx_1:
        idx_0, idx_1 = idx_1, idx_0

    if idx_0 > max_idx or idx_1 < min_idx:
        return []

    idx_0 = max(idx_0, min_idx)
    idx_1 = min(idx_1, max_idx)
    return list(range(idx_0, idx_1 + 1))


def _get_view(expr: str, min_idx: int, max_idx: int) -> list[int]:
    if expr == "all":
        return list(range(min_idx, max_idx + 1))

    result = []
    for subexpr in expr.split(","):
        if ":" not in subexpr:
            idx = _normalized_idx(int(subexpr), min_idx, max_idx)
            if idx is not None:
                result.append(idx)
        else:
            idx_0, idx_1 = subexpr.split(":")

            # such that n: means n:max and :n means min:n
            idx_0 = min_idx if idx_0 == "" else int(idx_0)
            idx_1 = max_idx if idx_1 == "" else int(idx_1)

            result.extend(_normalized_range(idx_0, idx_1, min_idx, max_idx))

    return result


def _swap_indices(input: list, idx_0: int, idx_1: int):
    input[idx_0], input[idx_1] = input[idx_1], input[idx_0]
    return input


def _append_to(input: list, elem: Any) -> list:
    input.append(elem)
    return input


def _extend_with(input: list, other: list) -> list:
    input.extend(other)
    return input


def _apply_to_one(input: list, func, idx: int, *args, **kwargs) -> list:
    input[idx] = func(input[idx], *args, **kwargs)
    return input


def _apply_to_subset(input: list, func, indices: list[int], *args, **kwargs) -> list:
    for idx in indices:
        input[idx] = func(input[idx], *args, **kwargs)
    return input


def _weave_with(input: list, other: list) -> list:
    result = []
    for odd, even in zip(input, other):
        result.extend([odd, even])

    input_len = len(input)
    other_len = len(other)

    if input_len > other_len:
        result.extend(input[other:len:])
    elif other_len > input_len:
        result.extend(other[input_len:])

    return result


class PageContainer(ABC):
    @abstractmethod
    def get_pages(self) -> list[Any]:
        pass

    @abstractmethod
    def set_pages(self, pages: list[Any]):
        pass

    # methods inherited by any object implementing the PageContainer
    # interface; I use the pages_ prefix in all of them so that it's
    # always clear they are implemented here.
    def pages_len(self) -> int:
        return len(self.get_pages())

    def pages_apply(self, func, *args, **kwargs) -> Self:
        self.set_pages(func(self.get_pages(), *args, **kwargs))
        return self

    def pages_pop(self, idx: int) -> Any:
        pages = self.get_pages()
        result = pages.pop(idx)
        self.set_pages(pages)
        return result

    def pages_insert(self, idx: int, page: Any) -> Self:
        return self.pages_apply(lambda pages, i, page: pages.insert(i, page), idx, page)

    def pages_invert(self) -> Self:
        return self.pages_apply(lambda pages: pages[::-1])

    def pages_swap(self, idx_0: int, idx_1: int) -> Self:
        return self.pages_apply(_swap_indices, idx_0, idx_1)

    def pages_append(self, page: Any) -> Self:
        return self.pages_apply(_append_to, page)

    def pages_extend(self, pages: list[Any]) -> Self:
        return self.pages_apply(_extend_with, pages)

    def pages_merge(self, other: Self) -> Self:
        return self.pages_extend(other.get_pages())

    def pages_weave(self, other: Self) -> Self:
        return self.pages_apply(_weave_with, other.get_pages())

    def pages_select(self, predicate) -> Self:
        self.set_pages([
            page for page in self.get_pages()
            if predicate(page)
        ])
        return self

    def pages_filter(self, predicate) -> Self:
        self.set_pages([
            page for idx, page in enumerate(self.get_pages())
            if predicate(idx)
        ])
        return self

    def pages_subset(self, indices: list[int]) -> Self:
        pages = self.get_pages()
        self.set_pages([
            pages[idx] for idx in indices
        ])
        return self

    def pages_view(self, expr: str, offset = 0) -> list[int]:
        result = _get_view(expr, offset, self.pages_len())
        return [idx - offset for idx in result]

    def pages_slice(self, expr: str, offset = 0) -> Self:
        return self.pages_subset(self.pages_view(expr, offset = offset))

    def pages_map(self, func, *args, **kwargs) -> Self:
        self.set_pages([
            func(page, *args, **kwargs) for page in self.get_pages()
        ])
        return self

    def pages_map_one(self, func, idx: int, *args, **kwargs) -> Self:
        return self.pages_apply(_apply_to_one, idx, *args, **kwargs)

    def pages_map_if(self, func, predicate, *args, **kwargs) -> Self:
        self.set_pages([
            func(page, *args, **kwargs) if predicate(idx) else page
            for idx, page in enumerate(self.get_pages())
        ])
        return self

    def pages_map_subset(self, func, indices: list[int], *args, **kwargs) -> Self:
        return self.pages_apply(_apply_to_subset, func, indices, *args, **kwargs)

    def pages_map_slice(self, func, expr: str, offset = 1, *args, **kwargs) -> Self:
        indices = self.pages_view(expr, offset = offset)
        return self.pages_map_subset(func, indices, *args, **kwargs)
