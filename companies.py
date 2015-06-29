import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.crmz.com/Directory/'

def get_state_urls():
    resp = requests.get(BASE_URL + 'CountryUS.htm')
    soup = BeautifulSoup(resp.text)
    for a in soup.select('a'):
        href = a.get('href')
        if href.startswith('State'):
            yield a.get('href')

def get_company_urls(state_url):
    

if __name__ == '__main__':
    # state_urls = list(get_state_urls())
    # print(len(state_urls))

