from pydantic import BaseModel
from typing import Optional

class AppResponse(BaseModel):
    name: Optional[str]
    size: Optional[str]
    downloads: Optional[str]
    version: Optional[str]
    release_date: Optional[str]
    min_screen: Optional[str]
    supported_cpu: Optional[str]
    package_id: Optional[str]
    sha1_signature: Optional[str]

    developer_cn: Optional[str]
    organization: Optional[str]
    local: Optional[str]
    country: Optional[str]
    state_city: Optional[str]

