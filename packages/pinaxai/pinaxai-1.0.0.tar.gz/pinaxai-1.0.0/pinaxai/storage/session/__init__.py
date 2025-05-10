from typing import Union

from pinaxai.storage.session.agent import AgentSession
from pinaxai.storage.session.team import TeamSession
from pinaxai.storage.session.workflow import WorkflowSession

Session = Union[AgentSession, TeamSession, WorkflowSession]

__all__ = [
    "AgentSession",
    "TeamSession",
    "WorkflowSession",
    "Session",
]
