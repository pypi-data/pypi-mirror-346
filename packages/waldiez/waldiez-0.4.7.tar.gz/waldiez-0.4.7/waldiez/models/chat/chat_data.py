# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Chat data model."""

from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator, model_validator
from typing_extensions import Annotated, Self

from ..agents.swarm_agent import (
    WaldiezSwarmAfterWork,
    WaldiezSwarmOnConditionAvailable,
)
from ..common import WaldiezBase, check_function, update_dict
from .chat_message import (
    CALLABLE_MESSAGE,
    CALLABLE_MESSAGE_ARGS,
    WaldiezChatMessage,
)
from .chat_nested import WaldiezChatNested
from .chat_summary import WaldiezChatSummary


class WaldiezChatData(WaldiezBase):
    """Chat data class.

    Attributes
    ----------
    name : str
        The name of the chat.
    source : str
        The source of the chat (sender).
    target : str
        The target of the chat (recipient).
    description : str
        The description of the chat.
    position : int
        The position of the chat. Ignored (UI related).
    order : int
        The of the chat. If negative, ignored.
    clear_history : Optional[bool], optional
        Whether to clear the chat history, by default None.
    message : Union[str, WaldiezChatMessage]
        The message of the chat.
    nested_chat : WaldiezChatNested
        The nested chat config.
    summary : WaldiezChatSummary
        The summary method and options for the chat.
    max_turns : Optional[int]
        The maximum number of turns for the chat, by default None (no limit).
    silent : Optional[bool], optional
        Whether to run the chat silently, by default None (ignored).
    summary_args : Optional[Dict[str, Any]]
        The summary args to use in autogen.
    real_source : Optional[str]
        The real source of the chat (overrides the source).
    real_target : Optional[str]
        The real target of the chat (overrides the target).
    max_rounds : int
        Maximum number of conversation rounds (swarm).
    after_work : Optional[WaldiezSwarmAfterWork]
        The work to do after the chat (swarm).

    Functions
    ---------
    validate_message(value: Any)
        Validate the message.
    validate_summary_method(value: Optional[WaldiezChatSummaryMethod])
        Validate the summary method.
    serialize_summary_method(value: Any, info: FieldSerializationInfo)
        Serialize summary method.
    get_chat_args()
        Get the chat arguments to use in autogen.
    """

    name: Annotated[
        str, Field(..., title="Name", description="The name of the chat.")
    ]
    source: Annotated[
        str,
        Field(
            ...,
            title="Source",
            description="The source of the chat (sender).",
        ),
    ]
    target: Annotated[
        str,
        Field(
            ...,
            title="Target",
            description="The target of the chat (recipient).",
        ),
    ]
    description: Annotated[
        str,
        Field(
            ...,
            title="Description",
            description="The description of the chat.",
        ),
    ]
    position: Annotated[
        int,
        Field(
            -1,
            title="Position",
            description="The position of the chat in the flow (Ignored).",
        ),
    ]
    order: Annotated[
        int,
        Field(
            -1,
            title="Order",
            description="The order of the chat in the flow.",
        ),
    ]
    clear_history: Annotated[
        Optional[bool],
        Field(
            None,
            alias="clearHistory",
            title="Clear History",
            description="Whether to clear the chat history.",
        ),
    ]
    message: Annotated[
        Union[str, WaldiezChatMessage],
        Field(
            title="Message",
            description="The message of the chat.",
            default_factory=WaldiezChatMessage,
        ),
    ]
    nested_chat: Annotated[
        WaldiezChatNested,
        Field(
            title="Nested Chat",
            description="The nested chat.",
            alias="nestedChat",
            default_factory=WaldiezChatNested,
        ),
    ]
    summary: Annotated[
        WaldiezChatSummary,
        Field(
            default_factory=WaldiezChatSummary,
            title="Summary",
            description="The summary method options for the chat.",
        ),
    ]
    max_turns: Annotated[
        Optional[int],
        Field(
            None,
            alias="maxTurns",
            title="Max Turns",
            description="The maximum number of turns for the chat.",
        ),
    ]
    prerequisites: Annotated[
        List[str],
        Field(
            title="Prerequisites",
            description="The prerequisites (chat ids) for the chat (if async).",
            default_factory=list,
        ),
    ]
    silent: Annotated[
        Optional[bool],
        Field(
            None,
            title="Silent",
            description="Whether to run the chat silently.",
        ),
    ]
    real_source: Annotated[
        Optional[str],
        Field(
            None,
            alias="realSource",
            title="Real Source",
            description="The real source of the chat (overrides the source).",
        ),
    ]
    real_target: Annotated[
        Optional[str],
        Field(
            None,
            alias="realTarget",
            title="Real Target",
            description="The real target of the chat (overrides the target).",
        ),
    ]
    max_rounds: Annotated[
        int,
        Field(
            20,
            title="Max Rounds",
            description="Maximum number of conversation rounds.(swarm)",
        ),
    ] = 20
    after_work: Annotated[
        Optional[WaldiezSwarmAfterWork],
        Field(
            None,
            alias="afterWork",
            title="After Work",
            description="The work to do after the chat (swarm).",
        ),
    ] = None
    context_variables: Annotated[
        Optional[Dict[str, Any]],
        Field(
            None,
            alias="contextVariables",
            title="Context Variables",
            description="The context variables to use in the chat.",
        ),
    ] = None
    available: Annotated[
        WaldiezSwarmOnConditionAvailable,
        Field(
            default_factory=WaldiezSwarmOnConditionAvailable,
            title="Available",
            description="The available condition for the chat.",
        ),
    ]

    _message_content: Optional[str] = None
    _chat_id: int = 0
    _prerequisites: List[int] = []

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self._message_content

    def get_chat_id(self) -> int:
        """Get the chat id.

        Returns
        -------
        int
            The chat id.
        """
        return self._chat_id

    def set_chat_id(self, value: int) -> None:
        """Set the chat id.

        Parameters
        ----------
        value : int
            The chat id.
        """
        self._chat_id = value

    def get_prerequisites(self) -> List[int]:
        """Get the chat prerequisites.

        Returns
        -------
        List[int]
            The chat prerequisites (if async).
        """
        return self._prerequisites

    def set_prerequisites(self, value: List[int]) -> None:
        """Set the chat prerequisites.

        Parameters
        ----------
        value : List[int]
            The chat prerequisites to set.
        """
        self._prerequisites = value

    @model_validator(mode="after")
    def validate_chat_data(self) -> Self:
        """Validate the chat data.

        Returns
        -------
        WaldiezChatData
            The validated chat data.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if not isinstance(self.message, WaldiezChatMessage):  # pragma: no cover
            return self
        self._message_content = self.message.content
        if self.message.type == "none":
            self._message_content = None
        if self.message.type == "string":
            self._message_content = self.message.content
        if self.message.type == "method":
            valid, error_or_body = check_function(
                self.message.content or "",
                CALLABLE_MESSAGE,
                CALLABLE_MESSAGE_ARGS,
            )
            if not valid:
                raise ValueError(error_or_body)
            self._message_content = error_or_body
        return self

    @field_validator("message", mode="before")
    @classmethod
    def validate_message(cls, value: Any) -> WaldiezChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The message value.

        Returns
        -------
        WaldiezChatMessage
            The validated message value.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if value is None:
            return WaldiezChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        if isinstance(value, (str, int, float, bool)):
            return WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content=str(value),
                context={},
            )
        if isinstance(value, dict):
            return WaldiezChatMessage.model_validate(value)
        if not isinstance(value, WaldiezChatMessage):
            return WaldiezChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        return value

    @field_validator("context_variables", mode="after")
    @classmethod
    def validate_context_variables(
        cls, value: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Validate the context variables.

        Parameters
        ----------
        value : Optional[Dict[str, Any]]
            The context variables value.

        Returns
        -------
        Optional[Dict[str, Any]]
            The validated context variables value.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if value is None:
            return None
        return update_dict(value)

    @property
    def summary_args(self) -> Optional[Dict[str, Any]]:
        """Get the summary args."""
        if self.summary.method not in (
            "reflection_with_llm",
            "reflectionWithLlm",
        ):
            return None
        args: Dict[str, Any] = {}
        if self.summary.prompt:
            args["summary_prompt"] = self.summary.prompt
        if self.summary.args:
            args.update(self.summary.args)
        return args

    def _get_context_args(self) -> Dict[str, Any]:
        """Get the context arguments to use in autogen.

        Returns
        -------
        Dict[str, Any]
            The dictionary to use for generating the kwargs.
        """
        extra_args: Dict[str, Any] = {}
        if not isinstance(self.message, WaldiezChatMessage):  # pragma: no cover
            return extra_args
        extra_args.update(update_dict(self.message.context))
        return extra_args

    def get_chat_args(self, for_queue: bool) -> Dict[str, Any]:
        """Get the chat arguments to use in autogen.

        Without the 'message' key.

        Parameters
        ----------
        for_queue : bool
            Whether to get the arguments for a chat queue.

        Returns
        -------
        Dict[str, Any]
            The dictionary to pass as kwargs.
        """
        args: Dict[str, Any] = {}
        if self.summary.method:
            args["summary_method"] = self.summary.method
        if self.summary_args:
            args["summary_args"] = self.summary_args
        if isinstance(self.max_turns, int) and self.max_turns > 0:
            args["max_turns"] = self.max_turns
        if isinstance(self.clear_history, bool):
            args["clear_history"] = self.clear_history
        if isinstance(self.silent, bool):
            args["silent"] = self.silent
        args.update(self._get_context_args())
        if for_queue:
            args["chat_id"] = self._chat_id
        if self._prerequisites:
            args["prerequisites"] = self._prerequisites
        return args
