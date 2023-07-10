import aiohttp
import asyncio
import platform
import argparse
from datetime import datetime, timedelta

"""
-- days [-d] 
-- currency [-c]
"""

parser = argparse.ArgumentParser(description="PB Exchange")
parser.add_argument("--days", "-d", help="Days to show", default="1")
parser.add_argument("--currency", "-c", help="Currency", default="EUR,USD")
args = vars(parser.parse_args())


def command_line_parser():
    try:
        days = int(args['days'])
        if days < 1:
            print('Results can be shown for 1 to 10 days. Its results for 1 day.')
            days = 1
        elif days > 10:
            print('Results can be shown for 1 to 10 days. Its results for 10 days.')
            days = 10
        currency = args['currency'].split(',')
        return days, currency
    except ValueError:
        print('Incorrect input.')
        print('Results for 1 day and for EUR and USD:')
        days, currency = (1, ['EUR', 'USD'])
        return days, currency


async def main(urls, currency):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        response = await resp.json()
                        result = {'date': response['date']}
                        for cur in currency:
                            for exchange in response['exchangeRate']:
                                if exchange['currency'] == cur:
                                    result[cur] = exchange
                        print(result)
                    else:
                        print(f"Error status: {resp.status} for {url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}', str(err))


if __name__ == '__main__':
    days, currency = command_line_parser()
    base_url = 'https://api.privatbank.ua/p24api/exchange_rates?date='
    i = 0
    urls = []
    for day in range(days):
        date_ = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
        i += 1
        urls.append(str(base_url + date_))

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(urls, currency))
