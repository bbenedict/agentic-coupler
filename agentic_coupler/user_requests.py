from typing import List
from pydantic import BaseModel


class UserRequests(BaseModel):  # Pydantic required for structured output, otherwise unecessary class
    user_requests: List[str]
