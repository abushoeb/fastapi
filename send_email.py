from fastapi import (
    FastAPI, 
    BackgroundTasks, 
    UploadFile, File, 
    Form, 
    Query,
    Body,
    Depends
)

from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any
from fastapi_mail.email_utils import DefaultChecker
from pathlib import Path

class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "email": ["type recipient email addess"],
                "subject": "FastAPI Templated Mail",
                "body": {"first_name": "recipient first name",
                        "last_name": "recipient last name"},
            }
        }

        
BASE_DIR = Path(__file__).resolve().parent

conf = ConnectionConfig(
    MAIL_USERNAME = "YourUsername",
    MAIL_PASSWORD = "strong_password",
    MAIL_FROM = "your@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "your mail server",
    MAIL_FROM_NAME="Desired Name",
    MAIL_TLS=True,
    MAIL_SSL=False,
    # USE_CREDENTIALS = True,
    # VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(BASE_DIR, 'templates')
)

app = FastAPI(title="Email - FastAPI", description="Sample Email Script")


@app.post("/email")
async def send_with_template(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail with HTML Templates",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        template_body=email.dict().get("body"),
        )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email_template.html") 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
