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
        today = pd.read_csv(str(df.loc[0].epath) + "\showroomstock\warehouse " + current_time + ".csv")
        del today['Quantity']
        today = today[~today.Product.str.endswith("SO")]
    except(FileNotFoundError):
        print("Todays Stock Skus have not been generated yet")
        return 0

    try:
        print("\instock\storisSTOCK " + last_time + ".csv")
        yesterday = pd.read_csv(str(df.loc[0].epath) + "\showroomstock\warehouse " + last_time + ".csv")
        del yesterday['Quantity']
        yesterday = yesterday[~yesterday.Product.str.endswith("SO")]
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


def makeMessage(intoday, outtoday):
    """
    Creates the string for the message
    :param intoday:
    :param outtoday:
    :return:
    """
    message = "Good morning all,\n\n\tBelow is the stock changes for the last 24 hours, please confirm this information" \
              "as this is a new system and could have issues.\n"
    if len(intoday) != 0:
        message = message + "\nIn Stock Today:\n"
        for x in intoday:
            message = message + x + "\n"
    elif len(intoday) == 0:
        message = message + "\nNOTHING NEW IN STOCK TODAY\n"
    if len(outtoday) != 0:
        message = message + "\nOut of Stock Today:\n"
        print(len(outtoday))
        for x in outtoday:
            message = message + x + "\n"
    elif len(outtoday) == 0:
        message = message + "\nNOTHING NEW OUT OF STOCK TODAY"
    return message


def emailChanges(intoday, outtoday):
    """

    :return:
    """
    intoday = intoday['Product'].values.tolist()
    outtoday = outtoday['Product'].values.tolist()
    user = "dduffy385@gmail.com"
    pwd = "Pushthebutton8*"
    """ "gmanzek@rubygordon.com", "tmichaud@rubygordon.com" """
    FROM = "dduffy385@gmail.com"
    TO = ["dmd9042@gmail.com"]
    SUBJECT = "Daily Stock Update"
    TEXT = makeMessage(intoday, outtoday)

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, "".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print('Something went wrong...')
    return 0