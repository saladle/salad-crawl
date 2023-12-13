# Task 2

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# import requests # TODO: aiohttp hỗ trợ bất đồng bộ
# https://cgarciae.github.io/pypeln/
import csv
import asyncio

import xlsxwriter

BASE_URL = 'https://app.getreditus.com/login/'
EMAIL = 'staakerole@gmail.com'
PASSWORD = 'QqHzAXjVR8#uBBN'
OUTPUT_FILE = 'result.csv'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)

maxWaitTime = WebDriverWait(driver, 10)
emailInput = maxWaitTime.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
emailInput.send_keys(EMAIL)
passwordInput = maxWaitTime.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
passwordInput.send_keys(PASSWORD)
signInBtn = maxWaitTime.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
signInBtn.click()

sleep(5)
# getLocalStorageScript = "localStorage.getItem('session');"
getLocalStorageScript = "window.localStorage;"
# token = driver.execute_script("localStorage.getItem('session');")
try:
    # token = driver.execute_script(getLocalStorageScript)
    token = driver.execute_script("return localStorage.getItem('session');")
    print("Token:", token)
except Exception as e:
    print("Error:", e)

workbook = xlsxwriter.Workbook("Result.xlsx")
async def getGeneralData():
    getDataApiUrl = 'https://api.getreditus.com/api/affiliate/dashboard/cards'
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    response = requests.get(getDataApiUrl, headers=headers)
    if response.status_code == 200:
        data = response.json()
        headers = list(data.keys())
        values = list(data.values())

        worksheet = workbook.add_worksheet("General Data")
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col += 1
        row += 1
        col = 0
        for value in values:
            worksheet.write(row, col, value)
            col += 1

        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow(data)
    else:
        print(f"API request failed with status code: {response.status_code}")

async def getReferralEvent():
    getDataApiUrl = 'https://api.getreditus.com/api/affiliate/dashboard/referrals_timeline?start_date=2023-10-30&end_date=2023-11-29' # Xử lý ngày dựa theo ngày hôm nay
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(getDataApiUrl, headers=headers)
    if response.status_code == 200:
        data = response.json()
        headers = list(data.keys())
        # values = list(data.values())
        print(data)
        # print(headers)
        # print(values)

        worksheet = workbook.add_worksheet("Referral Events")
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col += 2
        row += 1
        col = 0
        for row_num, row_data in enumerate(data, start=1):
            for col_num, col_data in enumerate(row_data.values()):
                worksheet.write(row_num, col_num, col_data)

        # with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=headers)
        #     writer.writeheader()
        #     writer.writerow(data)
    else:
        print(f"API request failed with status code: {response.status_code}")

async def getReferralStatus():
    getDataApiUrl = 'https://api.getreditus.com/api/affiliate/dashboard/referral_status?start_date=2023-10-30&end_date=2023-11-29'   
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    response = requests.get(getDataApiUrl, headers=headers)
    if response.status_code == 200:
        data = response.json()
        headers = list(data.keys())
        values = list(data.values())

        worksheet = workbook.add_worksheet("Referral Status")
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col += 1
        row += 1
        col = 0
        for value in values:
            worksheet.write(row, col, value)
            col += 1

        # with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=headers)
        #     writer.writeheader()
        #     writer.writerow(data)
    else:
        print(f"API request failed with status code: {response.status_code}")

async def getPartnerships():
    getDataApiUrl = 'https://api.getreditus.com/api/affiliate/partnerships?page=1&per_page=20&state=&customer_id=' #TODO: Xử lý khi có nhiều hơn 20 bản ghi
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    response = requests.get(getDataApiUrl, headers=headers)
    if response.status_code == 200:
        data = response.json()
        partnerShips = data["partnerships"]
        headers = list(partnerShips[0].keys())
        values = list(partnerShips[0].values())

        worksheet = workbook.add_worksheet("My Partnerships")
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col += 1
        row += 1
        col = 0
        for row_num, row_data in enumerate(partnerShips, start=1):
            for col_num, col_data in enumerate(row_data.values()):
                worksheet.write(row_num, col_num, col_data)

        # for value in values:
        #     worksheet.write(row, col, value)
        #     col += 1

        # with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        #     # writer = csv.DictWriter(csvfile, fieldnames=headers)
        #     writer = csv.DictWriter(csvfile, fieldnames=[])
        #     writer.writeheader()
        #     writer.writerow(data)
    else:
        print(f"API request failed with status code: {response.status_code}")

async def asynchronousTask():
    await asyncio.gather(getGeneralData(), getReferralEvent(), getReferralStatus(), getPartnerships())

asyncio.run(asynchronousTask())
workbook.close()
driver.quit()