from pydantic import BaseModel

class AuthenticationRequest(BaseModel):
    username: str

class AuthenticationParameters(BaseModel):
    password: bool = True
    mfa: bool = True
    passkey: bool = False
    email: bool = False