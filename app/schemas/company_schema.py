from typing import Optional, List

from pydantic import BaseModel


class CompanySchema(BaseModel):
	company_name: str
	company_title: str
	company_description: str
	company_city: Optional[str] = None
	company_phone: Optional[str] = None
	company_links: Optional[str] = None
	company_avatar: Optional[str] = None


class Company(CompanySchema):
	company_id: int
	company_owner_id: int


class CompanyCreateRequest(CompanySchema):
	pass


class CompanyUpdateRequest(BaseModel):
	company_name: Optional[str] = None
	company_title: Optional[str] = None
	company_description: Optional[str] = None
	is_visible: Optional[bool] = None


class CompaniesListResponse(BaseModel):
	companies: List[Company]


class CompanyDetailResponse(Company):
	is_visible: bool
