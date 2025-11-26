from app.core.repositories import Repository
from app.modules.users.models import User


class UserRepository(Repository):

    model = User
