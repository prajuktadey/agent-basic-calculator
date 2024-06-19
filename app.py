import json
from typing import Sequence, List

from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
import nest_asyncio
import chainlit as cl

nest_asyncio.apply()
llm = Ollama(model="mistral:latest", request_timeout=120.0)
Settings.llm = llm

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract two integers and returns the result integer"""
    return a - b


def divide(a: int, b: int) -> int:
    """Divides two integers and returns the result integer"""
    return a / b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
subtract_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)

#create an agent 
agent = ReActAgent.from_tools(
    [multiply_tool, add_tool, subtract_tool, divide_tool],
    llm=llm,
    verbose=True,
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hello there, I am an AI Agent. How cam I help you?").send()
    cl.user_session.set("agent", agent)
    
@cl.on_message
async def on_message(message:cl.Message):
    agent = cl.user_session.get("agent")

    response = agent.chat(message.content)
    await cl.Message(content=str(response)).send()  