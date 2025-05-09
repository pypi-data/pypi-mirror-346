from typing import Optional, List

from pydantic import BaseModel, computed_field


class ToolSearchResultDetails(BaseModel):
    url: Optional[str] = ""
    title: Optional[str] = ""
    content: str
    date_published: Optional[str] = ""

    @computed_field
    def content_with_weight(self) -> str:
        return f"URL:{self.url}\nTITLE: {self.title}\nDATE PUBLISHED: {self.date_published}\nCONTENT: {self.content}"


class ToolSearchResult(BaseModel):
    result: Optional[List[ToolSearchResultDetails]] = []
