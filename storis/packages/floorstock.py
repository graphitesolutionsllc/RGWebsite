"""
floorStock
This file will provide the functionality of checking in stock and the changes that happen day to day
this will assist in updating managers and salesman to keep the floor stickers working.
"""
import smtplib
from pathlib import Path

import pandas as pd
import datetime
import yagmail

pd.options.mode.chained_assignment = None


def checkChanges():
    """
    This will check the stockSKU files from today and yesterday to see if there are any changes to report
    :return: List of changes
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent) + '\settings.csv')
    current_time = datetime.datetime.now()
    last_time = datetime.datetime.now() - datetime.timedelta(days=1)
    current_time = str(current_time.month) + "." + str(current_time.day) + "." + str(current_time.year)[2:4]
    last_time = str(last_time.month) + "." + str(last_time.day) + "." + str(last_time.year)[2:4]

    try:
        today = pd.read_csv(str(df.loc[0].epath) + "\instock\storisSTOCK " + current_time + ".csv")
    except(FileNotFoundError):
        print("Todays Stock Skus have not been generated yet")
        return 0

    try:
         yesterday = pd.read_csv(str(df.loc[0].epath) + "\instock\storisSTOCK " + last_time + ".csv")
    except(FileNotFoundError):
        print("Yesterdays Stock Skus are not in the directory")
        return 0

    df = pd.concat([yesterday, today]).drop_duplicates(keep=False)
    df = df.assign(intoday=df.Product.isin(today.Product).astype(int))
    df = df.assign(outtoday=df.Product.isin(yesterday.Product).astype(int))
    intoday = df.loc[df['intoday'] == 1]
    outtoday = df.loc[df['outtoday'] == 1]
    print(intoday)
    print("---------------------------\n")
    print(outtoday)
    emailChanges(intoday, outtoday)
    return 0

def emailChanges(intoday, outtoday):
    """

    :return:
    """
    sent_from = "dduffy385@gmail.com"
    to = "dmd9042@gmail.com"
    #intoday = str(intoday['Product'].values.tolist())
    outtoday = str(outtoday['Product'].values.tolist())

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login("dduffy385@gmail.com", "Pushthebutton8*")
        server.send(to,"Daily Stock Update", intoday.to_string(index=False))
        server.close()
    except:
        print('Something went wrong...')
    return 0