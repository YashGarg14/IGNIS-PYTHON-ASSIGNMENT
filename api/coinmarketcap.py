import requests
from bs4 import BeautifulSoup

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    @staticmethod
    def fetch_coin_data(coin):
        url = f"{CoinMarketCap.BASE_URL}{coin}/"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {}

        try:
            data['price'] = float(soup.find('div', class_='priceValue').text.replace('$', '').replace(',', ''))
            data['price_change'] = float(soup.find('span', class_='sc-15yy2pl-0 feeyND').text.replace('%', '').replace(',', ''))
            data['market_cap'] = int(soup.find('div', class_='statsValue').text.replace('$', '').replace(',', ''))
            # Additional data extraction can be added here similarly
        except Exception as e:
            data['error'] = str(e)

        # Extract official links, social links, and other relevant information
        data['official_links'] = [
            {'name': 'website', 'link': url}  # Example, modify as necessary
        ]
        data['socials'] = [
            {'name': 'twitter', 'url': 'https://twitter.com/example'}  # Example, modify as necessary
        ]
        return data
