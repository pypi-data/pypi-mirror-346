from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

# Basic JSON types
JSONValue = Union[None, str, int, float, bool, Dict[str, Any], List[Any]]


class LanguageModelUsage(BaseModel):
    """Represents the number of tokens used in a prompt and completion."""

    prompt_tokens: int = Field(
        ...,
        description="The number of tokens used in the prompt.",
        alias="promptTokens",
    )
    completion_tokens: int = Field(
        ...,
        description="The number of tokens used in the completion.",
        alias="completionTokens",
    )
    total_tokens: int = Field(
        ...,
        description="The total number of tokens used (promptTokens + completionTokens).",
        alias="totalTokens",
    )


class LanguageModelV1FinishReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    TOOL_CALLS = "tool_calls"
    ERROR = "error"


class LanguageModelV1Source(BaseModel):
    """Source information for language model responses."""

    type: str
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    text: Optional[str] = None


class Attachment(BaseModel):
    """An attachment that can be sent along with a message."""

    name: Optional[str] = Field(
        None, description="The name of the attachment, usually the file name."
    )
    content_type: Optional[str] = Field(
        None, description="A string indicating the media type.", alias="contentType"
    )
    url: str = Field(..., description="The URL of the attachment.")


# Tool-related models
class ToolCall(BaseModel):
    """Represents a tool call made by the assistant."""

    id: str
    type: str = "function"
    name: str
    args: Any


class ToolResult(BaseModel):
    """Represents the result of a tool call."""

    id: str
    type: str
    name: str
    args: Any
    result: Any


class ToolInvocationState(str, Enum):
    PARTIAL_CALL = "partial-call"
    CALL = "call"
    RESULT = "result"


class ToolInvocation(BaseModel):
    """Tool invocations are either tool calls or tool results."""

    state: ToolInvocationState
    step: Optional[int] = None
    tool_call_id: str = Field(alias="toolCallId")
    type: str | None = None
    tool_name: str = Field(alias="toolName")
    args: Optional[Any] = None
    result: Optional[Any] = None


# Message part types
class TextUIPart(BaseModel):
    """A text part of a message."""

    type: Literal["text"] = "text"
    text: str


class ReasoningDetails(BaseModel):
    type: str
    text: Optional[str] = None
    signature: Optional[str] = None
    data: Optional[str] = None


class ReasoningUIPart(BaseModel):
    """A reasoning part of a message."""

    type: Literal["reasoning"] = "reasoning"
    reasoning: str
    details: List[ReasoningDetails]


class ToolInvocationUIPart(BaseModel):
    """A tool invocation part of a message."""

    type: Literal["tool-invocation"] = "tool-invocation"
    tool_invocation: ToolInvocation = Field(alias="toolInvocation")


class SourceUIPart(BaseModel):
    """A source part of a message."""

    type: Literal["source"] = "source"
    source: LanguageModelV1Source


class FileUIPart(BaseModel):
    """A file part of a message."""

    type: Literal["file"] = "file"
    mime_type: str = Field(alias="mimeType")
    data: str


class StepStartUIPart(BaseModel):
    """A step boundary part of a message."""

    type: Literal["step-start"] = "step-start"


MessagePart = Union[
    TextUIPart,
    ReasoningUIPart,
    ToolInvocationUIPart,
    SourceUIPart,
    FileUIPart,
    StepStartUIPart,
]


class Message(BaseModel):
    """AI SDK UI Messages used to communicate between frontend and API routes."""

    id: str | None = Field(None, description="A unique identifier for the message.")
    created_at: datetime | None = Field(
        None, description="The timestamp of the message.", alias="createdAt"
    )
    content: str = Field(..., description="Text content of the message.")
    role: Literal["system", "user", "assistant", "data"] = Field(
        ..., description="The role of the message sender."
    )
    reasoning: Optional[str] = Field(None, description="Reasoning for the message.")
    experimental_attachments: Optional[List[Attachment]] = Field(
        default=None,
        description="Additional attachments for the message.",
        alias="experimentalAttachments",
    )
    data: Optional[JSONValue] = Field(None, description="For data messages.")
    annotations: Optional[List[JSONValue]] = Field(
        default=None,
        description="Additional message-specific information added on the server.",
    )
    tool_invocations: Optional[List[ToolInvocation]] = Field(
        default=None,
        description="Tool invocations that the assistant made.",
        alias="toolInvocations",
    )
    # parts: List[MessagePart] = Field(
    #     default_factory=list, description="The parts of the message for rendering in the UI."
    # )


class UIMessage(Message):
    """Message with guaranteed parts field for UI rendering."""

    parts: List[MessagePart]


class CreateMessage(BaseModel):
    """Message creation model with optional ID."""

    id: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    content: str
    role: Literal["system", "user", "assistant", "data"]
    reasoning: Optional[str] = None
    experimental_attachments: Optional[List[Attachment]] = Field(
        None, alias="experimentalAttachments"
    )
    data: Optional[JSONValue] = None
    annotations: Optional[List[JSONValue]] = None
    tool_invocations: Optional[List[ToolInvocation]] = Field(
        None, alias="toolInvocations"
    )
    parts: Optional[List[MessagePart]] = None


