import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def login():
    # Get session id
    # getSessionIdPayload = 'email=eleanorlewis676rsdf%40gmail.com&password=C9xvPC%24SCcU%3B6%7EV&redirect_url=%2F'
    getSessionIdPayload = {
        "email": "eleanorlewis676rsdf@gmail.com",
        "password": "C9xvPC$SCcU;6~V",
        "redirect_url": "/"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://app.neuronwriter.com/ucp/login', data=getSessionIdPayload, allow_redirects=False) as response:
            responseCookies = response.cookies.get('contai_session_id')
            sessionId = responseCookies.key + "=" + \
                responseCookies.value
            print("session id: ", sessionId)
    # Get data
    getDataHeader = {
        "Cookie": sessionId
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://app.neuronwriter.com/ucp/affiliate', headers=getDataHeader) as response:
            content = await response.read()
            pageSource = content.decode('utf-8')
            soup = BeautifulSoup(pageSource, "html.parser")
            data = []
            for row in soup.select('table[data-export_fname="aff_daily_stats"] tbody tr'):
                print(row)
                date = row.select('td')[0].text.strip()
                clicks = row.select('td')[1].text.strip()
                unique_ips = row.select('td')[2].text.strip()
                entry = {'date': date, 'clicks': clicks,
                         'unique IPs': unique_ips}
                data.append(entry)
            print('\n', data)

    return

asyncio.run(login())
