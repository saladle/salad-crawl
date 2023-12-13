import aiohttp
import asyncio
from bs4 import BeautifulSoup

passwordPayload = {
    "ic-request": "true",
    "password": "2fijD4FNfM4Z@pj",
    "email": "teamasmads@gmail.com",
    "ic-id": 1,
    "ic-current-url": "/",
    "_method": "PUT"
}
emailPayload = {
    "ic-request": "true",
    "authenticity_token": "Y-q7cjhKtxJiV1OWgEXmLzEalbXKisCZzJsmy-VR5hcUkX77DdovO35KZWOe0bDS37F4FKU6ZjFn6e7XKN2AtA",
    "email": "teamasmads@gmail.com",
    "ic-id": 1,
    "ic-current-url": "/",
    "_method": "PUT"
}


async def login():
    # emailHeaders = {
        # "Accept": "text/html-partial, */*; q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "_leaddyno_session=MmJLWTRGV3p0NzlaUEZyWnRjMjc1b3owdXVVUm9BVlorR0o3RUlJWk5kaE9PWHFySTh3NVd3a0FBbytsOGdRcEdqZlJsZmFvWk9MS0xkMk82REJpcWV0RXdnRHJGdS9QbEhGenN6TElYZmRuSzlqK1V4aUY1T3NkTFlIVHNla2JZME9LejBHMUd1d1FOdWxqcXdTTUpBPT0tLU5KUmcwcjIwUTA2UEtkbkgwWE9hYVE9PQ%3D%3D--bcd81b9ef7a6e060e01f7615d789a486a7d1b94f",
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
    # }
    # async with aiohttp.ClientSession() as session:
    #     async with session.post('https://tradelle.leaddyno.com/sso', data=emailPayload, headers=emailHeaders) as response:
    #         emailResponseToken = response.headers['Set-Cookie']

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
        async with session.post('https://tradelle.leaddyno.com/sso', data=passwordPayload, headers=passwordHeaders) as response:
            token = response.headers
            passwordResponseToken = response.headers['Set-Cookie']

    getInfoHeaders = {
        # ":method": "GET",
        # ":authority": "tradelle.leaddyno.com",
        # ":scheme": "https",
        # ":path": "/affiliate",
        # # "sec-ch-ua": "Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "Windows",
        # "upgrade-insecure-requests": "1",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        # "sec-fetch-site": "same-origin",
        # "sec-fetch-mode": "navigate",
        # "sec-fetch-user": "?1",
        # "sec-fetch-dest": "document",
        # "referer": "https://tradelle.leaddyno.com/",
        # "accept-encoding": "gzip, deflate, br",
        # "accept-language": "en-US,en;q=0.9",
        "cookie": passwordResponseToken,
        # "if-none-match": "W/'2fc70b5ebd7a45aad667e0be52dbb996'",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://tradelle.leaddyno.com/affiliate', headers={**getInfoHeaders}, allow_redirects=False) as response:
            content = await response.read()  # Read the response content as bytes
            pageSource = content.decode('utf-8')  # Decode the bytes to a string
            soup = BeautifulSoup(pageSource, "html.parser")
            a = soup.select(".aff-progress-digit>b")
            # a = soup.find_all(class_="aff-progress-digit")
            print('Result: ', a)
            values = [int(element.text) for element in a]
            print('Values: ', values)


asyncio.run(login())
