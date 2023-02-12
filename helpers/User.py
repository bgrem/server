from typing import List
from uuid import uuid4


class UserHelper:
    def __init__(
        self,
        user_name: str,
        user_email: str,
        password: str,
        user_id: str = None,
        roles:List[str] = [],
    ) -> None:
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = f"{uuid4()}"
        self.user_name = user_name
        self.user_email = user_email
        self.password = password
        self.roles = roles
