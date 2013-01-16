__author__ = 'matt'

import smtplib
server = smtplib.SMTP('smtp.webfaction.com', 587)
server.set_debuglevel(True)
server.ehlo()
server.starttls()
server.ehlo()
server.login('crisewing_demobox', 's00p3rs3cr3t')
from_addr = "Matt Kenny <what@test.com>"
to_addrs = "matthewkenny@gmail.com"
subject = "this is a test"
message = "a mesage from python smtplib"

template = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
headers = template % (from_addr, to_addrs, subject)
email_body = headers + message
server.sendmail(from_addr, [to_addrs,], email_body)
server.close()