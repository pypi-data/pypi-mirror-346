import json
from typing import Any, AsyncGenerator, cast

from langchain_core.messages import AIMessageChunk, ToolCallChunk
from pydantic import BaseModel


class ToolCall(BaseModel):
    id: str
    name: str
    args: str = ""


def _start_step_part(run_id: str) -> str:
    return 'f:{{"messageId":{id}}}\n'.format(id=json.dumps(run_id))


def _text(text: str) -> str:
    return "0:{text}\n".format(text=json.dumps(text))


def _tool_call_start(id: str, name: str) -> str:
    return 'b:{{"toolCallId":{id},"toolName":{name}}}\n'.format(
        id=json.dumps(id), name=json.dumps(name)
    )


def _tool_call_delta_part(id: str, delta: str) -> str:
    return 'c:{{"toolCallId":{id},"argsTextDelta":{delta}}}\n'.format(
        id=json.dumps(id), delta=json.dumps(delta)
    )


def _tool_call_end(tool_call: ToolCall | None) -> str:
    if tool_call is None:
        raise ValueError(
            "Attempting to add a tool call end part without a tool call start part"
        )
    return '9:{{"toolCallId":{id},"toolName":{name},"args":{args}}}\n'.format(
        id=json.dumps(tool_call.id),
        name=json.dumps(tool_call.name),
        args=tool_call.args,
    )


def _end_step_part(stop_reason: str, usage_metadata) -> str:
    """
    The finish step part needs to come at the end of a step.

    Format: e:{finishReason:'stop' | 'length' | 'content-filter' | 'tool-calls' | 'error' | 'other' | 'unknown';
    usage:{promptTokens:number; completionTokens:number;},isContinued:boolean}\n
    """
    allowed = {
        "stop",
        "length",
        "content-filter",
        "tool-calls",
        "error",
        "other",
        "unknown",
    }
    if stop_reason in ["tool_use", "tool_calls"]:
        stop_reason = "tool-calls"
    elif stop_reason == "stop":
        stop_reason = "stop"
    elif stop_reason == "end_turn":
        stop_reason = "other"
    else:
        stop_reason = "unknown"
    prompt_tokens = 0
    completion_tokens = 0
    return 'e:{{"finishReason":{stop_reason},"usage":{{"promptTokens":{prompt_tokens},"completionTokens":{completion_tokens}}},"isContinued":false}}\n'.format(
        stop_reason=json.dumps(stop_reason),
        prompt_tokens=json.dumps(prompt_tokens),
        completion_tokens=json.dumps(completion_tokens),
    )


async def serialize_to_data_stream_protocol(
    stream: AsyncGenerator[AIMessageChunk, None],
) -> AsyncGenerator[str, None]:
    """
    Serializes an async stream of AIMessageChunks into Vercel AI SDK's data stream protocol format.

    This function processes chunks from an LLM response stream and converts them into the format
    expected by Vercel's UI components. It handles text content, tool calls, and metadata,
    properly formatting the beginning and end of processing steps.

    Args:
        stream: An async generator that yields AIMessageChunk objects from an LLM.

    Returns:
        An async generator yielding strings formatted according to Vercel's data stream protocol.

    References:
        https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol#tool-call-streaming-start-part
    """
    # a new ID signals the beggining of a new "step"
    # i.e., one LLM API call in the backend
    step_id = None
    current_tool_call: ToolCall | None = None

    current_index = 0
    current_type = None

    async for chunk in stream:
        run_id = chunk.id

        # if the run_id is different from the step_id, we need to start a new step
        if isinstance(run_id, str) and run_id != step_id:
            yield _start_step_part(run_id)
            step_id = run_id
            # reset the state
            current_index = 0
            current_type = None
            current_tool_call = None

        content = chunk.content

        if isinstance(content, str):
            # if the content is empty and there is a stop reason, we need to end the step
            if content:
                yield _text(content)
                current_type = "text"

            response_metadata = chunk.response_metadata
            stop_reason = None
            fields = ["stop_reason", "finish_reason"]
            for field in fields:
                if field in response_metadata:
                    stop_reason = response_metadata[field]
            if stop_reason is not None:
                # if we are stopping and the last content was a tool call, we need to end the tool call
                if current_type == "tool_call":
                    yield _tool_call_end(current_tool_call)
                yield _end_step_part(stop_reason, chunk.usage_metadata or {})

        elif isinstance(content, list):
            for x in content:
                if isinstance(x, str):
                    current_type = "text"
                    yield _text(x)
                    continue

                x = cast(dict[str, Any], x)

                # this will be the case for the text part
                if x["type"] == "text":
                    current_type = "text"
                    current_index = x["index"]
                    yield _text(x["text"])

        else:
            raise ValueError(f"Invalid content type: {type(content)}")

        tool_call_chunks: list[ToolCallChunk] = chunk.tool_call_chunks

        for x in tool_call_chunks:
            if any(
                [
                    current_index is not None
                    and x["index"] != current_index
                    and current_type == "tool_call",
                ]
            ):
                yield _tool_call_end(current_tool_call)

            # this condition marks the start of a tool call
            if x["name"] is not None:
                id_ = x["id"] or ""
                current_tool_call = ToolCall(id=id_, name=x["name"])
                yield _tool_call_start(id_, x["name"])

            if current_tool_call is None:
                raise ValueError(
                    "Attempting to add a tool call delta part without a tool call start part"
                )
            args = x["args"] or ""
            yield _tool_call_delta_part(current_tool_call.id, args)
            # we update the tool call args in place
            current_tool_call.args += args

            current_index = x["index"]
            current_type = "tool_call"
