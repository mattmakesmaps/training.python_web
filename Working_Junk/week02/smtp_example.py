__author__ = 'matt'

import smtplib
server = smtplib.SMTP('smtp.webfaction.com', 587)
server.set_debuglevel(True)
server.ehlo()
server.starttls()
server.ehlo()
server.login('crisewing_demobox', 's00p3rs3cr3t')
from_addr = "Hung Dom (Fake) <htdom@comcast.net>"
to_addrs = "matt@ridolfi.com"
subject = "Test Message"
message = "Gimme mah shrimp-fly-rice!"

template = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
headers = template % (from_addr, to_addrs, subject)
email_body = headers + message
server.sendmail(from_addr, [to_addrs,], email_body)
server.close()