from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

# 1. Define the "Allow-List" of Tools
# The AI can ONLY do these 3 things.
class ToolCall(BaseModel):
    tool_name: Literal["search_web", "read_pdf", "summarize_text"] = Field(
        ..., description="The name of the tool the AI wants to use"
    )
    arguments: str = Field(..., description="The input for the tool")

    # 2. Point 3: Validate Tool Arguments
    @field_validator("arguments")
    def prevent_path_traversal(cls, v):
        # Prevent the AI from trying to access system files like /etc/passwd
        forbidden_keywords = ["/etc/", "C:\\", ".env", "password", "config"]
        if any(keyword in v.lower() for keyword in forbidden_keywords):
            raise ValueError("SECURITY ALERT: Unauthorized file path or keyword detected!")
        return v
