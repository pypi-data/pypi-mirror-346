from collections.abc import Awaitable, Callable
from inspect import iscoroutinefunction
from typing import Any

# Pillar
from pillar.errors import PillarBlockError
from pillar.types import API_REQUEST, API_RESPONSE, AnalysisResponse, PillarMessage

# === Types ===

IsFlaggedCallable = Callable[[API_RESPONSE], bool]
"""Callable for checking if a response is flagged"""

OnFlaggedResultType = list[PillarMessage] | dict[str, Any] | PillarBlockError
"""List of messages or a PillarBlockError"""

OnFlaggedCallbackType = Callable[[API_REQUEST, API_RESPONSE], OnFlaggedResultType]
"""Callback for handling blocked content (must be synchronous)"""

CallbackResultType = None | Awaitable[None]
"""Return type for callbacks (None or awaitable None)"""

CallbackType = Callable[[API_REQUEST, API_RESPONSE], CallbackResultType]
"""Callback function signature for handling API responses"""

# === Helper Functions ===


def _is_async_callable(fn: Callable[..., Any]) -> bool:
    """Determine if a callable is asynchronous."""
    # Check if the function itself is async
    if iscoroutinefunction(fn):
        return True
    # Check if it's a callable class with an async __call__ method
    try:
        return iscoroutinefunction(type(fn).__call__)
    except AttributeError:
        return False


# === Block Detection ===


def is_analysis_response_flagged(analysis_response: AnalysisResponse) -> bool:
    """Check if an analysis response is flagged."""
    return analysis_response.flagged


def default_is_flagged(response: API_RESPONSE) -> bool:
    """Default flagged detector.

    Args:
        response: The API response to check

    Returns:
        bool: True if the response contains flagged content, False otherwise
    """
    if isinstance(response, AnalysisResponse):
        return is_analysis_response_flagged(response)
    return False


# === Default Callbacks ===


def perform_blocking(request: API_REQUEST, response: API_RESPONSE) -> OnFlaggedResultType:
    """Raise an error on flag.

    Args:
        request: API request data
        response: API response data

    Raises:
        PillarBlockError: Always raised with request and response data

    Returns:
        Never returns, always raises exception
    """
    raise PillarBlockError(request=request, response=response)


def perform_masking(request: API_REQUEST, response: API_RESPONSE) -> OnFlaggedResultType:
    """Mask flagged content in the response.

    Args:
        request: API request data
        response: API response data

    Returns:
        List[PillarMessage]: Messages with sensitive content masked,
        or original messages if something went wrong
    """

    fallback_messages = request.messages
    if not isinstance(response, AnalysisResponse):
        return fallback_messages
    if not response.masked_messages or not request.messages:
        return fallback_messages
    if len(request.messages) != len(response.masked_messages):
        return fallback_messages

    masked_messages: list[PillarMessage] = []
    # build masked messages
    for idx, msg in enumerate(request.messages):
        masked_content = response.masked_messages[idx]
        if isinstance(msg, PillarMessage):
            masked_msg = PillarMessage(
                role=msg.role,
                content=masked_content,
                tool_calls=msg.tool_calls,
                tool_call_id=msg.tool_call_id,
            )
            masked_messages.append(masked_msg)

    return masked_messages


def perform_monitoring(request: API_REQUEST, response: API_RESPONSE) -> OnFlaggedResultType:
    return request.messages
