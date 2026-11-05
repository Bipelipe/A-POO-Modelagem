from dataclasses import dataclass


@dataclass(frozen=True)
class User_account:
    username: str
    password_hash: str
    salt: str
