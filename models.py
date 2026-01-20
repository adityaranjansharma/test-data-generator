from pydantic import BaseModel
from typing import List, Optional

class MockDataRequest(BaseModel):
    count: int
    locale: str = "en_US"
    seed: Optional[int] = None
    email_domain: str = "testcorp.com"

class MockDataResponse(BaseModel):
    count: int
    data: List[dict]
