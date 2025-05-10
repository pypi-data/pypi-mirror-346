import pytest
from langchain_core.messages import AIMessageChunk

from langchain_vercel_adapters.stream_protocol.data_stream import (
    serialize_to_data_stream_protocol,
)

pytestmark = pytest.mark.asyncio


async def test_serialize_to_data_stream_protocol_with_groq():
    # Create mock chunks based on the input
    chunks = [
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content="Why",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" did",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" the",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" scare",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content="crow",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" win",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" an",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" award",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content="?",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" Because",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" he",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" was",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" outstanding",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" in",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" his",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=" field",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content=".\n\n",
            additional_kwargs={},
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
        ),
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 0,
                        "id": "call_0cdg",
                        "function": {
                            "arguments": '{"car_name": "BMW", "drivers_name": "John"}',
                            "name": "StartDriving",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
            tool_calls=[
                {
                    "name": "StartDriving",
                    "args": {"car_name": "BMW", "drivers_name": "John"},
                    "id": "call_0cdg",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "StartDriving",
                    "args": '{"car_name": "BMW", "drivers_name": "John"}',
                    "id": "call_0cdg",
                    "index": 0,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 1,
                        "id": "call_j10m",
                        "function": {
                            "arguments": '{"car_name": "BMW"}',
                            "name": "LockSeatbelt",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={},
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
            tool_calls=[
                {
                    "name": "LockSeatbelt",
                    "args": {"car_name": "BMW"},
                    "id": "call_j10m",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "LockSeatbelt",
                    "args": '{"car_name": "BMW"}',
                    "id": "call_j10m",
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={
                "finish_reason": "tool_calls",
                "model_name": "llama-3.1-8b-instant",
                "system_fingerprint": "fp_f7bd09b454",
            },
            id="run-23a4d42d-cd75-4569-82d7-6893b9ad3820",
            usage_metadata={
                "input_tokens": 287,
                "output_tokens": 57,
                "total_tokens": 344,
            },
        ),
    ]

    # Expected output
    expected_output = [
        'f:{"messageId":"run-23a4d42d-cd75-4569-82d7-6893b9ad3820"}\n',
        '0:"Why"\n',
        '0:" did"\n',
        '0:" the"\n',
        '0:" scare"\n',
        '0:"crow"\n',
        '0:" win"\n',
        '0:" an"\n',
        '0:" award"\n',
        '0:"?"\n',
        '0:" Because"\n',
        '0:" he"\n',
        '0:" was"\n',
        '0:" outstanding"\n',
        '0:" in"\n',
        '0:" his"\n',
        '0:" field"\n',
        '0:".\\n\\n"\n',
        'b:{"toolCallId":"call_0cdg","toolName":"StartDriving"}\n',
        'c:{"toolCallId":"call_0cdg","argsTextDelta":"{\\"car_name\\": \\"BMW\\", \\"drivers_name\\": \\"John\\"}"}\n',
        '9:{"toolCallId":"call_0cdg","toolName":"StartDriving","args":{"car_name": "BMW", "drivers_name": "John"}}\n',
        'b:{"toolCallId":"call_j10m","toolName":"LockSeatbelt"}\n',
        'c:{"toolCallId":"call_j10m","argsTextDelta":"{\\"car_name\\": \\"BMW\\"}"}\n',
        '9:{"toolCallId":"call_j10m","toolName":"LockSeatbelt","args":{"car_name": "BMW"}}\n',
        'e:{"finishReason":"tool-calls","usage":{"promptTokens":0,"completionTokens":0},"isContinued":false}\n',
    ]

    # Create an async generator from the chunks
    async def chunk_generator():
        for chunk in chunks:
            yield chunk

    # Convert the chunks to the data stream protocol format
    results = []
    async for protocol_chunk in serialize_to_data_stream_protocol(chunk_generator()):
        results.append(protocol_chunk)

    for x in results:
        print(repr(x))
    assert len(results) == len(expected_output)
    for i, (actual, expected) in enumerate(zip(results, expected_output)):
        if actual != expected:
            print("Actual:")
            print(actual)
            print("Expected:")
            print(expected)
        assert (
            actual == expected
        ), f"Mismatch at index {i}:\nExpected: {expected}\nActual: {actual}"
