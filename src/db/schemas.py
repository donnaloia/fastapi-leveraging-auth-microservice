from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class OrganizationBase(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

class CreateOrganization(OrganizationBase):
    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    organization_id: UUID

    class Config:
        orm_mode = True


class ApplicationDetailed(ApplicationBase):
    # this modifies the payload to replace the Application uuid with the entire Application as a nested resource
    organization: OrganizationBase
        
    class Config:
        exclude = ['organization_id']
    

class CreateApplication(ApplicationBase):
    id: Optional[UUID] = None
    
    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    application_id: UUID

    class Config:
        orm_mode = True


class ServiceDetailed(ServiceBase):
    application: ApplicationBase
        
    class Config:
        exclude = ['application_id']
    

class CreateApplication(ServiceBase):
    id: Optional[UUID] = None
    
    class Config:
        orm_mode = True