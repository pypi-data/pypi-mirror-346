import os
import json
import importlib
from abc import ABC, abstractmethod
from typing import Any, Awaitable, List, Optional, Callable
from functools import wraps
from langchain_together import ChatTogether
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.messages.tool import ToolMessage
import logging
from pathlib import Path
import inspect
from typing import Union
from longquanagent.register.tool import ToolManager
from aucodb.database import AucoDB, Collection, Record
import uuid
import asyncio
from functools import lru_cache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentMeta(ABC):
    """Abstract base class for agents"""

    @abstractmethod
    def __init__(
        self,
        llm: Union[ChatTogether, BaseLanguageModel, BaseChatOpenAI],
        tools: List = [],
        *args,
        **kwargs,
    ):
        """Initialize a new Agent with LLM and tools"""
        pass

    @abstractmethod
    def invoke(self, query: str, *args, **kwargs) -> Any:
        """Synchronously invoke the agent's main function"""
        pass

    @abstractmethod
    async def invoke_async(self, query: str, *args, **kwargs) -> Awaitable[Any]:
        """Asynchronously invoke the agent's main function"""
        pass


class Agent(AgentMeta):
    """Concrete implementation of an AI agent with tool-calling capabilities"""

    absolute_lib_path = Path(os.path.dirname(os.path.abspath(__file__)))
    TOOLS_PATH = Path(
        os.path.join(absolute_lib_path.parent, "tool_template", "tools.json")
    )

    _memory_instance = None
    _memory_lock = asyncio.Lock()
    _tools_cache = None

    def __init__(
        self,
        agent_name: str,
        llm: Union[ChatTogether, BaseLanguageModel, BaseChatOpenAI],
        tools: List = [],
        description: str = "You are a helpful assistant who can use the following tools to complete a task.",
        skills: list[str] = ["You can answer the user question with tools"],
        agent_template: Union[Path, str] = TOOLS_PATH,
        *args,
        **kwargs,
    ):
        """
        Initialize the agent with a language model, a list of tools, a description, and a set of skills.
        Parameters:
        ----------
        agent_name: str
            The name of agent, it must be unique.
        llm : Union[ChatTogether, BaseLanguageModel, BaseChatOpenAI]
            An instance of a language model used by the agent to process and generate responses.
        tools : List, optional
            A list of tools that the agent can utilize when performing tasks. Defaults to an empty list.
        description : str, optional
            A brief description of the assistant's capabilities. Defaults to a general helpful assistant message.
        skills : list[str], optional
            A list of skills or abilities describing what the assistant can do. Defaults to a basic tool-usage skill.
        agent_template : Path, optional
            The path to the agent template file. Defaults to the default template file.
        *args, **kwargs : Any
            Additional arguments passed to the superclass or future extensions.
        """
        self.agent_name = agent_name
        self.llm = llm
        self.tools = tools
        self.description = description
        self.skills = skills
        self.agent_template = agent_template
        # Add collection of agents
        if Agent._memory_instance is None:
            Agent._memory_instance = AucoDB(
                data_name="long_quan_agents",
                data_path=self.agent_template,
                is_overwrite=False,
            )
        self.memory = Agent._memory_instance
        agent_collection = Collection(name=self.agent_name)
        self.memory.add_collection(collection=agent_collection)
        # Add agent record with their agent_name
        self.agent_record = Record(name=self.agent_name, tools={})
        self.memory.collections[self.agent_name].add(record=self.agent_record)
        self.memory.save()
        self.tool_manager = ToolManager(memory=self.memory, agent_name=self.agent_name)
        if tools:
            self.register_tools(self.tools)

    def register_tools(self, tools: List[str]) -> Any:
        """
        Register a list of tools
        Args:
            - tools (List[str]): A list of tool names to register. It can be module paths or file paths.
        Returns:
            - None
        """
        for tool in tools:
            self.tool_manager.register_function(self.llm, tool)

    def invoke(self, query: str, *args, **kwargs) -> Any:
        """
        Select and execute a tool based on the task description
        """
        prompt = (
            "You are given a task and a list of available tools.\n"
            f"- Task: {query}\n"
            f"- Tools list: {json.dumps(self.tool_manager.tools)}\n\n"
            "Instructions:\n"
            "- If the task can be solved without tools, just return the answer without any explanation\n"
            "- If the task requires a tool, select the appropriate tool with its relevant arguments from Tools list according to following format (no explanations, no markdown):\n"
            "{\n"
            '"tool_name": "Function name",\n'
            '"arguments": "A dictionary of keyword-arguments to execute tool_name",\n'
            '"module_path": "Path to import the tool"\n'
            "}\n"
            "Let's say I don't know and suggest where to search if you are unsure the answer.\n"
            "Not make up anything.\n"
        )
        skills = "- ".join([skill + "\n" for skill in self.skills])
        messages = [
            SystemMessage(content=f"{self.description}\nHere is your skills: {skills}"),
            HumanMessage(content=prompt),
        ]

        try:
            response = self.llm.invoke(messages)
            tool_data = self._extract_json(response.content)

            if not tool_data or ("None" in tool_data) or (tool_data == "{}"):
                return response

            tool_call = json.loads(tool_data)
            return self._execute_tool(
                tool_call["tool_name"], tool_call["arguments"], tool_call["module_path"]
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Tool calling failed: {str(e)}")
            return None

    async def invoke_async(self, *args, **kwargs) -> Awaitable[Any]:
        """Asynchronously invoke the agent's LLM"""
        return await self.llm.ainvoke(*args, **kwargs)

    def _execute_tool(self, tool_name: str, arguments: dict, module_path: str) -> Any:
        """Execute the specified tool with given arguments"""
        # If function is directly registered by decorator @function_tool. Access it on runtime context.

        if module_path == "__runtime__" and tool_name in self.tool_manager.tools:
            # Execute the __runtime__ function, which registered by @function_tool decorator
            func = self.tool_manager._registered_tools[tool_name]
            artifact = func(**arguments)
            content = f"Completed executing tool {tool_name}({arguments})"
            logger.info(content)
            tool_call_id = self.tool_manager.tools[tool_name]["tool_call_id"]
            message = ToolMessage(
                content=content, artifact=artifact, tool_call_id=tool_call_id
            )
            return message

        # Execute the normal tools
        try:
            if tool_name in globals():
                return globals()[tool_name](**arguments)

            module = importlib.import_module(module_path, package=__package__)
            func = getattr(module, tool_name)
            artifact = func(**arguments)
            content = f"Completed executing tool {tool_name}({arguments})"
            logger.info(content)
            tool_call_id = self.tool_manager.tools[tool_name]["tool_call_id"]
            message = ToolMessage(
                content=content, artifact=artifact, tool_call_id=tool_call_id
            )
            return message
        except (ImportError, AttributeError) as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return None

    @staticmethod
    def _extract_json(text: str) -> Optional[str]:
        """Extract first valid JSON object from text using stack-based parsing"""
        start = text.find("{")
        if start == -1:
            return None

        stack = []
        for i in range(start, len(text)):
            if text[i] == "{":
                stack.append("{")
            elif text[i] == "}":
                stack.pop()
                if not stack:
                    return text[start : i + 1]
        return None

    def function_tool(self, func: Callable):
        """Decorator to register a function as a tool
        Args:
            func (Callable): Function to register as a tool on runtime
        # Example usage:
        tool_manager = ToolManager(memory=AucoDB(), agent_name="my_agent")
        @tool_manager.function_tool
        def sample_function(x: int, y: str) -> str:
            '''Sample function for testing'''
            return f"{y}: {x}"
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Get function metadata
        signature = inspect.signature(func)

        # Try to get module path, fall back to None if not available
        module_path = "__runtime__"

        # Create metadata
        if module_path == "__runtime__":
            metadata = {
                "tool_name": func.__name__,
                "arguments": {
                    name: (
                        str(param.annotation)
                        if param.annotation != inspect.Parameter.empty
                        else "Any"
                    )
                    for name, param in signature.parameters.items()
                },
                "return": (
                    str(signature.return_annotation)
                    if signature.return_annotation != inspect.Signature.empty
                    else "Any"
                ),
                "docstring": (func.__doc__ or "").strip(),
                "module_path": module_path,
                "tool_call_id": "tool_" + str(uuid.uuid4()),
                "is_runtime": module_path == "__runtime__",
            }

            # Register both the function and its metadata
            self.tool_manager.save_tool(func, metadata)
            logging.info(
                f"Registered tool: {func.__name__} "
                f"({'runtime' if module_path == '__runtime__' else 'file-based'})"
            )
        return wrapper
