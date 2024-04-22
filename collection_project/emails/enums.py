from enum import Enum


class EmailSendingStrategy(Enum):
    LOCAL = "local"
    MAILTRAP = "mailtrap"
    BREVO = "brevo"
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    AWS_SES = "aws_ses"
    POSTMARK = "postmark"
    CUSTOM = "custom"
    MOCK = "mock"
