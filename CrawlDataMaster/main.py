# import requests
import pypeln as pl
import aiohttp
import asyncio
import xlsxwriter
from bs4 import BeautifulSoup
import json
from datetime import datetime


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
    elif base == 'hasoffers':
        return await crawlDataHasoffers(loginRequestUrl, email, password)
    elif base == 'contadu':
        return await crawlDataContadu(loginRequestUrl, email, password)


async def crawlDataReditus(loginRequestUrl, email, password):
    token = await getTokenReditus(loginRequestUrl, email, password)
    return await getDataReditus(token)


async def crawlDataLeaddyno(loginRequestUrl, email, password):
    return await getDataLeaddyno(loginRequestUrl, email, password)


async def crawlDataIDevaffiliate(loginRequestUrl, email, password):
    return await getDataIDevaffiliate(loginRequestUrl, email, password)


async def crawlDataHasoffers(loginRequestUrl, email, password):
    return await getDataHasoffers(loginRequestUrl, email, password)


async def crawlDataContadu(loginRequestUrl, email, password):
    return await getDataContadu(loginRequestUrl, email, password)


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


async def getDataHasoffers(loginRequestUrl, email, password):
    getSessionIdHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding":	"gzip, deflate, br",
        "connection": "keep-alive",
        "cookie":	"EUcomp=1",
        "content-type":	"application/x-www-form-urlencoded",
    }
    # getSessionIdPayload = '_method=POST&data%5B_Token%5D%5Bkey%5D=a18812cb90d4183e44a6fb33ba70e35b5fbf5428&data%5BUser%5D%5Bemail%5D=evenelson380df%40gmail.com&data%5BUser%5D%5Bpassword%5D=A61yIU8g4%21f%29&data%5B_Token%5D%5Bfields%5D=56b682232e568ff7c2e5968393c245234b610de2%253An%253A0%253A%257B%257D'
    getSessionIdPayload = {
        'data[User][email]': email,
        'data[User][password]': password,
    }
    # Get session id
    async with aiohttp.ClientSession() as session:
        async with session.post(loginRequestUrl, data=getSessionIdPayload, headers=getSessionIdHeaders, allow_redirects=False) as response:
            responseCookies = response.cookies.get('PHPSESSID')
            sessionId = responseCookies.key + "=" + responseCookies.value

    getTokenHeaders = {
        "Cookie": sessionId
    }
    getTokenUrl = loginRequestUrl + 'publisher/'
    async with aiohttp.ClientSession() as session:
        async with session.get(getTokenUrl, headers=getTokenHeaders) as response:
            content = await response.read()
            pageSource = content.decode('utf-8')
            soup = BeautifulSoup(pageSource, "html.parser")
            try:
                script_tag = soup.find(
                    'script', text=lambda t: 'session_token' in t)
                if script_tag:
                    # Extract the session_token value from the script tag
                    session_token = script_tag.text.split(
                        '"session_token":"')[1].split('",')[0]

                    print("Session Token:", session_token)
                else:
                    print("Session Token not found.")
            except:
                print("Hasoffers: Error extracting Session Token")
                return

    # Get data
    getDataPayload = {
        "fields[]": ["Stat.impressions", "Stat.clicks", "Stat.conversions", "Stat.payout"],
        "Method": "getStats",
        "NetworkId": "vipre",
        "SessionToken": session_token,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api-p03.hasoffers.com/v3/Affiliate_Report.json', data=getDataPayload) as response:
            content = await response.text()
            response_json = json.loads(content)
            if 'response' in response_json:
                # print(response_json['response']['data']['data'][0]['Stat'])
                return response_json['response']['data']['data']
            else:
                print("Has offer: No 'response' attribute in the JSON content.")


async def getDataContadu(loginRequestUrl, email, password):
    # Get session id
    getSessionIdPayload = {
        "email": email,
        "password": password,
        "redirect_url": "/"
    }
    completeLoginRequestUrl = loginRequestUrl + 'login'
    async with aiohttp.ClientSession() as session:
        async with session.post(completeLoginRequestUrl, data=getSessionIdPayload, allow_redirects=False) as response:
            responseCookies = response.cookies.get('contai_session_id')
            sessionId = responseCookies.key + "=" + responseCookies.value
    # Get data
    getDataHeader = {
        "Cookie": sessionId
    }
    getDataUrl = loginRequestUrl + 'affiliate'
    async with aiohttp.ClientSession() as session:
        async with session.get(getDataUrl, headers=getDataHeader) as response:
            content = await response.read()
            pageSource = content.decode('utf-8')
            soup = BeautifulSoup(pageSource, "html.parser")
            data = []
            for row in soup.select('table[data-export_fname="aff_daily_stats"] tbody tr'):
                date = row.select('td')[0].text.strip()
                clicks = row.select('td')[1].text.strip()
                unique_ips = row.select('td')[2].text.strip()
                entry = {'date': date, 'clicks': clicks,
                         'unique IPs': unique_ips}
                data.append(entry)
    return data


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
        ('hasoffers', 'https://affiliate.vipre.com/',
         'evenelson380df@gmail.com', 'A61yIU8g4!f)'),
        ('hasoffers', 'https://affiliate.vipre.com/',
         'alishacooper125we@gmail.com', 'J9figOCIfbMICXB'),
        ('hasoffers', 'https://affiliate.vipre.com/',
         'asmlongle@gmail.com', 'tj5kLv2dNmZgZ!f'),
        ('contadu', 'https://app.neuronwriter.com/ucp/',
         'eleanorlewis676rsdf@gmail.com', 'C9xvPC$SCcU;6~V'),
    ]
    results = await pl.task.map(crawlDataMaster, data, workers=100)
    print(results)

asyncio.run(main())
