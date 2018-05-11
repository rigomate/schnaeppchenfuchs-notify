import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from germanMonth import NumberFromGermanMonth

# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
import time

# Import smtplib (to allow us to email)
import smtplib

import re
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    print('credentials are here' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
    SendMessageInternal(service, "me", message1)

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessage(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def SendEmail(msgPlain):
    to = "rigo.mate@gmail.com"
    sender = "rigo.mate@gmail.com"
    subject = "Fire Stick"
    msgHtml = msgPlain
    SendMessage(sender, to, subject, msgHtml, msgPlain)


def main():
    # set the url as VentureBeat,
    url = "https://schnaeppchenfuchs.com/suche?search=fire+tv+stick"
    # set the headers like we are a browser,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup)

    reg_fire = re.compile('<h2>.*stick.*<\/h2>')
    reg_date = re.compile('\s*(\d*).\s*(\S*)\s*(\d{4})\s\d*:\d{2}')
    #reg_date = re.compile('.*2018.*', flags=re.M)
    result = reg_fire.match(soup.getText())

    now = datetime.date.today()
    yesterday = now - datetime.timedelta(days=8)
    page = soup.find_all('div', {'class':'post'})
    for item in page:
        result = reg_date.search(item.__str__())
        #print(item.__str__())
        if result:
            year = result.group(3)
            month = NumberFromGermanMonth(result.group(2))
            day = result.group(1)
            print (year, month, day)
            postdate = datetime.date(int(year), int(month), int(day))
            if (postdate == now):
                print ("send email!")
                SendEmail("Fire Stick: https://schnaeppchenfuchs.com/suche?search=fire+tv+stick")

    #print (result)

if __name__ == "__main__":
    # execute only if run as a script
    main()