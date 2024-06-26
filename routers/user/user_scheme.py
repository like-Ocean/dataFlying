from pydantic import BaseModel, Field, EmailStr


class RegisterModel(BaseModel):
    login: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)


class DeleteAvatarModel(BaseModel):
    user_id: int = Field(...)


class ChangeModel(BaseModel):
    user_id: int = Field(...)
    login: str | None = Field(None)
    email: EmailStr | None = Field(None)
    IMEI: str | None = Field(None)
    phone_number: str | None = Field(None)


class DeleteUserModel(BaseModel):
    user_id: int = Field(...)


class ChangePasswordModel(BaseModel):
    user_id: int = Field(...)
    password: str = Field(min_length=8)


class Authorization(BaseModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class Item(BaseModel):
    key1: str = Field()
    key2: str = Field()

