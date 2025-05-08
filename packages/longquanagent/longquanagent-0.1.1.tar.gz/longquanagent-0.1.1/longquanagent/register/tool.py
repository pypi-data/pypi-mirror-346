import sys
import os
import json
import inspect
import importlib
import shutil
import logging
from functools import wraps
from typing import Dict, Any, Optional, Callable, Union
import ast
import uuid
from langchain_together import ChatTogether
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai.chat_models.base import BaseChatOpenAI
from pathlib import Path
from aucodb.database import AucoDB

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
absolute_lib_path = Path(os.path.dirname(os.path.abspath(__file__)))


class ToolManager:
    """Centralized tool management class"""

    def __init__(self, memory: AucoDB, agent_name: str):
        self.memory = memory
        self.agent_name = agent_name
        self.agent = self._load_agent(agent_name)
        self.agent_id = self.agent.id
        self.tools = self.agent.tools
        self._registered_tools = {}

    def _load_agent(self, agent_name: str):
        """Load the agent from the database"""
        agents = self.memory.collections[agent_name].find(f"name=='{agent_name}'")
        if len(agents) == 0:
            raise ValueError(f"Agent {agent_name} not found in memory")
        elif len(agents) == 2:
            raise ValueError(f"Agent {agent_name} duplicate in memory")
        return agents[0]

    def save_tool(self, func: Union[Callable, str], metadata: Dict[str, Any]):
        """Save a tool with its metadata"""
        new_tool = {}
        if isinstance(func, Callable):
            new_tool[func.__name__] = metadata
            self._registered_tools[func.__name__] = func
        else:
            new_tool[func] = metadata
        self.memory.collections[self.agent_name].update(self.agent_id, new_tool)
        self.tools.update(new_tool)
        self.memory.save()

    def register_function(
        self,
        llm: Union[ChatTogether, BaseLanguageModel, BaseChatOpenAI],
        module_path: str,
    ) -> None:
        """Register functions from a module"""
        try:
            if os.path.isfile(module_path):
                # This is a path of module import format
                module_path = Path(module_path)
                absolute_lib_path = Path(os.path.dirname(os.path.abspath(__file__)))
                destination_path = Path(
                    os.path.join(absolute_lib_path.parent, "tools", module_path.name)
                )
                shutil.copy2(module_path, destination_path)
                module_path = (
                    f"longquanagent.tools.{destination_path.name.split('.')[0]}"
                )
            module = importlib.import_module(module_path, package=__package__)
            module_source = inspect.getsource(module)
        except (ImportError, ValueError) as e:
            raise ValueError(f"Failed to load module {module_path}: {str(e)}")

        prompt = (
            "Analyze this module and return a list of tools in JSON format:"
            "- Module code:"
            f"{module_source}"
            "Format: Let's return a list of json format without further explaination and without ```json characters markdown and keep module_path unchange."
            "[{{"
            '"tool_name": "The function",'
            '"arguments": "A dictionary of keyword-arguments to execute tool. Let\'s keep default value if it was set",'
            '"return": "Return value of this tool",'
            '"docstring": "Docstring of this tool",'
            '"dependencies": "List of libraries need to run this tool",'
            f'"module_path": "{module_path}"'
            "}}]"
        )

        response = llm.invoke(prompt)

        try:
            new_tools = ast.literal_eval(response.content.strip())
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Invalid tool format from LLM: {str(e)}")

        for tool in new_tools:
            tool["module_path"] = module_path
            self.tools[tool["tool_name"]] = tool
            self.tools[tool["tool_name"]]["tool_call_id"] = "tool_" + str(uuid.uuid4())
            logging.info(f"Registered {tool['tool_name']}:\n{tool}")

        for tool_name, tool in self.tools.items():
            self.save_tool(tool_name, tool)

        logging.info(f"Completed registration for module {module_path}")

    @classmethod
    def extract_json(cls, text: str) -> Optional[str]:
        """Extract first valid JSON object from text"""
        stack = []
        start = text.find("{")
        if start == -1:
            return None

        for i in range(start, len(text)):
            if text[i] == "{":
                stack.append("{")
            elif text[i] == "}":
                stack.pop()
                if not stack:
                    return text[start : i + 1]
        return None
