from typing import Optional, List

import phonenumbers
from phonenumbers.phonenumberutil import format_number, PhoneNumberFormat, NumberParseException
from pydantic import BaseModel, constr, field_validator, Field


class CompanySchema(BaseModel):
	company_name: constr(min_length=1, max_length=100)
	company_title: constr(min_length=1, max_length=100)
	company_description: constr(min_length=1, max_length=500)
	company_city: Optional[constr(min_length=1, max_length=100)] = None
	company_phone: Optional[str] = None
	company_links: Optional[str] = None
	company_avatar: Optional[str] = None

	@field_validator('company_phone')
	def validate_phone(cls, field):
		if field is not None:
			try:
				field = phonenumbers.parse(field)
				if not phonenumbers.is_valid_number(field):
					raise ValueError('Invalid phone number')
				field = format_number(field, PhoneNumberFormat.E164)
			except NumberParseException as e:
				raise ValueError(f'An error occurred while parsing the phone number: {str(e)}')
			except Exception as e:
				raise ValueError(f'An unexpected error occurred: {str(e)}')
		return field


class Company(CompanySchema):
	company_id: int = Field(..., gt=0)
	company_owner_id: int = Field(..., gt=0)


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
