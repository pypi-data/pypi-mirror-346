from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from projectdavid_common.schemas.users_schema import UserBase


class ThreadCreate(BaseModel):
    # ⬇ default=[] lets the field be omitted entirely
    participant_ids: list[str] = Field(
        default_factory=list,
        description="Additional participant IDs (caller is added automatically)",
    )
    meta_data: dict[str, Any] | None = Field(
        default=None, description="Optional metadata for thread"
    )


class ThreadRead(BaseModel):
    id: str
    created_at: int
    meta_data: Dict[str, Any]
    object: str
    tool_resources: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class ThreadUpdate(BaseModel):
    participant_ids: Optional[List[str]] = Field(
        default=None, description="Updated list of participant IDs"
    )
    meta_data: Optional[Dict[str, Any]] = Field(default=None, description="Updated metadata")

    model_config = ConfigDict(from_attributes=True)


class ThreadParticipant(UserBase):
    pass


class ThreadReadDetailed(ThreadRead):
    participants: List[UserBase]

    model_config = ConfigDict(from_attributes=True)


class ThreadIds(BaseModel):
    thread_ids: List[str]

    model_config = ConfigDict(from_attributes=True)
