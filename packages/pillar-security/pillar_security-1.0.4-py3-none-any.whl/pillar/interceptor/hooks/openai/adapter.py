import traceback
from collections.abc import AsyncGenerator, AsyncIterable, Callable, Generator, Iterable
from enum import Enum
from typing import TYPE_CHECKING, Any, cast

from pillar.callbacks import OnFlaggedResultType
from pillar.errors import PillarBlockError
from pillar.interceptor.hooks.framework_adapter import ExtractedInput, FrameworkAdapter
from pillar.interceptor.hooks.hook_factory import create_generic_hook
from pillar.interceptor.hooks.openai.format_utils import (
    KNOWN_ROLE_PREFIXES,
    parse_completion_to_pillar_messages,
    pillar_messages_to_completion,
)
from pillar.interceptor.hooks.openai.stream_utils import (
    ChatCompletionChunk,
    CompletionChunk,
    chat_completion_stream_collector,
    completion_stream_collector,
)
from pillar.types import PillarMessage, Role

if TYPE_CHECKING:
    from pillar.client import Pillar


class OpenAIAPIType(Enum):
    CHAT = "chat"
    COMPLETION = "completion"


# --- OpenAI Specific Adapters ---


class BaseOpenAIAdapter(FrameworkAdapter):
    """Base adapter for common OpenAI logic."""

    @property
    def provider_name(self) -> str:
        return "openai"

    def _common_extract_input(
        self, args: tuple, kwargs: dict, input_arg_name: str, api_type: OpenAIAPIType
    ) -> ExtractedInput:
        """Helper to extract common arguments."""
        input_data = kwargs.get(input_arg_name)
        model = kwargs.get("model")
        stream = kwargs.get("stream", False)
        tools = (
            kwargs.get("tools") if api_type == OpenAIAPIType.CHAT else None
        )  # Tools only for chat

        return ExtractedInput(
            input_data=input_data,
            input_arg_name=input_arg_name,
            model=model,
            stream=stream,
            tools=tools,
            api_type=api_type,
            is_async=self.is_async,
            original_kwargs=kwargs.copy(),  # Store a copy
        )

    # --- Stream Handling (Reusing logic from old base_hook) ---
    def _handle_sync_stream_internal(
        self,
        pillar: "Pillar",
        stream_result: Iterable[ChatCompletionChunk | CompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],
        collector_func: Callable[[list[Any]], list[PillarMessage]],
    ) -> Generator[ChatCompletionChunk | CompletionChunk, None, None]:
        """Internal logic for sync stream handling.

        Iterates through the stream, yields chunks, and performs analysis
        after the stream is exhausted.
        """
        chunks = []
        api_type = extracted_input.api_type
        try:
            for chunk in stream_result:
                chunks.append(chunk)
                yield chunk
        except Exception as e:
            self.logger.error(
                f"Exception during OpenAI sync {api_type.value} stream passthrough: {e}"
            )
            self.logger.debug(traceback.format_exc())
            return

        try:
            messages = collector_func(chunks)
            if messages:
                analyze_kwargs = {
                    "messages": messages,
                    "model": extracted_input.model,
                    "provider": self.provider_name,
                    "tools": extracted_input.tools,  # Will be None for completion
                }
                _ = analyze_func(**analyze_kwargs)
        except PillarBlockError as blocking_error:
            raise blocking_error
        except Exception as e:
            self.logger.error(
                f"Exception during {analyze_func.__name__} OpenAI sync {api_type.value}: {e}"
            )
            self.logger.debug(traceback.format_exc())

    async def _handle_async_stream_internal(
        self,
        pillar: "Pillar",
        stream_result: AsyncIterable[ChatCompletionChunk | CompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],  # Should be an async function
        collector_func: Callable[[list[Any]], list[PillarMessage]],
    ) -> AsyncGenerator[ChatCompletionChunk | CompletionChunk, None]:
        """Internal logic for async stream handling.

        Asynchronously iterates through the stream, yields chunks, and performs
        analysis after the stream is exhausted.
        """
        chunks = []
        api_type = extracted_input.api_type
        try:
            async for chunk in stream_result:
                chunks.append(chunk)
                yield chunk
        except Exception as e:
            self.logger.error(
                f"Exception during OpenAI async {api_type.value} stream passthrough: {e}"
            )
            self.logger.debug(traceback.format_exc())
            return

        try:
            messages = collector_func(chunks)
            if messages:
                analyze_kwargs = {
                    "messages": messages,
                    "model": extracted_input.model,
                    "provider": self.provider_name,
                    "tools": extracted_input.tools,  # Will be None for completion
                }
                _ = await analyze_func(**analyze_kwargs)
        except Exception as e:
            # Note: analyze_async does not raise PillarBlockError
            self.logger.error(
                f"Exception during {analyze_func.__name__} OpenAI async {api_type.value}: {e}"
            )
            self.logger.debug(traceback.format_exc())


