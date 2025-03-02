import pydantic

class UserBase(pydantic.BaseModel):
    name: str
    password: str

    @pydantic.field_validator("content")
    @classmethod
    def check_content(cls, value):
        if len(value) < 1:
            raise ValueError("The content field cannot be empty")
        return value



class CreateUser(UserBase):
    title: str
    content: str


class UpdateUser(UserBase):
    title: str | None = None
    content: str | None = None
