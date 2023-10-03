from fastapi import Form, UploadFile, File
from pydantic import BaseModel

# https://stackoverflow.com/&/60670614
class AwesomeForm(BaseModel):
    username: str
    password: str
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        file: UploadFile = File(...)
    ):

        return cls(
            username = username,
            password = password,
            file = file
        )