import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from datetime import datetime


async def login():
    # getSessionIdHeaders = {
    #     "accept": "*/*",
    #     "accept-encoding": "gzip, deflate, br",
    #     "connection": "keep-alive",
    #     "cookie": "EUcomp=1",
    #     # "cookie":	"__ga.vipre.tune=GA1.3.1647441509.1702461365",
    #     # "cookie":	"__ga.vipre.tune_gid=GA1.3.168591006.1702461365",
    #     # "cookie":	"_gat_tune=1",
    #     # "cookie":	"__ga.vipre.tune_ga_Z9XNMSMFST=GS1.3.1702461364.1.1.1702461364.60.0.0",
    #     # "cookie":	"_dd_s=logs=1&id=7cd3a518-7e15-498e-8cb8-fb825fab275d&created=1702461362636&expire=1702462277468",
    #     # "cookie":	"swidth=1536",
    #     "Content-Type":	"application/x-www-form-urlencoded",
    # }
    getSessionIdHeaders = {
        'cookie': 'EUcomp=1',
        'content-type': 'application/x-www-form-urlencoded',
        'connection': 'keep-alive',
        "accept-encoding":	"gzip, deflate, br",
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    # getSessionIdPayload = '_method=POST&data%5B_Token%5D%5Bkey%5D=a18812cb90d4183e44a6fb33ba70e35b5fbf5428&data%5BUser%5D%5Bemail%5D=evenelson380df%40gmail.com&data%5BUser%5D%5Bpassword%5D=A61yIU8g4%21f%29&data%5B_Token%5D%5Bfields%5D=56b682232e568ff7c2e5968393c245234b610de2%253An%253A0%253A%257B%257D'
    getSessionIdPayload = {
        'data[User][email]': 'alishacooper125we@gmail.com',
        'data[User][password]': 'J9figOCIfbMICXB',
    }
    # Get session id
    async with aiohttp.ClientSession() as session:
        async with session.post('https://affiliate.vipre.com', data=json.dumps(getSessionIdPayload), headers=getSessionIdHeaders, allow_redirects=False) as response:
            responseCookies = response.cookies.get('PHPSESSID')
            sessionId = responseCookies.key + "=" + responseCookies.value
            print(sessionId)
            # sessionId = "PHPSESSID=620b9e8fffa69d6a329e1d1a86418aee"
    getTokenHeaders = {
        "Cookie": sessionId
    }
    print(getTokenHeaders)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://affiliate.vipre.com/publisher/', headers=getTokenHeaders) as response:
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
                print("Error extracting Session Token")
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
                print(response_json['response']['data']['data'])
            else:
                print("No 'response' attribute in the JSON content.")

    return

asyncio.run(login())
