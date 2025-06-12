from typing import Optional
from pydantic import BaseModel, Field

class TeamMember(BaseModel):
    team_member_id: str = Field(..., description="Unique identifier for the team member")
    role: str = Field(..., description="Description of what the the team member is responsible for")
    default_team_member: Optional[bool] = Field(False, description="Default team member if no clear team member selected demonstrated by UKNOWN")
    user_request: Optional[str] = Field(default=None, description="The original user request if provided")
    confidence: Optional[float] = Field(default=0.0, description="Confience score if the assigned team member is the correct team member")