# Stream-related types
class AssistantStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    AWAITING_MESSAGE = "awaiting_message"


class StreamStringPrefixes(str, Enum):
    TEXT = "0"
    ERROR = "3"
    ASSISTANT_MESSAGE = "4"
    ASSISTANT_CONTROL_DATA = "5"
    DATA_MESSAGE = "6"


class AssistantMessage(BaseModel):
    """Represents a message from the assistant."""

    id: str
    role: Literal["assistant"] = "assistant"
    content: List[Dict[str, Any]]


class DataMessage(BaseModel):
    """Represents a data message."""

    id: Optional[str] = None
    role: Literal["data"] = "data"
    data: JSONValue


class AssistantControlData(BaseModel):
    """Control data for assistant messages."""

    thread_id: str = Field(alias="threadId")
    message_id: str = Field(alias="messageId")


# Request/response models
class ChatRequest(BaseModel):
    """Request model for chat API."""

    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    messages: List[Message]
    data: Optional[JSONValue] = None


class ChatRequestOptions(BaseModel):
    """Options for chat requests."""

    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    data: Optional[JSONValue] = None
    experimental_attachments: Optional[List[Attachment]] = Field(
        None, alias="experimentalAttachments"
    )
    allow_empty_submit: Optional[bool] = Field(False, alias="allowEmptySubmit")


class ChatMessages(BaseModel):
    id: str
    messages: List[UIMessage]


class UseChatOptions(BaseModel):
    """Options for chat functionality."""

    keep_last_message_on_error: Optional[bool] = Field(
        True, alias="keepLastMessageOnError"
    )
    api: Optional[str] = "/api/chat"
    id: Optional[str] = None
    initial_messages: Optional[List[Message]] = Field(None, alias="initialMessages")
    initial_input: Optional[str] = Field(None, alias="initialInput")
    on_response: Optional[Any] = Field(None, alias="onResponse")
    on_finish: Optional[Any] = Field(None, alias="onFinish")
    on_error: Optional[Any] = Field(None, alias="onError")
    credentials: Optional[str] = "same-origin"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    send_extra_message_fields: Optional[bool] = Field(
        False, alias="sendExtraMessageFields"
    )
    stream_protocol: Optional[Literal["data", "text"]] = Field(
        "data", alias="streamProtocol"
    )


class UseCompletionOptions(BaseModel):
    """Options for completion functionality."""

    api: Optional[str] = "/api/completion"
    id: Optional[str] = None
    initial_input: Optional[str] = Field(None, alias="initialInput")
    initial_completion: Optional[str] = Field(None, alias="initialCompletion")
    on_response: Optional[Any] = Field(None, alias="onResponse")
    on_finish: Optional[Any] = Field(None, alias="onFinish")
    on_error: Optional[Any] = Field(None, alias="onError")
    credentials: Optional[str] = "same-origin"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    stream_protocol: Optional[Literal["data", "text"]] = Field(
        "data", alias="streamProtocol"
    )


class UseAssistantOptions(BaseModel):
    """Options for assistant functionality."""

    api: str
    thread_id: Optional[str] = Field(None, alias="threadId")
    credentials: Optional[str] = "same-origin"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    on_error: Optional[Any] = Field(None, alias="onError")


# Streaming related models
class DataStreamStringPrefixes(str, Enum):
    TEXT = "0"
    DATA = "2"
    ERROR = "3"
    MESSAGE_ANNOTATIONS = "8"
    TOOL_CALL = "9"
    TOOL_RESULT = "a"
    TOOL_CALL_STREAMING_START = "b"
    TOOL_CALL_DELTA = "c"
    FINISH_MESSAGE = "d"
    FINISH_STEP = "e"
    START_STEP = "f"
    REASONING = "g"
    SOURCE = "h"
    REDACTED_REASONING = "i"
    REASONING_SIGNATURE = "j"
    FILE = "k"


class ToolCallStreamingStart(BaseModel):
    """Data for starting a streaming tool call."""

    tool_call_id: str = Field(alias="toolCallId")
    tool_name: str = Field(alias="toolName")


class ToolCallDelta(BaseModel):
    """Delta updates for a streaming tool call."""

    tool_call_id: str = Field(alias="toolCallId")
    args_text_delta: str = Field(alias="argsTextDelta")


class FinishMessage(BaseModel):
    """Message indicating the completion of a response."""

    finish_reason: LanguageModelV1FinishReason = Field(alias="finishReason")
    usage: Optional[Dict[str, int]] = None


class FinishStep(BaseModel):
    """Message indicating the completion of a step."""

    is_continued: bool = Field(alias="isContinued")
    finish_reason: LanguageModelV1FinishReason = Field(alias="finishReason")
    usage: Optional[Dict[str, int]] = None


class StartStep(BaseModel):
    """Message indicating the start of a step."""

    message_id: str = Field(alias="messageId")


class RedactedReasoning(BaseModel):
    """Redacted reasoning data."""

    data: str


class ReasoningSignature(BaseModel):
    """Signature for reasoning data."""

    signature: str


class FileData(BaseModel):
    """File data for streaming."""

    data: str
    mime_type: str = Field(alias="mimeType")
