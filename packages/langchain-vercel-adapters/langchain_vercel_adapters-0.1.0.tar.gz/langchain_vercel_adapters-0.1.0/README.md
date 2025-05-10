# LangChain Vercel Adapters

This library provides a lightweight wrapper to integrate langchain-based messages into a [Vercel's Chat SDK](https://vercel.com/blog/introducing-chat-sdk).


## Features

- Convert LLM streaming output into vercel's [data stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol#data-stream-protocol)

## Installation

```bash
pip install langchain-vercel-adapters
```

## Quickstart

Here is a simple example of a fastapi server:

```bash
pip install langchain-vercel-adapters langchain langchain_anthropic 
```

Server example:

```python
import os
from typing import AsyncGenerator, cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

from langchain_core.messages import AIMessageChunk
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain_vercel_adapters import (
    serialize_to_data_stream_protocol,
    VercelTypes as V
)


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

app = FastAPI()

llm = ChatAnthropic(
    model_name="claude-3-sonnet-20240229",
    api_key=ANTHROPIC_API_KEY,
)

async def stream_joke(topic: str) -> AsyncGenerator[AIMessageChunk, None]:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a joke teller. You are given a topic and you need to tell a joke about it."),
            ("user", "tell me a joke about {topic}"),
        ]
    )
    chain = prompt | llm

    async for event in chain.astream({"topic": topic}):
        event = cast(AIMessageChunk, event)
        yield event
    

@app.post("/api/chat/{topic}")
async def handle_chat_data(request: V.ChatMessages, topic: str):
    messages = request.messages
    stream = stream_joke(topic)
    stream = serialize_to_data_stream_protocol(stream)
    response = StreamingResponse(stream, media_type="text/event-stream")
    response.headers['x-vercel-ai-data-stream'] = 'v1'
    return response
```
