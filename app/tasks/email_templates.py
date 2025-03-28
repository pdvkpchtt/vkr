from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings

def create_mechanic_confirmation_template(
    description: str,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Новая заявка на ремонт!"
    email["From"] = settings.smtp_user
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Новая заявка</h1>
            Описание заявки от водителя: {description}
        """,
        subtype="html"
    )
    return email

def create_driver_confirmation_template(
    bid_id: int,
    description: str,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Новая заявка на ремонт"
    email["From"] = settings.smtp_user
    email["To"] = email_to

    email.set_content(
        f"""
                <h1>Успешное выполнение заявки!</h1>
            Ваша заявка на ремонт {bid_id} готова!
            Описание заявки от механика: {description}
        """,
        subtype="html"
    )
    return email
