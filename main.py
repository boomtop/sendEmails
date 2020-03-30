import smtplib
import os
import sys
from configparser import ConfigParser
from validate_email import validate_email


# TODO  отправка письма одному адресату
# TODO создать форму с подписью фирмы
# TODO создать папку для вложений, которые после отправки удаляются
# TODO парсинг csv и добавление в адресата


def send_mail(subject, text, to):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    host = cfg.get("smtp", "server_name")
    username = cfg.get("smtp", "login")
    password = cfg.get("smtp", "password")
    from_addr = cfg.get("smtp", "from_addr")
    port = cfg.get("smtp", "server_port")

    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "BCC: %s" % to_mail,
        "Subject: %s" % subject,
        "",
        text
    ))

    try:
        server = smtplib.SMTP_SSL(host, port)
        server.login(username, password)
    except smtplib.SMTPConnectError:
        print("Error Connect")
    except smtplib.SMTPAuthenticationError:
        print("Error password or login")
    except smtplib.SMTPServerDisconnected:
        print("Server Error")
    server.sendmail(from_addr, to, BODY)
    server.quit()


if __name__ == '__main__':
    subject = "Test send mail"
    to = ["reklama_vol35@mail.ru", "ololol@rio-vologda,ru", "avlipro12@gmail.com"]
    text = "Bla bla bla"
    # send_mail(subject, text, to)
    for to_mail in to:
        valid_email = validate_email(to_mail, verify=True)
        print(to_mail, valid_email)
        send_mail(subject, text, to_mail)
