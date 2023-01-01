import requests
import selectorlib
import time
import smtplib, ssl
import os
import sqlite3



url = 'http://programmer100.pythonanywhere.com/tours/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url = url, headers=HEADERS)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    print(f"Value: {value}")
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "zafrip14@gmail.com"
    password = "lroyqtbeghgwydpn"

    receiver = "zafrip14@gmail.com"
    context = ssl.create_default_context()

    msg = f"Subject: Tours\n".encode('utf-8') + message.encode('utf-8')

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(from_addr= username, to_addrs=receiver, msg=msg)



def add_tours(tour):
    print('Inserting values in DB')
    cursor.execute("INSERT INTO events VALUES(?,?,?)", tour)
    connection.commit()


def read_tours(tour):
    tour = tour.split(",")
    tour = [item.strip() for item in tour]
    band, city, date  = tour

    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    check = cursor.fetchall()

    if check:
        result = []
    else:
        result = tour
    
    return result



if __name__ == '__main__':
    count = 1
    while count <= 10:
        scraped = scrape(url)
        extracted = extract(scraped)
        print(extracted)
        if extracted != 'No upcoming tours':
            result = read_tours(extracted)
            if result:
                add_tours(result)
                # send_email(message=extracted)
        time.sleep(1)
        count += 1

