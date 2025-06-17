from datetime import datetime
from typing import List, Optional

from ollama import Message
from pydantic import BaseModel


class State(BaseModel):
    messages: List[Message]
    documents: Optional[list] = None  # 필요시 문서 객체로 교체
    started_at: datetime
