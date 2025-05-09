# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Utility functions for generating agent related strings."""

from .captain_agent import get_captain_agent_extras
from .code_execution import get_agent_code_execution_config
from .group_manager import get_group_manager_extras
from .rag_user import get_rag_user_extras
from .reasoning import get_reasoning_agent_extras
from .swarm_agent import get_swarm_extras
from .teachability import get_agent_teachability_string
from .termination_message import get_is_termination_message

__all__ = [
    "get_agent_code_execution_config",
    "get_agent_teachability_string",
    "get_captain_agent_extras",
    "get_group_manager_extras",
    "get_is_termination_message",
    "get_rag_user_extras",
    "get_reasoning_agent_extras",
    "get_swarm_extras",
]
