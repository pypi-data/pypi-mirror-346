from typing import Optional
from pydantic import BaseModel, ConfigDict
from langchain_core.runnables import RunnableConfig


class RemoteRunnableRequest(BaseModel):
    input: dict
    config: Optional[RunnableConfig]
    kwargs: Optional[dict]

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "input": {"messages": []},
                    "config": {},
                    "kwargs": {},
                }
            ]
        },
    )
