import os
import csv
from collections import defaultdict
import random
from pprint import pprint
import smtplib
from email.mime.text import MIMEText

dir = os.path.dirname(__file__)
file = dir + '\\userlist.csv'
data = defaultdict(dict)
user_done = []
assigned_done = []
users = []
assignmets = {}

def run_sim(user):
    #print("running match . . .")
    if user in user_done:
        return
    num = random.randrange(0, len(users))
    if users[num] == user:
        #print("same person . . .")
        run_sim(user)
    elif users[num] in assigned_done:
        #print("already assigned . . .")
        run_sim(user)
    elif users[num] in data[user]['no']:
        #print("exclusion . . .")
        run_sim(user)
    else:
        #print("%s matched with %s" % (user, users[num]))
        assignmets[user] = users[num]
        user_done.append(user)
        assigned_done.append(users[num])

def send_texts():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('username', 'password')
    for santa in assignmets:
        msg = MIMEText("You are assigned %s as secret santa" % assignmets[santa])
        msg['To'] = data[santa]['phone']
        msg['Subject'] = "Secret Santa!"
        s.send_message(msg)
        print("%s has been sent a message" % santa)
    s.quit()


with open(file, 'r')as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data[row[0]]['phone'] = row[1]
        data[row[0]]['no'] = row[2].split(',')
        users.append(row[0])
    for key in users:
        run_sim(key)

    send_texts()

pprint(assigned_done)