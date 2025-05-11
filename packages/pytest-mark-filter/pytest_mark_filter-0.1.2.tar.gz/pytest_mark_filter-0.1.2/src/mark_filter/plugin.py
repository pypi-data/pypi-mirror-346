import pytest
from typing import Iterator
from pytest import Mark


def _custom_iter_markers(item_name, iter_marker_fn):
    """
    Decorator to filter markers by name using match kw
    """

    def decor(name: str | None = None) -> Iterator[Mark]:
        for marker in iter_marker_fn(name):
            if sub_name := marker.kwargs.get("match"):
                if sub_name not in item_name:
                    continue
            if sub_name := marker.kwargs.get("not_match"):
                if sub_name in item_name:
                    continue
            yield marker

    return decor


@pytest.hookimpl(tryfirst=True)  # try to run first
def pytest_collection_modifyitems(items):
    """
    Replace iter markers with our filter
    """

    for item in items:
        item.iter_markers = _custom_iter_markers(item.name, item.iter_markers)
