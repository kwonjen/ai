import json
import time


from bs4 import BeautifulSoup
from selenium import webdriver

## 최신 작성순
URL = 'https://www.yanolja.com/reviews/domestic/1000102261?sort=HOST_CHOICE'
def crawl_yanolja_reviews():
    review_list = []
    driver = webdriver.Chrome()
    driver.get(URL)

    ## 페이지 로드까지 기다리기
    time.sleep(3)

    scroll_count = 10
    for i in range(scroll_count):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);');
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ## 리뷰점수, 날짜, 리뷰텍스트 3가지 정보 필요

    review_containers = soup.select('#__next > section > div > div.css-1js0bc8 > div > div > div')
    review_date = soup.select('#__next > section > div > div.css-1js0bc8 > div > div > div > div.css-8ehu1o > div > div.css-1ivchjf > p')

    for i in range(len(review_containers)):


if __name__ == '__main__':
    crawl_yanolja_reviews()

