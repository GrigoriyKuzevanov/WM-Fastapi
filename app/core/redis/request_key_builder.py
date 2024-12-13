from typing import Any, Callable

from fastapi import Request, Response


def request_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Request | None = None,
    response: Response | None = None,
    **kwargs: Any,
) -> str:
    """Builds a unique key for cache using requests details.

    Args:
        func (Callable[..., Any]): The function to decorate.
        namespace (str): A string prefix for key. Defaults to "".
        request (Request | None): Fastapi request object. Defaults to None.
        response (Response | None): Fastapi response object. Defaults to None.

    Returns:
        str: A string using to generate cache key.
    """

    return ":".join(
        [
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )
