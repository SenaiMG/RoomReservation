from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

class EmailService:
    @staticmethod
    def send_text_email(subject, message, recipient_list, from_email=None):
        """
        Envia um email de texto simples.
        """
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )

        email.send()

    @staticmethod
    def send_html_email(subject, html_content, recipient_list, from_email=None):
        """
        Envia um email com corpo HTML.
        """
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = "html"  # Define o conteúdo como HTML

        email.send()

    @staticmethod
    def send_email_with_attachment(subject, message, recipient_list, attachment_path, from_email=None, html_message=None):
        """
        Envia um email com anexo, opcionalmente pode incluir corpo HTML.
        """
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )

        if html_message:
            email.content_subtype = "html"  # Define o conteúdo como HTML
            email.body = html_message

        email.attach_file(attachment_path)  # Anexa o arquivo

        email.send()

    
    @staticmethod
    def send_html_email_with_template(subject, template_name, context, recipient_list, from_email=None):
        """
        Envia um email com corpo HTML renderizado a partir de um template.
        """
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        html_content = render_to_string(template_name, context)
        
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = "html"  # Define o conteúdo como HTML

        email.send()






"""
Formas de enviar o email:
from notifications.services import EmailService

# Exemplo de envio de um email de texto simples
EmailService.send_text_email(
    subject="Sua reserva foi confirmada",
    message="Sua reserva para a sala XYZ foi confirmada.",
    recipient_list=["usuario@example.com"]
)

# Exemplo de envio de um email com corpo HTML
EmailService.send_html_email(
    subject="Sua reserva foi confirmada",
    html_content="<h1>Reserva Confirmada</h1><p>Sua reserva para a sala XYZ foi confirmada.</p>",
    recipient_list=["usuario@example.com"]
)

# Exemplo de envio de um email com anexo e corpo HTML
EmailService.send_email_with_attachment(
    subject="Documento Importante",
    message="Veja o documento em anexo.",
    recipient_list=["usuario@example.com"],
    attachment_path="/caminho/para/anexo.pdf",
    html_message="<p>Veja o documento em anexo.</p>"
)


#exemplo de envio com template html
context = {
    'user': user,
    'room': room,
    'reservation_date': reservation_date,
    'time_slot': time_slot,
}

EmailService.send_html_email_with_template(
    subject="Confirmação de Reserva",
    template_name="emails/email_confirmacao_reserva.html",
    context=context,
    recipient_list=[user.email]
)
"""
