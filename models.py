from pydantic import BaseModel
from typing import List, Optional

class MockDataRequest(BaseModel):
    count: int
    locale: str = "en_GB"
    seed: Optional[int] = None
    email_domain: str = "testcorp.co.uk"


class MockDataResponse(BaseModel):
    count: int
    data: List[dict]
