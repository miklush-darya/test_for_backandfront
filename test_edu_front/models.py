from typing import Optional
from flask import session
from pydantic import BaseModel as PyModel, EmailStr, Extra, validator


class BaseModel(PyModel):
    id: Optional[int]
    # created: Optional[datetime]
    # modified: datetime = None

    def dict_without_none(self, **kwargs):
        return self.dict(exclude_none=True, **kwargs)


class StoreInSessionMixin:
    def store_in_session(self: BaseModel, **kwargs):
        session[self.__class__.__name__.lower()] = self.dict()
        session.modified = True

    @classmethod
    def from_session(cls):
        data = session.get(cls.__name__.lower())
        if data is not None:
            return cls(**data)


class ErrorModel(PyModel):
    message: str = "Something Wrong."


class Login(PyModel):
    email: EmailStr
    password: str

    class Config:
        extra = Extra.ignore


class Auth(StoreInSessionMixin, PyModel):
    access: str
    refresh: str


class RegisterUser(PyModel):
    email: EmailStr
    password: str
    password_submit: str

    class Config:
        extra = Extra.ignore

    @validator('password_submit')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class User(StoreInSessionMixin, BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
