import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import Literal, Union


class MailSender:
    def __init__(self, sender_email: str, password: Union[str, int]) -> None:
        self.sender_email = sender_email or ""
        self.password = password

    def __get_default_message(self, receiver_email: str, receiver_name: str, code: str):
        """Retorna a mensagem padrão utilizada para o corpo do email."""
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

        return message

    def __connect_to_smtp_server_and_send_mail(
        self,
        server_host: str,
        server_port: int,
        receiver_email: str,
        message: str,
        has_ssl: Union[bool, None] = None,
        tls: Union[bool, None] = None,
    ) -> Literal['success', 'failure']:
        """Realiza uma conexão SMTP e envia um email."""

        SMTP_HANDLER = smtplib.SMTP_SSL if has_ssl else smtplib.SMTP
        smtp_kwargs = { 'host': server_host, 'port': server_port }

        ssl_context = ssl.create_default_context()
        if has_ssl:
            smtp_kwargs['context'] = ssl_context

        try:
            with SMTP_HANDLER(**smtp_kwargs) as server:
                if tls:
                    server.starttls(context=ssl_context)

                server.login(self.sender_email, self.password)
                server.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=receiver_email,
                    msg=message
                )
            return 'success'
        except smtplib.SMTPAuthenticationError as e:
            print(f'Erro ao autenticar email <{self.sender_email}>: {e}')
            return 'failure'
        except smtplib.SMTPConnectError as e:
            print(f'Erro durante a conexão SMTP <{self.sender_email}>: {e}')
            return 'failure'

    def send_via_gmail(self, to: str, name: str, code: str, **kwargs) -> None:
        '''
            Envia um email com o código de agendamento utilizando o servidor SMTP do Gmail.\n

            [to]: email do destinatário\n
            [name]: nome do destinatário\n
            [code]: código do agendamento, o mesmo código deve ser salvo no banco de dados
        '''
        receiver_email: str = kwargs.get('to', to)
        receiver_name: str = kwargs.get('name', name)

        message = self.__get_default_message(receiver_email, receiver_name, code)

        self.__connect_to_smtp_server_and_send_mail(
            server_host='smtp.gmail.com',
            server_port=465,
            has_ssl=True,
            receiver_email=receiver_email,
            message=message.as_string(),
        )
    
    def send_via_outlook(self, to: str, name: str, code: str, **kwargs) -> None:
        '''
            Envia um email com o código de agendamento utilizando o servidor SMTP do Outlook.\n

            [to]: email do destinatário\n
            [name]: nome do destinatário\n
            [code]: código do agendamento, o mesmo código deve ser salvo no banco de dados
        '''
        receiver_email: str = kwargs.get('to', to)
        receiver_name: str = kwargs.get('name', name)

        message = self.__get_default_message(receiver_email, receiver_name, code)

        self.__connect_to_smtp_server_and_send_mail(
            server_host='smtp-mail.outlook.com',
            server_port=587,
            tls=True,
            receiver_email=receiver_email,
            message=message.as_string(),
        )
    