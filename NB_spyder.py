# List of used libs

import smtplib
import pandas as pd
import bs4
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Data source for scraping & required data.

r = requests.get('https://www.welcomenb.ca/content/wel-bien/en/recruitment_events.html')
soup = bs4.BeautifulSoup(r.text, "lxml")

maintable = soup.table
tr_list = []

for tr in maintable.find_all('tr'):
    tr = tr.text.strip()
    tr_list.append(tr)


# Turn the data to dataframe.

df = pd.DataFrame(data=tr_list, columns=['Date'])
df[['Date','Time', 'Event', 'Place', 'Status']] = df['Date'].str.split('\n', expand=True)
df.to_excel('/Users/antonlysenko/Desktop/nbsr.xlsx')


# Mail setup.

fromaddr = "me@gmail.com" # send from mail adr
toaddr = "someone@gmail.com"   # send to mail adr

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr

msg['Subject'] = "New Branswick upcoming National and International Recruitment Events update!" # Letter's subj

body = """Hey there !

Please find the report about Upcoming National and International Recruitment Events
for NB Canada in attachment to this letter.

Regards,
Web-spider"""  

msg.attach(MIMEText(body, 'plain'))

filename = "nbsr.xlsx"
attachment = open("/Users/antonlysenko/Desktop/nbsr.xlsx", "rb") # file attachment path

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, " ")  # password for mail sender required
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
