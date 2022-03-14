"""
websiteLink
Author: Daniel Duffy
Company: Ruby Gordon Furniture
This python script for the current moment will function as a backend helper to connect
STORIS with furnituredealer.net. It will accomplish this by making a copy of the database and then
using the copy to scrape data, one finished with the scrape this program will delete the copy. The end result
of this will be a .csv file to feed information to the back end of our website for inventory
"""
#!/usr/bin/env python3
import sys
import time
import datetime
import os
import colorama
import pyautogui as pg
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from termcolor import colored

import pandas as pd
pd.options.mode.chained_assignment = None


def initilizeSTORIS():
    """
    This will ensure STORIS is set up and on the report page
    :return:
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    print(colored("\t->Ensure STORIS is logged on to a user who have the privileges to run a report", 'blue'))
    width, height = pg.size()
    pg.moveTo(width / 2, height / 2)
    pg.moveTo((width / 2) - 400, height - 25)  # Screen position for STORIS
    pg.click()
    print(colored("Logging into communication server...", 'yellow'))
    time.sleep(5)
    pg.write('sales')
    pg.press('enter')
    print(colored("Logging into STORIS with stored info...", 'yellow'))
    time.sleep(5)
    pg.write(str(df.loc[0].user))
    pg.press('tab')
    pg.write(str(df.loc[0].password))
    pg.press('tab')
    pg.write('10')
    pg.press('tab')
    pg.press('enter')
    print(colored("Putting STORIS in background...", 'yellow'))
    time.sleep(1)
    pg.moveTo((width / 2) - 400, height - 25)  # Screen position for STORIS
    pg.click()
    time.sleep(1)
    return 0


def cleanUpGui():
    """
    Initialize can run rouge and mess up the rest of the program this will close STORIS and initialize again
    :return: Nothing
    """
    width, height = pg.size()
    print(colored("\nCLOSING STORIS...", 'red'))
    pg.moveTo((width / 2) - 400, height - 24)  # Screen position for STORIS
    pg.rightClick()
    pg.moveRel(0,-25)
    pg.click()
    time.sleep(.5)
    pg.moveTo((width / 2) + 607, (height/2) - 385)  # Screen position for End Button STORIS
    pg.click()
    time.sleep(3)
    initilizeSTORIS()
    return 0


def runReport():
    """
    Runs the two reports needed utilizing pyautogui to mimic a human pulling it
    :return: Nothing
    """
    width, height = pg.size()
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    pg.moveTo((width / 2) - 400, height - 25)  # Screen position for STORIS
    pg.click()
    print(colored("Running ONHAND Report...", 'yellow'))
    pg.moveTo((width / 2) - 550, height / 2 - 68)  # Screen position for run report
    pg.click()
    pg.click()
    time.sleep(3)
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.write('onhand')
    pg.press('tab')
    pg.press('enter')
    time.sleep(3)
    pg.press('enter')
    print(colored("ONHAND Exporting:", 'cyan'))
    for x in range(df.loc[0].delay, 0, -1):
        print(colored("\t->Waiting " + str(x) + " seconds...", 'yellow'))
        time.sleep(1)

    print(colored("\n\t->ONHAND Report Generated Successfully\n", 'green'))
    pg.press('esc')
    time.sleep(1.5)
    pg.moveTo((width / 2) - 400, height - 25)  # Screen position for STORIS
    pg.click()
    pg.click()
    print(colored("Running FDNEX1 Report...", 'yellow'))
    pg.moveTo((width / 2) - 550, height / 2 - 68)  # Screen position for run report
    pg.click()
    pg.click()
    time.sleep(3)
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.write('fdnexport1')
    pg.press('tab')
    pg.press('enter')
    time.sleep(1.5)
    pg.press('enter')
    time.sleep(1)
    print(colored("FDNEX Exporting:", 'cyan'))
    for x in range(df.loc[0].delay, 0, -1):
        print(colored("\t->Waiting " + str(x) + " seconds...", 'yellow'))
        time.sleep(1)

    print(colored("\n\t->FDNEX1 Report Generated Successfully\n", 'green'))
    pg.press('esc')
    print(colored("Placing STORIS in the background...", 'yellow'))
    time.sleep(2)
    return 0


def scrapeFiles(autoRun):
    """
    Grabs the raw file and parse it into the global list of Pieces
    fileName (String) - Filename holding the raw data to be opened and scraped
    :return: Nothing
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    onhandxlsx = str(df.loc[0].rpath + '\ONHAND.xlsx')
    onhandcsv = str(df.loc[0].rpath + '\ONHAND.csv')
    fdnexxlsx = str(df.loc[0].rpath + '\FDNEX1.xlsx')
    fdnexcsv = str(df.loc[0].rpath + '\FDNEX1.csv')
    runit = True
    print(colored("Attempting to collect data from STORIS...", 'yellow'))
    try:
        onhand = pd.read_excel(onhandxlsx)
        onhand.to_csv(onhandcsv, index=None, header=True)
        onhand = onhand.dropna(how='all')  # how="all" only deletes the FULLY empty rows
    except (FileNotFoundError, PermissionError):
        print(colored("ERROR:  " + str(onhandxlsx) + " NOT FOUND OR IS IN USE", 'red'))
        runit = False
    try:
        fdnex = pd.read_excel(fdnexxlsx)
        fdnex.to_csv(fdnexcsv, index=None, header=True)
        fdnex = fdnex.dropna(how='all')  # how="all" only deletes the FULLY empty rows
        print(colored("Deleting all empty rows...", 'yellow'))
    except (FileNotFoundError, PermissionError):
        print(colored("ERROR:  " + str(fdnexxlsx) + " NOT FOUND OR IS IN USE", 'red'))
        runit = False
    if runit:
        mainFileHandle(onhand, fdnex)
    return 0


