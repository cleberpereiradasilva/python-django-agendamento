import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import Union


class MailSender:
    def __init__(self, sender_email: str, password: Union[str, int]) -> None:
        self.sender_email = sender_email or ""
        self.password = password

    def send_via_gmail(self, to: str, name: str, code: str, **kwargs) -> bool:
        '''
            Envia um email com o código de agendamento utilizando o servidor SMTP do Gmail.\n

            [to]: email do destinatário\n
            [name]: nome do destinatário\n
            [code]: código do agendamento, o mesmo código deve ser salvo no banco de dados\n

            Retorna <True> após o email ser enviado.
        '''
        receiver_email: str = kwargs.get('to', to)
        receiver_name: str = kwargs.get('name', name)
        code: str = kwargs.get('code', code)

        if not receiver_email or not receiver_name:
            print('[!!!] receiver_email or receiver_name were not provided, email not sended. [!!!]')
            return

        message = MIMEMultipart("alternative")
        message["Subject"] = "GIMI - Seu código de agendamento de reunião."
        message["From"] = self.sender_email
        message["To"] = receiver_email

        html = f"""
        <html>
            <head>
                <style>
                    p {'{ font-size: 1rem; }'}
                </style>
            </head>
            <body>
                <p>
                    Olá, {receiver_name}<br>
                    Aqui está o número do seu agendamento na sala de reuniões.<br>
                </p>
                <h1>{code}</h1>
                <p><strong>Somente você</strong> pode utilizá-lo para excluir/cancelar seu agendamento.</p>
            </body>
        </html>
        """
        message.attach(MIMEText(html, "html"))

        ssl_context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email,
                receiver_email,
                msg=message.as_string()
            )