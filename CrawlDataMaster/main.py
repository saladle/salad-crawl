# import requests
import pypeln as pl
import aiohttp
import asyncio
import xlsxwriter
from bs4 import BeautifulSoup
import json


BASE_URL = 'https://app.getreditus.com/login/'
EMAIL = 'staakerole@gmail.com'
PASSWORD = 'QqHzAXjVR8#uBBN'
OUTPUT_FILE = 'result.csv'


async def crawlDataMaster(args):
    base, loginRequestUrl, email, password = args
    if base == 'reditus':
        return await crawlDataReditus(loginRequestUrl, email, password)
    elif base == 'leaddyno':
        return await crawlDataLeaddyno(loginRequestUrl, email, password)
    elif base == 'iDevaffiliate':
        return await crawlDataIDevaffiliate(loginRequestUrl, email, password)


async def crawlDataReditus(loginRequestUrl, email, password):
    token = await getTokenReditus(loginRequestUrl, email, password)
    return await getDataReditus(token)


async def crawlDataLeaddyno(loginRequestUrl, email, password):
    return await getDataLeaddyno(loginRequestUrl, email, password)


async def crawlDataIDevaffiliate(loginRequestUrl, email, password):
    return await getDataIDevaffiliate(loginRequestUrl, email, password)


async def getTokenReditus(loginRequestUrl, email, password):
    payload = {
        "email": email,
        "password": password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(loginRequestUrl, data=payload) as response:
            return response.headers['Authorization']


async def getDataReditus(token):
    getDataApiUrl = 'https://api.getreditus.com/api/affiliate/dashboard/cards'
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(getDataApiUrl, headers=headers) as response:
            return await response.json()


async def getDataLeaddyno(loginRequestUrl, email, password):
    passwordPayload = {
        "ic-request": "true",
        "password": password,
        "email": email,
        "ic-id": 1,
        "ic-current-url": "/",
        "_method": "PUT"
    }
    emailPayload = {
        "ic-request": "true",
        "authenticity_token": "Y-q7cjhKtxJiV1OWgEXmLzEalbXKisCZzJsmy-VR5hcUkX77DdovO35KZWOe0bDS37F4FKU6ZjFn6e7XKN2AtA",
        "email": email,
        "ic-id": 1,
        "ic-current-url": "/",
        "_method": "PUT"
    }
    emailHeaders = {
        "Cookie": "_leaddyno_session=MmJLWTRGV3p0NzlaUEZyWnRjMjc1b3owdXVVUm9BVlorR0o3RUlJWk5kaE9PWHFySTh3NVd3a0FBbytsOGdRcEdqZlJsZmFvWk9MS0xkMk82REJpcWV0RXdnRHJGdS9QbEhGenN6TElYZmRuSzlqK1V4aUY1T3NkTFlIVHNla2JZME9LejBHMUd1d1FOdWxqcXdTTUpBPT0tLU5KUmcwcjIwUTA2UEtkbkgwWE9hYVE9PQ%3D%3D--bcd81b9ef7a6e060e01f7615d789a486a7d1b94f",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(loginRequestUrl, data=emailPayload, headers=emailHeaders) as response:
            emailResponseToken = response.headers['Set-Cookie']

    passwordHeaders = {
        # "Accept": "text/html-partial, */*; q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": emailResponseToken,
        # "Origin": "https://tradelle.leaddyno.com",
        # "Referer": "https://tradelle.leaddyno.com/",
        # "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        # "Sec-Ch-Ua-Mobile": "?0",
        # "Sec-Ch-Ua-Platform": "\"Windows\"",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        # "X-Http-Method-Override": "PUT",
        # "X-Ic-Request": "true",
        # "X-Requested-With": "XMLHttpRequest"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(loginRequestUrl, data=passwordPayload, headers=passwordHeaders) as response:
            passwordResponseToken = response.headers['Set-Cookie']

    getInfoHeaders = {
        ":method": "GET",
        ":authority": "tradelle.leaddyno.com",
        ":scheme": "https",
        ":path": "/affiliate",
        # "sec-ch-ua": "Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://tradelle.leaddyno.com/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cookie": passwordResponseToken,
        "if-none-match": "W/'2fc70b5ebd7a45aad667e0be52dbb996'",
    }
    dataRequestUrl = loginRequestUrl.replace('/sso', '/affiliate')
    async with aiohttp.ClientSession() as session:
        async with session.get(dataRequestUrl, headers={**getInfoHeaders}, allow_redirects=False) as response:
            content = await response.read()  # Read the response content as bytes
            # Decode the bytes to a string
            pageSource = content.decode('utf-8')
            soup = BeautifulSoup(pageSource, "html.parser")
            results = soup.select(".aff-progress-digit>b")
            resultsContent = [int(element.text) for element in results]
            result_dict = {}
            if (len(resultsContent) > 0):
                result_dict = {
                    'Friends have visited us': resultsContent[0], 'Friends have signed up with us': resultsContent[1], 'Purchases made by friends': resultsContent[2]}
            return result_dict


async def getDataIDevaffiliate(loginRequestUrl, email, password):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = f'csrf_token=&userid={email}&password={
        password}&token_affiliate_login=2eed4d63883d9ed92399'
    async with aiohttp.ClientSession() as session:
        async with session.post(loginRequestUrl, data=payload, headers=headers) as response:
            content = await response.read()  # Read the response content as bytes
            # Decode the bytes to a string
            pageSource = content.decode('utf-8')
            soup = BeautifulSoup(pageSource, "html.parser")
            results = soup.select(".heading")
            resultsContent = [element.text.strip() for element in results]
            lastElement = resultsContent[len(resultsContent) - 1]
            twoLastElement = lastElement.replace(" ", "").split('\n\n')
            resultsContent.pop()
            resultsContent = resultsContent + twoLastElement
            if (len(resultsContent) > 0):
                result_dict = {
                    'Total Transactions': resultsContent[0], 'Current Earnings': resultsContent[1], 'Total Earned To Date': resultsContent[2], 'Unique Visitors': resultsContent[3], 'Sales Ratio': resultsContent[4]}
            return result_dict


async def main():
    data = [
        ('reditus', 'https://api.getreditus.com/auth/sign_in',
         'alishacooper125we@gmail.com', 'sB"K3??9^8;n'),
        ('reditus', 'https://api.getreditus.com/auth/sign_in',
         'staakerole@gmail.com', 'QqHzAXjVR8#uBBN'),
        ('leaddyno', 'https://cramly.leaddyno.com/sso',
         'teamasmads@gmail.com', 'yqZWRKe6hrYmS4u'),
        ('leaddyno', 'https://tradelle.leaddyno.com/sso',
         'teamasmads@gmail.com', '2fijD4FNfM4Z@pj'),
        ('iDevaffiliate', 'https://affiliate.hide-my-ip.com/login.php',
         'beckyanderson23g', 'CqA5v9BvI6J0'),
        ('iDevaffiliate', 'https://affiliate.simplybook.me/login.php',
         'emilymurphy965df', 'L4AYLVa97S'),
    ]
    results = await pl.task.map(crawlDataMaster, data, workers=100)
    print(results)

asyncio.run(main())
