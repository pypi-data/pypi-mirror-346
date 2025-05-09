# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=too-many-return-statements,too-many-instance-attributes
"""Export agents."""

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezModel

from ..base import (
    AgentPosition,
    AgentPositions,
    BaseExporter,
    ExporterMixin,
    ExporterReturnType,
    ExportPosition,
    ImportPosition,
)
from .utils import (
    get_agent_code_execution_config,
    get_captain_agent_extras,
    get_group_manager_extras,
    get_is_termination_message,
    get_rag_user_extras,
    get_reasoning_agent_extras,
    get_swarm_extras,
)


class AgentExporter(BaseExporter, ExporterMixin):
    """Agents exporter."""

    def __init__(
        self,
        agent: WaldiezAgent,
        agent_names: Dict[str, str],
        models: Tuple[List[WaldiezModel], Dict[str, str]],
        chats: Tuple[List[WaldiezChat], Dict[str, str]],
        skill_names: Dict[str, str],
        is_async: bool,
        group_chat_members: List[WaldiezAgent],
        for_notebook: bool,
        arguments_resolver: Callable[[WaldiezAgent], List[str]],
        output_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        """Initialize the agents exporter.

        Parameters
        ----------
        agent : WaldiezAgent
            The agent to export.
        agent_names : Dict[str, str]
            The agent ids to names mapping.
        models : Tuple[List[WaldiezModel], Dict[str, str]]
            All the models and the model ids to names mapping.
        chats : Tuple[List[WaldiezChat], Dict[str, str]]
            All the chats and the chat ids to names mapping.
        skill_names : Dict[str, str]
            The skill ids to names mapping.
        is_async : bool
            Whether the whole flow is async.
        for_notebook : bool
            Whether the exporter is for a notebook.
        output_dir : Optional[Union[str, Path]], optional
            The output directory, by default None
        """
        self.for_notebook = for_notebook
        self.agent = agent
        self.agent_names = agent_names
        if output_dir is not None and not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
        self.output_dir = output_dir
        self.models = models[0]
        self.model_names = models[1]
        self.skill_names = skill_names
        self.arguments_resolver = arguments_resolver
        self.group_chat_members = group_chat_members
        self.chats = chats
        self.is_async = is_async
        self._agent_name = agent_names[agent.id]
        # content, argument, import
        self._code_execution = get_agent_code_execution_config(
            agent=self.agent,
            agent_name=self._agent_name,
            skill_names=self.skill_names,
        )
        # before_rag, retrieve_arg, rag_imports
        self._rag = get_rag_user_extras(
            agent=self.agent,
            agent_name=self._agent_name,
            model_names=self.model_names,
            path_resolver=self.path_resolver,
            serializer=self.serializer,
        )
        # before_manager, group_chat_arg
        self._group_chat = get_group_manager_extras(
            agent=self.agent,
            agent_names=self.agent_names,
            group_chat_members=self.group_chat_members,
            serializer=self.serializer,
        )
        # before_agent, extra args, handoff_registrations
        self._swarm = get_swarm_extras(
            agent=self.agent,
            agent_names=self.agent_names,
            skill_names=self.skill_names,
            chats=self.chats,
            is_async=self.is_async,
            serializer=self.serializer,
            string_escape=self.string_escape,
        )
        # before_agent, termination_arg
        self._termination = get_is_termination_message(
            agent=self.agent, agent_name=self._agent_name
        )
        self._reasoning = get_reasoning_agent_extras(
            agent=self.agent,
            serializer=self.serializer,
        )
        self._captain = get_captain_agent_extras(
            agent=self.agent,
            agent_names=self.agent_names,
            all_models=self.models,
            serializer=self.serializer,
            output_dir=self.output_dir,
        )

    def get_imports(self) -> Optional[List[Tuple[str, ImportPosition]]]:
        """Get the imports.

        Returns
        -------
        Optional[Tuple[str, ImportPosition]]
            The imports.
        """
        position = ImportPosition.THIRD_PARTY
        # default imports based on the agent class.
        agent_imports = self.agent.ag2_imports
        # if code execution is enabled, update the imports.
        if self._code_execution[2]:
            agent_imports.add(self._code_execution[2])
        # if RAG is enabled, update the imports.
        if self._rag[2]:
            agent_imports.update(self._rag[2])
        # if the agent has skills, add the register_function import.
        if self.agent.data.skills:
            agent_imports.add("from autogen import register_function")
        return sorted(
            [(import_string, position) for import_string in agent_imports],
            key=lambda x: x[0],
        )

    def get_system_message_arg(self) -> str:
        """Get the system message argument.

        Returns
        -------
        str
            The system message argument.
        """
        if not self.agent.data.system_message:
            return ""
        system_message = self.string_escape(self.agent.data.system_message)
        return ",\n    system_message=" + f'"{system_message}"'

    def get_before_export(
        self,
    ) -> Optional[List[Tuple[str, Union[ExportPosition, AgentPosition]]]]:
        """Generate the content before the main export.

        Returns
        -------
        Optional[List[Tuple[str, Union[ExportPosition, AgentPosition]]]]
            The exported content before the main export and its position.
        """
        before_agent_string = ""
        if self._code_execution[0] and self._code_execution[2]:
            before_agent_string += self._code_execution[0]
        if self._termination[1]:
            before_agent_string += self._termination[1]
        if self._group_chat[0]:
            before_agent_string += self._group_chat[0]
        if self._rag[0]:
            before_agent_string += self._rag[0]
        if self._swarm[0]:
            before_agent_string += self._swarm[0]
        if before_agent_string:
            return [
                (
                    before_agent_string,
                    AgentPosition(self.agent, AgentPositions.BEFORE),
                )
            ]
        return None

    def get_after_export(
        self,
    ) -> Optional[List[Tuple[str, Union[ExportPosition, AgentPosition]]]]:
        """Generate the content after the main export.

        Returns
        -------
        Optional[List[Tuple[str, Union[ExportPosition, AgentPosition]]]]
            The exported content after the main export and its position.
        """
        after_agent_string = ""
        if self._swarm[2]:
            after_agent_string += self._swarm[2]
        if after_agent_string:
            return [
                (
                    after_agent_string,
                    AgentPosition(self.agent, AgentPositions.AFTER_ALL),
                )
            ]
        return None

    def generate(self) -> Optional[str]:
        """Generate the exported agent.

        Returns
        -------
        Optional[str]
            The exported agent.
        """
        agent = self.agent
        agent_name = self._agent_name
        retrieve_arg = self._rag[1]
        group_chat_arg = self._group_chat[1]
        is_termination = self._termination[0]
        code_execution_arg = self._code_execution[1]
        system_message_arg = self.get_system_message_arg()
        default_auto_reply: str = "None"
        if agent.data.agent_default_auto_reply:
            default_auto_reply = (
                f'"{self.string_escape(agent.data.agent_default_auto_reply)}"'
            )
        extras = (
            f"{group_chat_arg}{retrieve_arg}{self._reasoning}{self._captain}"
        )
        ag2_class = self.agent.ag2_class
        if agent.agent_type == "swarm":
            # SwarmAgent is deprecated.
            ag2_class = "ConversableAgent"
        agent_str = f"""{agent_name} = {ag2_class}(
    name="{agent_name}",
    description="{agent.description}"{system_message_arg},
    human_input_mode="{agent.data.human_input_mode}",
    max_consecutive_auto_reply={agent.data.max_consecutive_auto_reply},
    default_auto_reply={default_auto_reply},
    code_execution_config={code_execution_arg},
    is_termination_msg={is_termination},{extras}
"""
        if self._swarm[1]:
            agent_str += self._swarm[1]
        # e.g. llm_config=...
        other_args = self.arguments_resolver(agent)
        if other_args:
            agent_str += ",\n".join(other_args)
        if not agent_str.endswith("\n"):
            agent_str += "\n"
        agent_str += ")"
        return agent_str

    def export(self) -> ExporterReturnType:
        """Export the agent.

        Returns
        -------
        ExporterReturnType
            The exported agent.
        """
        agent_string = self.generate() or ""
        is_group_manager = self.agent.agent_type == "group_manager"
        after_export = self.get_after_export() or []
        content: Optional[str] = agent_string
        if is_group_manager and agent_string:
            content = None
            # make sure the group manager is defined
            # after the rest of the agents.
            # to avoid issues with (for example):
            #  'group_manager_group_chat = GroupChat(
            #    # assistant and rag_user should be defined first
            # '    agents=[assistant, rag_user],
            # '    enable_clear_history=True,
            # ...
            after_export.append(
                (agent_string, AgentPosition(None, AgentPositions.AFTER_ALL, 0))
            )
        return {
            "content": content,
            "imports": self.get_imports(),
            "environment_variables": [],
            "before_export": self.get_before_export(),
            "after_export": after_export,
        }