def deleteFiles():
    """
    Deletes all the old files to clean out the pipeline and avoid any memory issues
    :return: Nothing
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    os.remove(str(df.loc[0].rpath) + "\FDNEX1.csv")
    os.remove(str(df.loc[0].rpath) + "\ONHAND.csv")
    os.remove(str(df.loc[0].rpath) + "\FDNEX1.xlsx")
    os.remove(str(df.loc[0].rpath) + "\ONHAND.xlsx")
    return 0


def getLocations(row, fdnex):
    """
    Returns a list of Locations for a sku
    :param sku: The Store SKU for the item
    :return: a list of integers for location of item
    """

    locations = []
    fdnex2 = fdnex.loc[fdnex['Product'] == row].Whse.values.tolist()
    [locations.append(x) for x in fdnex2 if x not in locations]
    locations2 = []
    for item in locations:
        locations2.append(str(int(item)))
    locations2 = ",".join(locations2)
    return locations2


def salesInStockMR(onhand):
    """
    Takes the merged onhand report from mainFileHandle and compares it to the days before and sends an email
    with items that went out of stock and items that came into stock
    :param onhand: The dataframe made from onhand
    :return: Nothing
    """
    return 0


def mainFileHandle(onhand, fdnex):
    """
    Handles all of the functionality for reading the datafiles and preparing them for class instancing
    :param onhand:
    :param fdnex:
    :return:
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    current_time = datetime.datetime.now()
    print(colored("Deleting all un-needed locations", 'yellow'))
    fdnex = fdnex[(fdnex.Whse == 10) | (fdnex.Whse == 12) | (fdnex.Whse == 88) | (fdnex.Product == '.*-SO')]
    print(colored("Creating Net Available", 'yellow'))
    onhand['Net Available'] = onhand['Qty On Hand'] - onhand['Qty Resvd']
    print(colored("Deleting all not in stock items...", 'yellow'))
    print(colored("Finding locations for in stock items...", 'yellow'))
    onhand['Location'] = onhand.apply(lambda row: getLocations(row.Product, fdnex), axis=1)
    onhand['Location'].replace('', None, inplace=True)
    onhand.dropna(subset=['Location'], inplace=True)
    getLocations("18SUV5-CH", fdnex)

    SKUs = onhand.pop('Product')
    VendMod = onhand.pop('Vend Mod')
    one = onhand.pop('Description')
    two = onhand.pop('Vend')
    three = onhand.pop('Sell Price')
    onhand1 = onhand.pop('Suggested Retail')
    five = onhand.pop('Qty On Hand')
    six = onhand.pop('Qty Unresvd')
    seven = onhand.pop('Qty Resvd')
    eight = onhand.pop('Net Available')
    nine = onhand.pop('Location')
    #Reorganizing Dataframe
    onhand['Product'] = SKUs
    onhand['Vend Mod'] = VendMod
    onhand['Description'] = one
    onhand['Vend'] = two
    onhand['Sell Price'] = three
    onhand['Suggested Retail'] = three
    onhand['Qty On Hand'] = five
    onhand['Qty Unresvd'] = six
    onhand['Qty Resvd'] = seven
    onhand['Net Available'] = eight
    onhand['Location'] = nine
    onhand['MSRP'] = onhand1
    onhand.replace('"', '', regex=True)
    #onhand.sort_values('Product')
    print(
        colored("Attempting to export Website Backend to file location (" + str(df.loc[0].epath) + "\storis " + str(current_time.month)
                + "." + str(current_time.day) + "." + str(current_time.year)[2:4] + ".csv" + ")...", 'yellow'))
    try:
        onhand.to_csv(str(df.loc[0].epath) + "\storis " + str(current_time.month) + "." + str(current_time.day)
                      + "." + str(current_time.year)[2:4] + ".csv", encoding='utf-8', index=False)
        print(colored("\t->File created successfully!\n", 'green'))
        # print(onhand) This prints the DataFrame may keep this for an option in settings
        print(colored("Attempting to export in stock SKUs to file location (" + str(df.loc[0].epath) + "\instock\storisSTOCK " + str(current_time.month)
                + "." + str(current_time.day) + "." + str(current_time.year)[2:4] + ".csv" + ")...", 'yellow'))
        SKUs.to_csv(str(df.loc[0].epath) + "\storisSTOCK " + str(current_time.month) + "." + str(current_time.day)
                      + "." + str(current_time.year)[2:4] + ".csv", encoding='utf-8', index=False)
        print(colored("\t->File created successfully!\n", 'green'))
        deleteFiles()
    except PermissionError:
        print(colored("\nERROR: CANNOT SAVE THIS FILE IS CURRENTLY IN USE WITH ANOTHER APPLICATION", 'red'))
        print(colored("Returning to Main Menu in: 5", 'red'))
        for x in range(4, 0, -1):
            print("                           " + colored(str(x), 'red'))
            time.sleep(1)
    return 0