class OpenAIChatAdapter(BaseOpenAIAdapter):
    """Adapter for OpenAI Chat Completion API."""

    def extract_input(self, args: tuple, kwargs: dict) -> ExtractedInput:
        return self._common_extract_input(
            args, kwargs, input_arg_name="messages", api_type=OpenAIAPIType.CHAT
        )

    def format_input_for_pillar(
        self, pillar: "Pillar", extracted_input: ExtractedInput
    ) -> tuple[list[PillarMessage], Any]:
        """
        Format the input for the Pillar framework.

        Chat messages are already in a compatible list format
        No special formatting context needed
        """
        # in the chat completion case, the input_data is already a list of dicts
        is_list = isinstance(extracted_input.input_data, list)
        dict_list = is_list and all(isinstance(item, dict) for item in extracted_input.input_data)
        if dict_list:
            messages = [PillarMessage(**msg) for msg in extracted_input.input_data]
        else:
            # fallback
            messages = []
        return messages, None

    def format_output_from_pillar(
        self,
        pillar: "Pillar",
        processed_input: OnFlaggedResultType,
        original_formatting_metadata: Any,
        extracted_input: ExtractedInput,
    ) -> Any:
        """
        Format the output from the Pillar framework.

        Assume processed_input is the potentially modified list of messages
        """
        if isinstance(processed_input, list):
            return processed_input
        elif isinstance(processed_input, dict):  # Single message dict
            return [PillarMessage(**processed_input)]
        else:
            self.logger.warning(f"Unexpected type: {type(processed_input)}. Using original.")
            return extracted_input.input_data  # Fallback

    def handle_sync_stream(
        self,
        pillar: "Pillar",
        stream_result: Iterable[ChatCompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],
    ) -> Generator[ChatCompletionChunk, None, None]:
        """Handle sync stream for Chat Completion, calling the internal helper.

        Calls the internal sync generator function (_handle_sync_stream_internal)
        which immediately returns the generator object.
        """
        # cast the return type to the expected type, as the internal function is generic
        new_stream_result = cast(
            Generator[ChatCompletionChunk, None, None],
            self._handle_sync_stream_internal(
                pillar,
                stream_result,
                extracted_input,
                analyze_func,
                chat_completion_stream_collector,
            ),
        )
        return new_stream_result

    def handle_async_stream(
        self,
        pillar: "Pillar",
        stream_result: AsyncIterable[ChatCompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        """Handle async stream for Chat Completion, calling the internal helper.

        Calls the internal async generator function (_handle_async_stream_internal)
        which immediately returns the async generator object.
        """
        # cast the return type to the expected type, as the internal function is generic
        new_stream_result = cast(
            AsyncGenerator[ChatCompletionChunk, None],
            self._handle_async_stream_internal(
                pillar,
                stream_result,
                extracted_input,
                analyze_func,
                chat_completion_stream_collector,
            ),
        )
        return new_stream_result

    def extract_output_for_pillar(
        self, pillar: "Pillar", result: Any, extracted_input: ExtractedInput
    ) -> list[PillarMessage] | None:
        """Extract the output from the OpenAI API.

        If the result is a ChatCompletion object, extract the messages.
        """
        if hasattr(result, "choices") and result.choices:
            # Ensure messages are dicts for analysis
            try:
                output_dicts = [choice.message.to_dict() for choice in result.choices]
                messages = [PillarMessage(**msg_dict) for msg_dict in output_dicts]
                return messages
            except Exception as e:
                self.logger.error(f"Failed to convert OpenAI chat choices to dicts: {e}")
                return None
        else:
            self.logger.warning(f"No choices found in OpenAI chat response object: {type(result)}")
            return None


class OpenAICompletionAdapter(BaseOpenAIAdapter):
    """Adapter for OpenAI Completion API (Legacy)."""

    def extract_input(self, args: tuple, kwargs: dict) -> ExtractedInput:
        return self._common_extract_input(
            args, kwargs, input_arg_name="prompt", api_type=OpenAIAPIType.COMPLETION
        )

    def format_input_for_pillar(
        self, pillar: "Pillar", extracted_input: ExtractedInput
    ) -> tuple[list[PillarMessage], Any]:
        # Need to parse the prompt string/list into PillarMessages
        # Also need to track if role prefixes were used.
        prompt = extracted_input.input_data
        had_role_prefix = isinstance(prompt, str) and any(
            prompt.strip().startswith(p) for p in KNOWN_ROLE_PREFIXES
        )
        messages = parse_completion_to_pillar_messages(prompt)
        return messages, had_role_prefix  # Pass had_role_prefix as context

    def format_output_from_pillar(
        self,
        pillar: "Pillar",
        processed_input: OnFlaggedResultType,
        original_formatting_metadata: Any,  # This is had_role_prefix
        extracted_input: ExtractedInput,
    ) -> Any:
        """
        Format the output from the Pillar framework.

        Convert pillar messages back to a flat string, respecting original prefix usage
        """
        had_role_prefix = original_formatting_metadata
        final_prompt = pillar_messages_to_completion(processed_input, had_role_prefix)
        return final_prompt

    def handle_sync_stream(
        self,
        pillar: "Pillar",
        stream_result: Iterable[CompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],
    ) -> Generator[CompletionChunk, None, None]:
        """Handle sync stream for Completion, calling the internal helper.

        Calls the internal sync generator function (_handle_sync_stream_internal)
        which immediately returns the generator object.
        """
        # cast the return type to the expected type, as the internal function is generic
        return cast(
            Generator[CompletionChunk, None, None],
            self._handle_sync_stream_internal(
                pillar, stream_result, extracted_input, analyze_func, completion_stream_collector
            ),
        )

    def handle_async_stream(
        self,
        pillar: "Pillar",
        stream_result: AsyncIterable[CompletionChunk],
        extracted_input: ExtractedInput,
        analyze_func: Callable[..., Any],
    ) -> AsyncGenerator[CompletionChunk, None]:
        """Handle async stream for Completion, calling the internal helper.

        Calls the internal async generator function (_handle_async_stream_internal)
        which immediately returns the async generator object.
        """
        # cast the return type to the expected type, as the internal function is generic
        return cast(
            AsyncGenerator[CompletionChunk, None],
            self._handle_async_stream_internal(
                pillar, stream_result, extracted_input, analyze_func, completion_stream_collector
            ),
        )

    def extract_output_for_pillar(
        self, pillar: "Pillar", result: Any, extracted_input: ExtractedInput
    ) -> list[PillarMessage] | None:
        """Extract the output from the OpenAI API.

        If the result is a Completion object, extract the text.
        """
        if hasattr(result, "choices") and result.choices:
            try:
                completion_text = result.choices[0].text
                # Convert completion text to a single PillarMessage
                output_messages = [
                    PillarMessage(role=Role.ASSISTANT.value, content=completion_text)
                ]
                return output_messages
            except (AttributeError, IndexError) as e:
                self.logger.error(f"Failed to extract text from OpenAI completion choice: {e}")
                return None
        else:
            self.logger.warning(
                f"No choices found in OpenAI completion response object: {type(result)}"
            )
            return None


# --- Factory Function ---


def create_openai_hook_factory(
    pillar: "Pillar",
    is_async: bool,
    api_type: Enum,
) -> Callable:
    """
    Factory to create OpenAI hook functions using the generic hook and specific adapters.
    """
    adapter: FrameworkAdapter
    if api_type == OpenAIAPIType.CHAT:
        adapter = OpenAIChatAdapter(is_async=is_async, logger=pillar.logger)
    elif api_type == OpenAIAPIType.COMPLETION:
        adapter = OpenAICompletionAdapter(is_async=is_async, logger=pillar.logger)
    else:
        raise ValueError(f"Unsupported OpenAI API type: {api_type.value}")

    # Create and return the hook using the generic creator and the chosen adapter
    return create_generic_hook(pillar, adapter)
