from app.core.exceptions import WrongUser
from app.schemas.user_schema import User
from app.services.user_service import UserService


class IsCurrentUser:

	def __init__(self, db, user_id, token):
		self.db = db
		self.user_id = user_id
		self.token = token
		self.service = UserService(db)

	async def __call__(self):
		current_user: User = await self.service.get_current_user(token=self.token)
		if not self.user_id == current_user.user_id:
			raise WrongUser
