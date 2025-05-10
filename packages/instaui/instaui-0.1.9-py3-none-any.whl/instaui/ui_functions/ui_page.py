from typing import Callable
from instaui.launch_collector import get_launch_collector, PageInfo


def page(url: str = "/"):
    """Register a page route.

    Args:
        url (str): The route URL.
    """

    def wrapper(func: Callable):
        get_launch_collector().register_page(PageInfo(url, func))
        return func

    return wrapper
