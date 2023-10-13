from typing import Optional, List

import phonenumbers
from pydantic import BaseModel, constr, field_validator, AnyUrl


class CompanySchema(BaseModel):
	company_name: constr(min_length=1, max_length=100)
	company_title: constr(min_length=1, max_length=100)
	company_description: constr(min_length=1, max_length=500)
	company_city: Optional[constr(min_length=1, max_length=100)] = None
	company_phone: Optional[str] = None
	company_links: Optional[AnyUrl] = None
	company_avatar: Optional[AnyUrl] = None

	@field_validator('company_phone')
	def validate_phone(cls, field):
		if field is not None:
			field = phonenumbers.parse(field)
			if not phonenumbers.is_valid_number(field):
				raise ValueError('Invalid phone number')
		return field


class Company(CompanySchema):
	company_id: int
	company_owner_id: int


class CompanyCreateRequest(CompanySchema):
	pass


class CompanyUpdateRequest(BaseModel):
	company_name: Optional[constr(min_length=1, max_length=100)] = None
	company_title: Optional[constr(min_length=1, max_length=100)] = None
	company_description: Optional[constr(min_length=1, max_length=500)] = None
	is_visible: Optional[bool] = None


class CompaniesListResponse(BaseModel):
	companies: List[Company]


class CompanyDetailResponse(Company):
	is_visible: bool
