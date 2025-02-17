from flask_mail import Message
from happy_again import mail
from happy_again.common.consts import HAPPY_AGAIN_NO_REPLY_EMAIL, DATE_FORMAT, BASE_PATH


def send_email(to, subject, msg_html):
    msg = Message(subject, recipients=to, html=msg_html, sender=HAPPY_AGAIN_NO_REPLY_EMAIL)
    mail.send(msg)

def send_email_with_attachments(to, subject, msg_html, pdfname):

    msg = Message(subject, recipients=to, html=msg_html, sender=HAPPY_AGAIN_NO_REPLY_EMAIL)
    binary_pdf = open(BASE_PATH + '/apis/users/email_pdfs/' + pdfname, 'rb')
    msg.attach(pdfname, 'application/pdf', binary_pdf.read())
    mail.send(msg)


def datetime_to_str(date):
    if date:
        return date.strftime(DATE_FORMAT)
    return None
