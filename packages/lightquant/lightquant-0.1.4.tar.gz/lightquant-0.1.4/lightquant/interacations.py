import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

import pyreadr
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

# Define COMMASPACE explicitly
COMMASPACE = ", "


def readRDS(filename):
    data = pyreadr.read_r(filename)
    if data:
        return data[None]


def saveRDS(pd_file, path):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd_df = ro.conversion.py2rpy(pd_file)
    ro.r["saveRDS"](r_from_pd_df, path, version=2)


def send_mail(send_from, send_to, password, subject, text, files=None, is_html=False):
    if not isinstance(send_to, list):
        raise TypeError(f"Expected 'send_to' to be a list, got {type(send_to).__name__}")

    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    if is_html:
        msg.attach(MIMEText(text, "html"))  # Set the content type to HTML
    else:
        # Set the content type to plain text
        msg.attach(MIMEText(text, "plain"))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(send_from, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