def websiteUploader():
    """
    Uploads the 'storis xx.xx.xx' file for the current day to the backend of the Ruby Gordon client fac ing website
    :return: Nothing
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent) + '\settings.csv')
    rgBackend = "https://admin.furnituredealer.net/login.aspx"
    current_time = datetime.datetime.now()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.implicitly_wait(0.5)
    driver.get(rgBackend)
    username = driver.find_element(by=By.ID, value="UserNameText")
    password = driver.find_element(by=By.ID, value="PasswordText")
    username.send_keys("dduffy@rubygordon.com")
    password.send_keys("Pushthebutton8*")
    driver.find_element(by=By.ID, value="LoginButton").click()
    driver.get("https://admin.furnituredealer.net/merchandisingtools/integration/import.aspx?dealerid=117")
    driver.find_element(by=By.XPATH, value="//*[@id='ctl00_MainContent_UploadOptionsContainer']/div[1]/div/div[1]").click()
    s = driver.find_element(by=By.XPATH, value="//*[@id='ctl00_MainContent_FileUpload']")
    s.send_keys((str(df.loc[0].epath) + "\storis " + str(current_time.month)
                + "." + str(current_time.day) + "." + str(current_time.year)[2:4] + ".csv"))
    time.sleep(.5)
    driver.find_element(by=By.NAME, value="ctl00$MainContent$ctl00").click()
    driver.close()
    return 0


def closeSTORIS():
    """

    :return:
    """
    width, height = pg.size()
    pg.moveTo((width / 2) - 400, height - 24)  # Screen position for STORIS
    pg.rightClick()
    pg.moveRel(0, -25)
    pg.click()
    return 0


def fullWebsiteUpdate():
    """

    :return:
    """
    initilizeSTORIS()
    runReport()
    scrapeFiles(True)
    websiteUploader()
    closeSTORIS()
    return 0


def runLogic():
    """
    Grabbing from settings this will iterate the mainFileHandle function by the time established in the file
    :param onhand:
    :param fdnex:
    :return: Nothing
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    loop = True
    while loop:
        cleanUpGui()
        time.sleep(1)
        runReport()
        scrapeFiles(True)
        websiteUploader()
        print(colored("Waiting for set delay (Press ctrl + c to go to main menu): ", 'cyan'))
        for x in range(int(df.loc[0].time), 0, -1):
            print(colored("\t->Waiting " + str(x) + " seconds...", 'yellow'))
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print(colored("\nINPUT RECEIVED RETURNING TO MAIN MENU\n     ->An email has been sent out to the "
                              "administrator of this software\n     ->Please ensure all your settings are correct"
                              "\n     ->Remember to initialize before running again\n", 'red'))
                loop = False
                break

    return 0


