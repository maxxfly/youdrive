import aiohttp
import asyncio
import re
import argparse


async def youdrive():
    """Get position of the car"""

    parser = argparse.ArgumentParser(description='Post picture on Twitter')

    parser.add_argument('--login', dest='login', action='store', required=True)
    parser.add_argument('--password', dest='password', action='store', required=True)
    parser.add_argument('--car_id', dest='car_id', action='store', required=True)

    args = parser.parse_args()

    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.direct-assurance.fr/Sales/AGDF/DirectAssurance/Motor/Standard/Desktop/LogOn/initLogOn') as response:
            html = await response.text()

            p = re.compile('(/Sales/(.*)/Common/Login)', re.MULTILINE)            
            m = p.search(html)

            url_form = 'https://www.direct-assurance.fr' + m[1]
            key_path = m[2]

        payload = {'UserName': args.login, 
                   'Password': args.password }

        async with session.post(url_form, data=payload) as response:
            html = await response.text()
            cookie_auth = response.cookies['AuthCookie']

        url_api = f'https://www.direct-assurance.fr/Sales/{key_path}/YouDriveDashboard/LastLocation/{args.car_id}'

        print(url_api)
        async with session.post(url_api) as response:
            html = await response.text()
            print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(youdrive())