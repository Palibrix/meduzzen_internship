from fastapi import HTTPException


class UserExist(HTTPException):
	def __init__(self, detail="User with this email already exist"):
		super().__init__(
			status_code=404,
			detail=detail
		)


class CompanyExist(HTTPException):
	def __init__(self, detail="Company with this name already exist"):
		super().__init__(
			status_code=404,
			detail=detail
		)


class ObjectNotFound(HTTPException):
	def __init__(self, detail="Object not found"):
		super().__init__(
			status_code=404,
			detail=detail
		)


class WrongUser(HTTPException):
	def __init__(self, detail="Forbidden"):
		super().__init__(
			status_code=403,
			detail=detail
		)


class CredentialsException(HTTPException):
	def __init__(self, detail="Could not validate credentials"):
		super().__init__(
			status_code=401,
			detail=detail,
			headers={"WWW-Authenticate": "Bearer"},
		)


class WrongPasswordOrEmail(HTTPException):
	def __init__(self, detail="Incorrect username or password"):
		super().__init__(
			status_code=401,
			detail=detail,
			headers={"WWW-Authenticate": "Bearer"},
		)


class InactiveUser(HTTPException):
	def __init__(self, detail="Inactive user"):
		super().__init__(
			status_code=400,
			detail=detail
		)
