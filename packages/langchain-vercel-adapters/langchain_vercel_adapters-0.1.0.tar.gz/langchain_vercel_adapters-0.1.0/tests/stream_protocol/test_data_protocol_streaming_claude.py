import pytest
from langchain_core.messages import AIMessageChunk

from langchain_vercel_adapters.stream_protocol.data_stream import (
    serialize_to_data_stream_protocol,
)


pytestmark = pytest.mark.asyncio


async def test_serialize_to_data_stream_protocol_with_content_list():
    # Create mock chunks based on the input
    chunks = [
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            usage_metadata={
                "input_tokens": 479,
                "output_tokens": 1,
                "total_tokens": 480,
                "input_token_details": {"cache_creation": 0, "cache_read": 0},
            },
        ),
        AIMessageChunk(
            content=[{"text": "Here", "type": "text", "index": 0}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[
                {
                    "text": "'s a short joke: Why don't scientists trust",
                    "type": "text",
                    "index": 0,
                }
            ],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[
                {
                    "text": " atoms? Because they make up everything!",
                    "type": "text",
                    "index": 0,
                }
            ],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[{"text": " \n\nNow, I'll help", "type": "text", "index": 0}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[
                {
                    "text": " you start driving and make sure to",
                    "type": "text",
                    "index": 0,
                }
            ],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[{"text": " lock the seatbelt:", "type": "text", "index": 0}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
        ),
        AIMessageChunk(
            content=[
                {
                    "id": "toolu_01D8yE8c3ueoggg1hV56Ysyu",
                    "input": {},
                    "name": "StartDriving",
                    "type": "tool_use",
                    "index": 1,
                }
            ],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[
                {
                    "name": "StartDriving",
                    "args": {},
                    "id": "toolu_01D8yE8c3ueoggg1hV56Ysyu",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "StartDriving",
                    "args": "",
                    "id": "toolu_01D8yE8c3ueoggg1hV56Ysyu",
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": "", "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": "",
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": '{"car_name":', "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": '{"car_name":',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": ' "bmw"', "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ' "bmw"',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ' "bmw"',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": ', "driver', "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ', "driver',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ', "driver',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": 's_name"', "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": 's_name"',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": 's_name"',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": ': "John"}', "type": "tool_use", "index": 1}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ': "John"}',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ': "John"}',
                    "id": None,
                    "index": 1,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[
                {
                    "id": "toolu_01UuVvQSuChUrntM5BqjovsD",
                    "input": {},
                    "name": "LockSeatbelt",
                    "type": "tool_use",
                    "index": 2,
                }
            ],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[
                {
                    "name": "LockSeatbelt",
                    "args": {},
                    "id": "toolu_01UuVvQSuChUrntM5BqjovsD",
                    "type": "tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": "LockSeatbelt",
                    "args": "",
                    "id": "toolu_01UuVvQSuChUrntM5BqjovsD",
                    "index": 2,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": "", "type": "tool_use", "index": 2}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": "",
                    "id": None,
                    "index": 2,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": '{"car_name":', "type": "tool_use", "index": 2}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            tool_calls=[{"name": "", "args": {}, "id": None, "type": "tool_call"}],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": '{"car_name":',
                    "id": None,
                    "index": 2,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": ' "bmw', "type": "tool_use", "index": 2}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": ' "bmw',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": ' "bmw',
                    "id": None,
                    "index": 2,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content=[{"partial_json": '"}', "type": "tool_use", "index": 2}],
            additional_kwargs={},
            response_metadata={},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            invalid_tool_calls=[
                {
                    "name": None,
                    "args": '"}',
                    "id": None,
                    "error": None,
                    "type": "invalid_tool_call",
                }
            ],
            tool_call_chunks=[
                {
                    "name": None,
                    "args": '"}',
                    "id": None,
                    "index": 2,
                    "type": "tool_call_chunk",
                }
            ],
        ),
        AIMessageChunk(
            content="",
            additional_kwargs={},
            response_metadata={"stop_reason": "tool_use", "stop_sequence": None},
            id="run-70530d41-5d23-43aa-901f-b0cd2cd63d9d",
            usage_metadata={
                "input_tokens": 0,
                "output_tokens": 159,
                "total_tokens": 159,
                "input_token_details": {},
            },
        ),
    ]

    # Expected output based on the user's specification
    expected_output = [
        'f:{"messageId":"run-70530d41-5d23-43aa-901f-b0cd2cd63d9d"}\n',
        '0:"Here"\n',
        "0:\"'s a short joke: Why don't scientists trust\"\n",
        '0:" atoms? Because they make up everything!"\n',
        '0:" \\n\\nNow, I\'ll help"\n',
        '0:" you start driving and make sure to"\n',
        '0:" lock the seatbelt:"\n',
        'b:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","toolName":"StartDriving"}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":""}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":""}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":"{\\"car_name\\":"}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":" \\"bmw\\""}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":", \\"driver"}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":"s_name\\""}\n',
        'c:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","argsTextDelta":": \\"John\\"}"}\n',
        '9:{"toolCallId":"toolu_01D8yE8c3ueoggg1hV56Ysyu","toolName":"StartDriving","args":{"car_name": "bmw", "drivers_name": "John"}}\n',
        'b:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","toolName":"LockSeatbelt"}\n',
        'c:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","argsTextDelta":""}\n',
        'c:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","argsTextDelta":""}\n',
        'c:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","argsTextDelta":"{\\"car_name\\":"}\n',
        'c:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","argsTextDelta":" \\"bmw"}\n',
        'c:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","argsTextDelta":"\\"}"}\n',
        '9:{"toolCallId":"toolu_01UuVvQSuChUrntM5BqjovsD","toolName":"LockSeatbelt","args":{"car_name": "bmw"}}\n',
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
    # assert len(results) == len(expected_output), f"Expected {len(expected_output)} chunks, got {len(results)}"

    for i, (actual, expected) in enumerate(zip(results, expected_output)):
        if actual != expected:
            print("Actual:")
            print(actual)
            print("Expected:")
            print(expected)
        assert (
            actual == expected
        ), f"Mismatch at index {i}:\nExpected: {expected}\nActual: {actual}"
