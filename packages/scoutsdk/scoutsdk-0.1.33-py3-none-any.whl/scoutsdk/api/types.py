from pydantic import BaseModel
from typing import Any, Union

SCOUT_CUSTOM_FUNCTION_CONTENT_TYPE = "scout/custom function"


class AssistantResponse(BaseModel):
    message: str
    assistant_id: str


class ChatCompletionMessage(BaseModel):
    role: str
    content: Union[str, list[dict[str, Any]]]