def cleanRestartSettings():
    """
    Deletes and recreates the settings.csv file fresh
    :return: Nothing
    """
    df = pd.DataFrame(columns=['rpath', 'epath', 'user', 'password', 'time','delay'])
    df.loc[0] = ["D:\Graphite Solutions LLC\STORIS\Exports", "D:\Graphite Solutions LLC\STORIS", "DMD", "1234", 15, 45]
    df.to_csv(str(Path(__file__).resolve().parent)+'\settings.csv', encoding='utf-8', index=False)
    return 0


def editSettings():
    """
    Edit the settings of the API including where to save the files/where to find the files, user log in for STORIS,
    time iteration length
    :return: Nothing
    """
    df = pd.read_csv(str(Path(__file__).resolve().parent)+'\settings.csv')
    print("Report Path:          " + str(df.loc[0].rpath) + "\nExport Path:          " + str(df.loc[0].epath) +
          "\nSTORIS User:          " + str(df.loc[0].user) + "\nSTORIS Password:      " + str(df.loc[0].password) +
          "\nTime between website reports(Seconds):   " + str(df.loc[0].time) +
          "\nTime between STORIS reports(Seconds):   " + str(df.loc[0].delay) + "\n")
    selection = input("Edit Settings (Y/n): ")
    edited = [0, 0, 0, 0, 0, 0]
    if selection == 'Y':
        selection2 = input("Clean and restart file (Y/n): ")
        if selection2 == 'Y':
            cleanRestartSettings()
        else:
            edited[0] = input("Please enter the STORIS report filepath: ")
            edited[1] = input("Please enter the website backend filepath: ")
            edited[2] = input("Please enter STORIS username: ")
            edited[3] = input("Please enter STORIS password: ")
            edited[4] = input("Please enter the time between auto runs(Seconds): ")
            edited[5] = input("Please enter the delay for STORIS reports to export(Seconds): ")
            df.loc[0] = edited
            df.to_csv(str(Path(__file__).resolve().parent)+'\settings.csv', encoding='utf-8', index=False)
            editSettings()
    elif selection == 'n':
        print("\nReturning to Main Menu")
    else:
        print(colored("Unknown character!", 'red'))
    return 0


def help(firstTime):
    """
    Displays the help text and later will include ability to read more documentation
    :return: Nothing
    """
    if firstTime:
        print("For first time use please ensure the following steps are followed:\n"
              "\t->Ensure setting has the correct file paths, username, password, and time delay\n"
              "\t->STORIS is installed on the machine as in pinned to the second spot from the left\n"
              "\t\t->Additionally ensure user has correct privileges for running reports\n"
              + colored("\t->IF YOU START AN AUTO RUN (LIVE) INSTANCE YOU WILL NEED TO EXIT OUT OF THE APPLICATION"
                        "AND RESTART THE STORIS API IF YOU NEED TO ACCESS THE MENU", 'red'))
    else:
        print(colored("Initialize Program",'yellow')+": This will ensure that STORIS is open and prepared for the Auto run functionality \n"
              + colored("Run Auto Program",'yellow')+": This will automatically run the website backend report pulling from STORIS,\n\t\t running"
              " automatically depending on the time setting (minutes)\n"+colored("Manual STORIS Report",'yellow')+": This will use STORIS to "
              "manually once generate the raw reports(NO AUTO)\n"+colored("Export Single Report",'yellow')+": This will run only one "
              "website backend in-stock report based on the STORIS exports(NO AUTO) \n"+colored("Clean up GUI",'yellow')+": Shuts down STORIS "
              "and signs back in with user saved data\n"+colored("Settings",'yellow')+": This will allow you to edit\n"
              "\t\t ->where the program is getting the reports from STORIS\n"
              "\t\t ->Where it is exporting the file for the backend of the website\n"
              "\t\t ->The username for STORIS\n"
              "\t\t ->The password for STORIS\n"
              "\t\t ->The time wait for STORIS\n"
              + colored("First Time", 'yellow') + ": Gives users an idea how to use STORIS API for the first time\n"
              + colored("Help", 'yellow') + ": Gives users an information on different uses of STORIS API\n"
              + colored("Quit",'red')+": Will exit the program\n")
    input("Enter any key to go back to the main menu: ")
    return 0


