import requests
from bs4 import BeautifulSoup
from datetime import date

def parsing_bs(url):
    """
    BeautifulSoup로 파싱하는 함수
    :param url: olympic url,
    :return: BeautifulSoup Object
    """

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def crawl_ranking_data(soup):
    """
    메달 순위 크롤링 함수
    :param soup: BeautifulSoup Object
    :return: json
    """

    crawl_data = []
    table = soup.select_one('.table-schedule')
    trs = table.select('tr')
    for tr in trs[1:]:
        rank = tr.contents[1].text.strip()
        country = tr.contents[3].text.strip()
        gold = tr.contents[5].text.strip()
        silver = tr.contents[7].text.strip()
        bronze = tr.contents[9].text.strip()
        total = tr.contents[11].text.strip()
        rank_by_total = tr.contents[13].text.strip()
        noc = tr.contents[15].text.strip()

        crawl_data.append({"순위": rank,"국가": country,"금": gold,"은": silver,"동": bronze,"합계": total,"합계 순위": rank_by_total,"NOC": noc})

    updated = date.today().isoformat()
    result = {"date": updated, "ranking": crawl_data}
    return result

