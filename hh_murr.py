import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': '**/**',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
           }

base_url = 'https://spb.hh.ru/search/vacancy?area=2&st=searchVacancy&text=python&page=0'

def hh_parses(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')

        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)

            for i in range(count):
                url = f'https://spb.hh.ru/search/vacancy?area=2&st=searchVacancy&text=python&page={i}'

                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')

        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        for div in divs:

            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                })
            except:
                pass

        print(len(jobs))

    else:
        print('Error')
    print(count)
    return jobs

def files_writer(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('title', 'URL', 'company'))

        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company']))


g = hh_parses(base_url, headers)
files_writer(g)