def main():
    """

    :return:
    """
    x = 0
    last_time = time.time()
    while True:
        if x == 0:
            selection = input(
                "\n    " + colored("Welcome to STORIS API", 'yellow') + "\n\n ---------------------------\n"
                "          " + (colored("MAIN MENU",'cyan')) + "\n ---------------------------\n\nI: Initialize Program\n"
                "R: Run Auto Program\nE: Export Single Report\nM: Manual STORIS Report\nW: Website Upload\nU: Update Website\nC: Clean up STORI\nS: Settings"
                "\nF: First Time\nH: Help\nQ: Quit\n>>")
        else:
            selection = input("\n ---------------------------\n          " + (colored("MAIN MENU", 'cyan')) +
                              "\n ---------------------------\n\nI: Initialize Program\nR: Run Auto Program"
                              "\nE: Export Single Report\nM: Manual STORIS Report\nW: Website Upload\nU: Update Website\nC: Clean up STORIS\nS: Settings"
                              "\nF: First Time\nH: Help\nQ: Quit\n>>")
        if selection == "Q" or selection == "q":
            print("\nQuitting")
            break

        elif selection == "I" or selection == "i":
            print(colored("\nInitializing STORIS API...", 'green'))
            initilizeSTORIS()

        elif selection == "R" or selection == "r":
            warning = input(
                colored("->IF YOU START AN AUTO RUN (LIVE) INSTANCE YOU WILL NEED TO EXIT OUT OF THE APPLICATION"
                        " AND RESTART THE STORIS API IF YOU NEED TO ACCESS THE MENU\n", 'red') +
                colored("Do you wish to continue(Y/n): ", 'blue')
            )
            if warning == 'Y':
                print(colored("\nRunning STORIS API...", 'yellow'))
                runLogic()
            elif warning == 'y':
                print(colored("Please use Capitalization to confirm you wish to continue", 'yellow'))
            else:
                pass

        elif selection == "S" or selection == "s":
            print(colored("\nSettings for STORIS API...\n", 'blue'))
            editSettings()

        elif selection == "F" or selection == "f":
            print(colored("\nfor first time use STORIS API...\n", 'blue'))
            help(True)

        elif selection == "W" or selection == "w":
            print(colored("\nStarting Website Uploader...\n", 'blue'))
            websiteUploader()

        elif selection == "U" or selection == "u":
            print(colored("\nRunning full webiste update...\n", 'blue'))
            fullWebsiteUpdate()

        elif selection == "H" or selection == "h":
            print(colored("\n\t\t\t\tHelp for STORIS API\n"
                          "\t-----------------------------------------------------------------------------------\n",
                          'blue'))
            help(False)

        elif selection == "C" or selection == "c":
            print(colored("\nCleaning STORIS API...\n", 'yellow'))
            cleanUpGui()

        elif selection == "E" or selection == "e":
            print(colored("\nExporting single report...\n", 'yellow'))
            scrapeFiles(False)

        elif selection == "M" or selection == "m":
            print(colored("\nRunning STORIS Reports...\n", 'yellow'))
            runReport()

        elif selection == "T" or selection == "t":
            print(colored("\n\t->Resetting Settings.csv...\n", 'blue'))
            cleanRestartSettings()

        else:
            print(colored("ERROR: Character not supported", 'red'))

        x = x + 1

    return 0


if __name__ == '__main__':
    """
    This is the main logic for this program
    For the moment this will be a command line based program, after working with the end users i will attempt to 
    create a GUI for this application
    """
    colorama.init()
    main()

