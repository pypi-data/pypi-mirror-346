from typing import Any, Literal
from types import FunctionType
from supereasyai.messages import AssistantMessage, AssistantMessageStream, Message, ToolMessage
from abc import ABC, abstractmethod
from doms_json import generate_json_schema
import inspect


class NoModel(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AIBase(ABC):
    @abstractmethod
    def query(self,
              messages: list[Message],
              model: str | None = None,
              temperature: float | None = None,
              tools: list[dict | FunctionType] | None = None,
              tool_choice: Literal["none", "auto", "required"] | None = None,
              force_tool: str | None = None,
              stream: bool = False) -> AssistantMessage | AssistantMessageStream:
        raise NotImplementedError()
    
    @abstractmethod
    def query_format(self,
              messages: list[Message],
              format: type,
              model: str | None = None,
              temperature: float | None = None) -> Any:
        raise NotImplementedError()


class AI:
    def __init__(self, base: AIBase, model: str | None = None) -> None:
        self.__base__: AIBase = base
        self.model: str | None = model
    
    def query(self,
              messages: list[Message],
              model: str | None = None,
              temperature: float | None = None,
              tools: list[dict | FunctionType] | None = None,
              tool_choice: Literal["none", "auto", "required"] | None = None,
              force_tool: str | None = None,
              stream: bool = False) -> AssistantMessage | AssistantMessageStream:
        if model == None and self.model == None:
            raise NoModel("No model given. Either pass a model through the query function or set a model when creating the AI object.")
        return self.__base__.query(
            messages=messages,
            model=model if model else self.model,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice,
            force_tool=force_tool,
            stream=stream
        )
    
    def query_format(self,
              messages: list[Message],
              format: type,
              model: str | None = None,
              temperature: float | None = None) -> Any:
        if model == None and self.model == None:
            raise NoModel("No model given. Either pass a model through the query function or set a model when creating the AI object.")
        return self.__base__.query_format(
            messages=messages,
            format=format,
            model=model if model else self.model,
            temperature=temperature
        )
    
    def query_and_run_tools(self,
              messages: list[Message],
              model: str | None = None,
              temperature: float | None = None,
              tools: list[FunctionType] | None = None,
              tool_choice: Literal["none", "auto", "required"] | None = None,
              force_tool: str | None = None,
              autonomy: Literal["none", "follow_up", "full"] = False) -> list[AssistantMessage | ToolMessage]:
        return_messages: list[AssistantMessage | ToolMessage] = []
        while True:
            response: AssistantMessage = self.query(model=model, messages=messages + return_messages, temperature=temperature, tools=tools, tool_choice=tool_choice, force_tool=force_tool, stream=False)
            return_messages.append(response)
            if response.tool_calls:
                return_messages += response.run_tool_calls(tools)
            if autonomy == "follow_up":
                return_messages.append(self.query(model=model, messages=messages + return_messages, temperature=temperature, stream=False))
            if autonomy != "full" or response.tool_calls == None:
                break
        return return_messages



def function_to_tool(function: FunctionType) -> dict:
    tool: dict = {
        "type": "function",
        "function": {
            "name": function.__name__,
            "parameters": generate_json_schema(function),
            "strict": True
        }
    }
    doc: str | None = inspect.getdoc(function)
    if doc:
        tool["function"]["description"] = doc.split("\n")[0]
    return tool