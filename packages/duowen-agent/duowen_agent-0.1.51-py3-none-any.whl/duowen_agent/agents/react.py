import logging
import time
from typing import TypedDict, Union, Optional, List

from duowen_agent.llm import OpenAIChat
from duowen_agent.tools.base import Tool
from duowen_agent.tools.manager import ToolManager
from duowen_agent.tools.mcp_client import McpClient
from duowen_agent.utils.string_template import StringTemplate
from .base import BaseAgent
from ..utils.core_utils import remove_think, parse_json_markdown

REACT_SYSTEM_PROMPT_TEMPLATE = StringTemplate(
    template_format="jinja2",
    template="""
As a diligent Task Agent, you goal is to effectively accomplish the provided task or question as best as you can.

## Tools
You have access to the following tools, the tools information is provided by the following schema:
{{tool_descriptions}}

## Output Format
To answer the question, Use the following JSON format. JSON only, no explanation. Otherwise, you will be punished.
The output should be formatted as a JSON instance that conforms to the format below. JSON only, no explanation.

```json
{
"analysis": "The thought of what to do and why.",
"action": # the action to take, must be one of provided tools
    {
    "name": "tool name",
    "args": "tool input parameters, json type data"
    }
}
```

If this format is used, the user will respond in the following format:

```
Observation: tool response
```

You should keep repeating the above format until you have enough information
to answer the question without using any more tools. At that point, you MUST respond
in the one of the following two formats:

- If you can answer the question:

```json
{
"analysis": "The thought of what to do and why.",
"action": {
    "name": "finish",
    "args": {"content": "You answer here."}
    }
}
```

- If you cannot answer the question in the current context:

```json
{
"analysis": "The thought of what to do and why.",
"action": {
    "name": "finish",
    "args": {"content": "Sorry, I cannot answer your query, because (Summary all the upper steps, and explain)"}
    }
}
```

## Attention
- Your output is JSON only and no explanation.
- Choose only ONE tool and you can't do without using any tools in one step.
- Your final answer output language should be consistent with the language used by the user. Middle step output is English.
- Whether the action input is JSON or str depends on the definition of the tool.

## User question
{{question}}

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant history.

""",  # noqa: E501
)
PREFIX_TEMPLATE = """You are a {agent_identity}, named {agent_name}, your goal is {agent_goal}, and the constraint is {agent_constraints}. """  # noqa


class ActionResponse(TypedDict):
    analysis: str
    action_name: str
    action_parameters: Union[dict, str]


class ReactAgent(BaseAgent):

    def __init__(
        self,
        *,
        llm: OpenAIChat,
        tools: List[Tool] = None,
        mcp_client: Optional[McpClient] = None,
        prefix_prompt_template: StringTemplate = StringTemplate(PREFIX_TEMPLATE),
        filter_function_list: List[str] = None,
        enable_role: bool = False,
        agent_name: str = "tool-agent",
        agent_identity: str = "tool-agent",
        agent_goal: str = "provides better assistance and services for humans.",
        agent_constraints: str = "none",
        max_iterations: Optional[int] = 15,
        _from: Optional[str] = None,
        **kwargs,
    ):
        super().__init__()
        self.tool_manager = ToolManager(tools, filter_function_list) if tools else None
        self.mcp_client = mcp_client
        self.llm = llm
        self.system_prompt_template: StringTemplate = REACT_SYSTEM_PROMPT_TEMPLATE
        self.prefix_prompt_template: StringTemplate = prefix_prompt_template
        self.conversation_prompt: str = ""
        self.filter_function_list = filter_function_list
        self.max_iterations = max_iterations
        self.max_execution_time: Optional[float] = None

        self.enable_role: bool = enable_role
        self.agent_name: str = agent_name
        self.agent_identity: str = agent_identity
        self.agent_goal: str = agent_goal
        self.agent_constraints: str = agent_constraints

    def get_llm(self) -> OpenAIChat:
        return self.llm

    def _build_system_prompt(self, instruction: str) -> str:
        prefix_prompt = (
            self.prefix_prompt_template.format(
                agent_identity=self.agent_identity,
                agent_name=self.agent_name,
                agent_goal=self.agent_goal,
                agent_constraints=self.agent_constraints,
            )
            if self.enable_role
            else ""
        )

        _func_tool_descriptions = (
            self.tool_manager.tool_descriptions if self.tool_manager else "\n"
        )

        _mpc_tool_descriptions = (
            self.mcp_client.tool_descriptions if self.mcp_client else "\n"
        )

        return prefix_prompt + self.system_prompt_template.format(
            question=instruction,
            tool_descriptions=_func_tool_descriptions + _mpc_tool_descriptions,
        )

    @property
    def current_date(self) -> str:
        return f"Current date: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def _run(
        self, instruction: str, return_raw_data: bool = False, **kwargs
    ) -> Union[str, ActionResponse]:
        self.conversation_prompt = self._build_system_prompt(instruction)
        logging.info(f"[agent] ToolAgent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            llm_resp: str = ""

            for i in self.llm.chat_for_stream(
                messages=self.conversation_prompt + self.current_date
            ):
                yield {"think": i}
                llm_resp += i

            while llm_resp == "":
                llm_resp: str = ""

                for i in self.llm.chat(
                    messages=self.conversation_prompt + self.current_date
                ):
                    yield {"think": i}
                    llm_resp += i

            llm_resp = remove_think(llm_resp)

            action_resp: ActionResponse = self._parse_llm_response(llm_resp)

            yield {
                "action": {
                    "analysis": action_resp["analysis"],
                    "action_name": action_resp["action_name"],
                    "action_parameters": action_resp["action_parameters"],
                }
            }

            self.conversation_prompt += f"\nAction:{llm_resp}\n"
            logging.info(
                f"[dw] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "finish" in action_resp["action_name"]:
                if return_raw_data:
                    yield {"result": action_resp}

                yield {"result": action_resp["action_parameters"]["content"]}
                return

            tool_result, tool_result_meta = self.run_tool(
                action_resp["action_name"], action_resp["action_parameters"]
            )
            self.conversation_prompt += f"Observation: {tool_result}\n"
            yield {
                "observation": {
                    "result": tool_result,
                    "view": tool_result_meta,
                    "analysis": action_resp["analysis"],
                    "action_name": action_resp["action_name"],
                    "action_parameters": action_resp["action_parameters"],
                }
            }
            iterations += 1
            used_time += time.time() - start_time

    def run_tool(self, tool_name: str, parameters: Union[str, dict]):

        if self.tool_manager and self.tool_manager.get_tool(tool_name):
            return self.tool_manager.run_tool(tool_name, parameters)
        elif self.mcp_client.get_tool_info(tool_name):
            return self.mcp_client.run_tool(tool_name, parameters), None
        else:
            return f"未知的工具调用{tool_name}", None

    def _should_continue(self, current_iteration: int, current_time_elapsed) -> bool:
        if self.max_iterations and current_iteration >= self.max_iterations:
            return False
        if self.max_execution_time and current_time_elapsed >= self.max_execution_time:
            return False
        return True

    def _parse_llm_response(self, llm_resp: str) -> ActionResponse:

        data: dict = parse_json_markdown(llm_resp)

        return ActionResponse(
            analysis=data["analysis"],
            action_name=data["action"]["name"],
            action_parameters=data["action"]["args"],
        )
