import mimetypes
from email.message import EmailMessage
from typing import List, Optional
import aiosmtplib

from ..core.config import settings

class SMTPMailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD

    async def send_mail(
        self,
        to: List[str],
        subject: str,
        body: str,
        body_type: str = "plain",
        attachments: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject

        if cc:
            msg["Cc"] = ", ".join(cc)

        full_recipients = to + (cc if cc else []) + (bcc if bcc else [])

        msg.set_content(body, subtype=body_type)

        if attachments:
            for file_path in attachments:
                content_type, encoding = mimetypes.guess_type(file_path)
                if content_type is None or encoding is not None:
                    content_type = "application/octet-stream"
                main_type, sub_type = content_type.split("/", 1)

                async with await self._read_file(file_path) as file_data:
                    filename = file_path.split("/")[-1]
                    msg.add_attachment(file_data, maintype=main_type, subtype=sub_type, filename=filename)

        await aiosmtplib.send(
            message=msg,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            use_tls=True,
            recipients=full_recipients,
        )

    async def _read_file(self, path: str):
        with open(path, "rb") as f:
            data = f.read()
        return data
