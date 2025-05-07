from typing import Any, Iterable, Iterator, Optional
from uuid import uuid4

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import (
    Message,
    MessageParam,
    MessageStreamEvent,
)

from ...scribe import scribe
from ..logger import (
    Generation,
    GenerationConfig,
    Logger,
    Trace,
    TraceConfig,
)
from .async_client import MaximAnthropicAsyncClient
from .utils import AnthropicUtils


class MaximAnthropicClient:
    def __init__(self, client: Anthropic, logger: Logger):
        self._client = client
        self._logger = logger
        self._aio = MaximAnthropicAsyncClient(AsyncAnthropic(api_key=client.api_key), logger)

    def messages_stream(
        self,
        messages: Iterable[MessageParam],
        system:Optional[str] = None,
        *,
        model: str,
        max_tokens: int,
        trace_id: Optional[str] = None,
        generation_name: Optional[str] = None,
        **kwargs: Any,
    )->Iterator[MessageStreamEvent] :
        is_local_trace = trace_id is None
        final_trace_id = trace_id or str(uuid4())
        generation: Optional[Generation] = None
        trace: Optional[Trace] = None
        
        try:
            openai_style_messages = None
            if system is not None:
                openai_style_messages = [{"role": "system", "content": system}] + list(messages)
            trace = self._logger.trace(TraceConfig(id=final_trace_id))
            gen_config = GenerationConfig(
                id=str(uuid4()),
                model=model,
                provider="anthropic",
                name=generation_name,
                model_parameters=AnthropicUtils.get_model_params(
                    max_tokens=max_tokens,
                    **kwargs
                ),
                messages=AnthropicUtils.parse_message_param(
                    openai_style_messages if openai_style_messages is not None else messages #type:ignore
                ),
            )
            generation = trace.generation(gen_config)
        except Exception as e:
            scribe().warning(
                f"[MaximSDK][AnthropicClient] Error in generating content: {str(e)}"
            )

        response = self._client.messages.stream(
            **({'system': system} if system is not None else {}),
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            **kwargs
        )

        try:
            if generation is not None:
                 with response as response:
                    for event in response:
                        if event.type == "message_stop":
                            print(event.message)
                            generation.result(event.message)
                            if is_local_trace and trace is not None:
                                trace.end()
                        # generation.result(event)
                        yield event #type:ignore
            # if is_local_trace and trace is not None:
            #     trace.end()
        except Exception as e:
            scribe().warning(
                f"[MaximSDK][AnthropicClient] Error in logging generation: {str(e)}"
            )


    def messages(
        self,
        messages: Iterable[MessageParam],
        system:Optional[str] = None,
        *,
        model: str,
        max_tokens: int,
        trace_id: Optional[str] = None,
        generation_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Message:
        is_local_trace = trace_id is None
        final_trace_id = trace_id or str(uuid4())
        generation: Optional[Generation] = None
        trace: Optional[Trace] = None
        
        try:
            openai_style_messages = None
            if system is not None:
                openai_style_messages = [{"role": "system", "content": system}] + list(messages)
            trace = self._logger.trace(TraceConfig(id=final_trace_id))
            gen_config = GenerationConfig(
                id=str(uuid4()),
                model=model,
                provider="anthropic",
                name=generation_name,
                 model_parameters=AnthropicUtils.get_model_params(
                    max_tokens=max_tokens,
                    **kwargs
                ),
                messages=AnthropicUtils.parse_message_param(
                    openai_style_messages if openai_style_messages is not None else messages #type:ignore
                ),
            )
            generation = trace.generation(gen_config)
        except Exception as e:
            scribe().warning(
                f"[MaximSDK][AnthropicClient] Error in generating content: {str(e)}"
            )

        response = self._client.messages.create(
            **({'system': system} if system is not None else {}),
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            **kwargs
        )

        try:
            if generation is not None:
                generation.result(response)
            if is_local_trace and trace is not None:
                if response is not None:
                    trace.set_output(str(response.content))
                trace.end()
        except Exception as e:
            scribe().warning(
                f"[MaximSDK][AnthropicClient] Error in logging generation: {str(e)}"
            )

        return response

    @property
    def aio(self) -> MaximAnthropicAsyncClient:
        return self._aio