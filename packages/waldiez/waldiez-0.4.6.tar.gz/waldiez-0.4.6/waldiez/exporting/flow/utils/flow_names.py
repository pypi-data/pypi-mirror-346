# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Ensure unique names for agents, models, skills, and chats."""

from typing import Callable, Dict, List, TypedDict

from waldiez.models import (
    Waldiez,
    WaldiezAgent,
    WaldiezChat,
    WaldiezModel,
    WaldiezSkill,
)


class ResultType(TypedDict):
    """The result type for ensure_unique_names."""

    agent_names: Dict[str, str]
    model_names: Dict[str, str]
    skill_names: Dict[str, str]
    chat_names: Dict[str, str]
    agents: List[WaldiezAgent]
    models: List[WaldiezModel]
    skills: List[WaldiezSkill]
    chats: List[WaldiezChat]
    flow_name: str


# pylint: disable=too-many-locals
def ensure_unique_names(
    waldiez: Waldiez,
    get_valid_instance_name: Callable[..., Dict[str, str]],
    max_length: int = 46,
    flow_name_max_length: int = 20,
) -> ResultType:
    """Ensure unique names for agents, models, skills, and chats and flow.

    Parameters
    ----------
    waldiez : Waldiez
        The Waldiez instance.
    get_valid_instance_name : Callable[..., Dict[str, str]]
        The function to get a valid instance name.
    max_length : int, optional
        The maximum length of the name, by default 64
    flow_name_max_length : int, optional
        The maximum length of the flow name, by default 20

    Returns
    -------
    ResultType
        The result with unique names for agents, models, skills, chats, flow.
    """
    all_names: Dict[str, str] = {}
    agent_names: Dict[str, str] = {}
    model_names: Dict[str, str] = {}
    skill_names: Dict[str, str] = {}
    chat_names: Dict[str, str] = {}
    agents: List[WaldiezAgent] = []
    models: List[WaldiezModel] = []
    skills: List[WaldiezSkill] = []
    chats: List[WaldiezChat] = []

    for agent in waldiez.agents:
        all_names = get_valid_instance_name(
            (agent.id, agent.name),
            all_names,
            prefix="wa",
            max_length=max_length,
        )
        agent_names[agent.id] = all_names[agent.id]
        agents.append(agent)
    for model in waldiez.models:
        all_names = get_valid_instance_name(
            (model.id, model.name),
            all_names,
            prefix="wm",
            max_length=max_length,
        )
        model_names[model.id] = all_names[model.id]
        models.append(model)
    for skill in waldiez.skills:
        all_names = get_valid_instance_name(
            (skill.id, skill.name),
            all_names,
            prefix="ws",
            max_length=max_length,
        )
        skill_names[skill.id] = all_names[skill.id]
        skills.append(skill)
    for chat in waldiez.flow.data.chats:
        all_names = get_valid_instance_name(
            (chat.id, chat.name), all_names, prefix="wc", max_length=max_length
        )
        chat_names[chat.id] = all_names[chat.id]
        chats.append(chat)
    all_names = get_valid_instance_name(
        (waldiez.flow.id, waldiez.flow.name),
        all_names,
        prefix="wf",
        max_length=flow_name_max_length,
    )
    flow_name = all_names[waldiez.flow.id]
    result: ResultType = {
        "agent_names": agent_names,
        "model_names": model_names,
        "skill_names": skill_names,
        "chat_names": chat_names,
        "agents": agents,
        "models": models,
        "skills": skills,
        "chats": chats,
        "flow_name": flow_name,
    }
    return result
