from app.modules.users.models import User
from app.shared.repositories import Repository


class UserRepository(Repository):

    model = User
