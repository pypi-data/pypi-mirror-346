from dataclasses import dataclass
from typing import Optional


@dataclass
class AddDataPostData:
    spaceId: str
    ownerId: str
    dataType: str
    fileName: str
    texture_ext: Optional[str] = None


@dataclass
class AddNewSpacePostData:
    spaceName: str
    
    
@dataclass
class DeleteSpacePostData:
    spaceId: str