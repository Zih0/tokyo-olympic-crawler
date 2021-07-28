import requests
from bs4 import BeautifulSoup
from datetime import date
import json

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


def crawl_medalist_data(url):
    """
        메달 순위 크롤링 함수
        :param url: json url
        :return: dict
        """
    base_url = 'https://olympics.com/tokyo-2020/olympic-games'
    crawl_data = []
    gold = []
    silver = []
    bronze = []
    kr = []
    data = json.loads(requests.get(url).text)
    for medallist in data['medallistsJSON']:
        noc = medallist['c_code']
        name = medallist['a_name']
        gender = medallist['a_sex']
        image = base_url + medallist['a_img'].replace("../../..","")
        sport = medallist['d_code']
        if medallist['m_code'] == '1':
            medal = "금"
            gold.append({'국가': noc, '종목': sport, '메달': medal, '이름': name, '성별': gender, '사진': image})
        elif medallist['m_code'] == '2':
            medal = "은"
            silver.append({'국가': noc, '종목': sport, '메달': medal, '이름': name, '성별': gender, '사진': image})
        else:
            medal = "동"
            bronze.append({'국가': noc, '종목': sport, '메달': medal, '이름': name, '성별': gender, '사진': image})
        crawl_data.append({'국가': noc, '종목': sport, '메달': medal,'이름': name, '성별': gender, '사진': image})
        if noc == 'KOR':
            kr.append({'국가': noc, '종목': sport, '메달': medal, '이름': name, '성별': gender, '사진': image})
    updated = date.today().isoformat()
    medalists_result = {"date": updated, "medalists": crawl_data}
    gold_result = {"date": updated, "medalists": gold}
    silver_result = {"date": updated, "medalists": silver}
    bronze_result = {"date": updated, "medalists": bronze}
    kr_result = {"date": updated, "medalists": kr}

    return medalists_result, gold_result, silver_result, bronze_result, kr_result
