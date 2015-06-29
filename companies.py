import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'http://www.crmz.com/Directory/'

def get_state_urls():
    resp = requests.get(BASE_URL)
    soup = BeautifulSoup(resp.text)
    for a in soup.select('a'):
        href = a.get('href')
        if href.startswith('State') or href.startswith('Country'):
            yield a.get('href')

def get_company_urls(state_url):
    resp = requests.get(urljoin(BASE_URL, state_url))
    soup = BeautifulSoup(resp.text)
    for a in soup.select('a'):
        href = a.get('href')
        if 'ReportPreview.aspx?BusinessId' in href:
            yield href

def get_company_data(company_url):
    resp = requests.get(urljoin(BASE_URL, company_url))
    soup = BeautifulSoup(resp.text)
    tables = soup.select('body > center > table')
    name = tables[2].select('tr')[1].td.text
    address1 = tables[2].select('tr')[2].td.text
    try:
        address2 = tables[2].select('tr')[3].select('td')[1].text
        ticker = tables[2].select('tr')[3].get_text()
    except IndexError:
        address2 = tables[2].select('tr')[4].select('td')[1].text
        ticker = tables[2].select('tr')[4].get_text()
    ticker_rex = re.search('Ticker: ([A-Z ]+)', ticker)
    if ticker_rex:
        ticker = ticker_rex.group(1)
    else:
        ticker = ''
    industry_rows = tables[6].select('table')[1].table.select('tr')
    sector = industry_rows[4].select('td')[2].text
    industry = industry_rows[5].select('td')[2].text

    # remove non-breaking spaces from address2
    address2 = address2.replace('\xa0', ' ')

    return dict(
        name=name,
        address1=address1,
        address2=address2,
        ticker=ticker,
        industry=industry,
        sector=sector
    )

if __name__ == '__main__':
    # data = get_company_data('http://www.crmz.com/Report/ReportPreview.aspx?BusinessId=419')
    # print(data)
    try:
        for state_url in get_state_urls():
            for company_url in get_company_urls(state_url):
                try:
                    company_data = get_company_data(company_url)
                    print('parsed {}'.format(urljoin(BASE_URL, company_url)), file=sys.stderr)
                    print(company_data, file=sys.stdout)
                except Exception as e:
                    print('error {}'.format(urljoin(BASE_URL, company_url)), file=sys.stderr)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
