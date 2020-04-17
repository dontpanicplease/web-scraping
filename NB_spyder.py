import smtplib
import pandas as pd
import bs4
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# LF required data.
r = requests.get('https://www.welcomenb.ca/content/wel-bien/en/recruitment_events.html')
soup = bs4.BeautifulSoup(r.text, "lxml")

maintable = soup.table
tr_list = []

for tr in maintable.find_all('tr'):
    tr = tr.text.strip()
    tr_list.append(tr)


# Turn to data frame.
df = pd.DataFrame(data=tr_list, columns=['Date'])
df[['Date','Time', 'Event', 'Place', 'Status']] = df['Date'].str.split('\n', expand=True)
df.to_excel('/Users/antonlysenko/Desktop/nbsr.xlsx')


fromaddr = "linuxman2019@gmail.com"
toaddr = "bhua2017@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "New Branswick upcoming National and International Recruitment Events update!"

body = """Hey there !

Please find the report about Upcoming National and International Recruitment Events
for NB Canada in attachment to this letter.

Regards,
Web-spider"""

msg.attach(MIMEText(body, 'plain'))

filename = "nbsr.xlsx"
attachment = open("/Users/antonlysenko/Desktop/nbsr.xlsx", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Areyou1or0")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
