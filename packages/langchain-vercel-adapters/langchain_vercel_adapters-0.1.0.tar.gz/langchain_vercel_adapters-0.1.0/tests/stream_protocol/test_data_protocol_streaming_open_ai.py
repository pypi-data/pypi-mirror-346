import pytest
from langchain_core.messages import AIMessageChunk

from langchain_vercel_adapters.stream_protocol.data_stream import (
    serialize_to_data_stream_protocol,
)

pytestmark = pytest.mark.asyncio


async def test_serialize_to_data_stream_protocol_with_chunked_tool_calls():
    # Create mock chunks based on the input
    chunks = [
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content="Why",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" don't",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" scientists",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" trust",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" atoms",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content="?",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" Because",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" they",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" make",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" up",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" everything",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content="!\n\n",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content="Now",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=",",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" let's",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" get",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" started",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" with",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" the",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" BMW",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" and",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" ensure",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" the",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" seat",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content="belt",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" is",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=" locked",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        AIMessageChunk(
            content=".",
            additional_kwargs={},
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
        # First tool call - StartDriving
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 0,
                        "id": "call_TCmtOURVFGzvGWiS6MZgAMn5",
                        "function": {"arguments": "", "name": "StartDriving"},
                        "type": "function",
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            tool_calls=[
                {
                    "name": "StartDriving",
                    "args": {},
                    "id": "call_TCmtOURVFGzvGWiS6MZgAMn5",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "StartDriving",
                    "args": "",
                    "id": "call_TCmtOURVFGzvGWiS6MZgAMn5",
                    "index": 0,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        # Tool call argument chunks - progressively building the args for StartDriving
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 0,
                        "id": None,
                        "function": {"arguments": '{"ca', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": '{"ca',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": "r_nam", "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": "r_nam",
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": "r_nam",
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": 'e": "B', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'e": "B',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'e": "B',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": 'MW",', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'MW",',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'MW",',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": ' "dri', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ' "dri',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ' "dri',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": "vers_n", "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": "vers_n",
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": "vers_n",
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": 'ame"', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'ame"',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'ame"',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": ': "Ra', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ': "Ra',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ': "Ra',
                    "id": None,
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
                        "index": 0,
                        "id": None,
                        "function": {"arguments": 'ul"}', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'ul"}',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'ul"}',
                    "id": None,
                    "index": 0,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        # Second tool call - LockSeatbelt
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 1,
                        "id": "call_vYvVHzbfwN9numXO9WuUOiZY",
                        "function": {"arguments": "", "name": "LockSeatbelt"},
                        "type": "function",
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            tool_calls=[
                {
                    "name": "LockSeatbelt",
                    "args": {},
                    "id": "call_vYvVHzbfwN9numXO9WuUOiZY",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "LockSeatbelt",
                    "args": "",
                    "id": "call_vYvVHzbfwN9numXO9WuUOiZY",
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        # Tool call argument chunks - progressively building the args for LockSeatbelt
        AIMessageChunk(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "index": 1,
                        "id": None,
                        "function": {"arguments": '{"ca', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": '{"ca',
                    "id": None,
                    "index": 1,
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
                        "id": None,
                        "function": {"arguments": "r_nam", "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": "r_nam",
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": "r_nam",
                    "id": None,
                    "index": 1,
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
                        "id": None,
                        "function": {"arguments": 'e": "B', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'e": "B',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'e": "B',
                    "id": None,
                    "index": 1,
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
                        "id": None,
                        "function": {"arguments": 'MW"}', "name": None},
                        "type": None,
                    }
                ]
            },
            response_metadata={},
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 'MW"}',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 'MW"}',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        # Final chunk with finish reason
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={
                "finish_reason": "tool_calls",
                "model_name": "gpt-4o-2024-08-06",
                "system_fingerprint": "fp_f5bdcc3276",
            },
            id="run-1ab1f38b-72e1-4907-8c73-bf7902c23d63",
        ),
    ]

    # Expected output should match what was provided by the user
    expected_output = [
        'f:{"messageId":"run-1ab1f38b-72e1-4907-8c73-bf7902c23d63"}\n',
        '0:"Why"\n',
        '0:" don\'t"\n',
        '0:" scientists"\n',
        '0:" trust"\n',
        '0:" atoms"\n',
        '0:"?"\n',
        '0:" Because"\n',
        '0:" they"\n',
        '0:" make"\n',
        '0:" up"\n',
        '0:" everything"\n',
        '0:"!\\n\\n"\n',
        '0:"Now"\n',
        '0:","\n',
        '0:" let\'s"\n',
        '0:" get"\n',
        '0:" started"\n',
        '0:" with"\n',
        '0:" the"\n',
        '0:" BMW"\n',
        '0:" and"\n',
        '0:" ensure"\n',
        '0:" the"\n',
        '0:" seat"\n',
        '0:"belt"\n',
        '0:" is"\n',
        '0:" locked"\n',
        '0:"."\n',
        'b:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","toolName":"StartDriving"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":""}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"{\\"ca"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"r_nam"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"e\\": \\"B"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"MW\\","}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":" \\"dri"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"vers_n"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"ame\\""}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":": \\"Ra"}\n',
        'c:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","argsTextDelta":"ul\\"}"}\n',
        '9:{"toolCallId":"call_TCmtOURVFGzvGWiS6MZgAMn5","toolName":"StartDriving","args":{"car_name": "BMW", "drivers_name": "Raul"}}\n',
        'b:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","toolName":"LockSeatbelt"}\n',
        'c:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","argsTextDelta":""}\n',
        'c:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","argsTextDelta":"{\\"ca"}\n',
        'c:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","argsTextDelta":"r_nam"}\n',
        'c:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","argsTextDelta":"e\\": \\"B"}\n',
        'c:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","argsTextDelta":"MW\\"}"}\n',
        '9:{"toolCallId":"call_vYvVHzbfwN9numXO9WuUOiZY","toolName":"LockSeatbelt","args":{"car_name": "BMW"}}\n',
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

    # Verify the output
    assert len(results) == len(
        expected_output
    ), f"Expected {len(expected_output)} chunks, got {len(results)}"

    for i, (actual, expected) in enumerate(zip(results, expected_output)):
        if actual != expected:
            print("Actual:")
            print(actual)
            print("Expected:")
            print(expected)
        assert (
            actual == expected
        ), f"Mismatch at index {i}:\nExpected: {expected}\nActual: {actual}"
