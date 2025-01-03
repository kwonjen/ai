import json
import time


from bs4 import BeautifulSoup
from selenium import webdriver

import config

## 최신 작성순
URL = 'https://www.yanolja.com/reviews/domestic/1000102261'

# OpenAI Conn
client = config.Init.open_ai_conn();

def crawl_yanolja_reviews():
    review_list = []
    driver = webdriver.Chrome()
    driver.get(URL)

    ## 페이지 로드까지 기다리기
    time.sleep(3)

    scroll_count = 20
    for i in range(scroll_count):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ## 리뷰점수, 날짜, 리뷰텍스트 3가지 정보 필요

    review_containers = soup.select('#__next > section > div > div.css-1js0bc8 > div > div > div')
    review_date = soup.select('#__next > section > div > div.css-1js0bc8 > div > div > div > div.css-1mwn02k > div > div.css-1ivchjf > p')

    for i in range(len(review_containers)):
        review_text = review_containers[i].find('p', class_='content-text').text
        review_stars = review_containers[i].find_all('path', {'fill': 'currentColor'})
        star_cnt = len(review_stars)
        date = '2024.12.23' #review_date[i].text

        review_dict = {
            'review': review_text,
            'stars': star_cnt,
            'date': date
        }
        # print(review_dict)
        review_list.append(review_dict)

        with open('./res/reviews.json', 'w') as f:
            json.dump(review_list, f, indent=4, ensure_ascii=False)

def pre_process_review(path='./res/reviews.json'):

        with open(path, 'r', encoding='utf-8') as f:
            review_list = json.load(f)

        reviews_good, reviews_bad = [], []
        for r in review_list:
                if r['stars'] == 5:
                    reviews_good.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]') ## 각 리뷰의 시작과 끝을 스페셜토큰(REVIEW_START)을 추가해준다. 자연어 처리모델에 사용되는 방법
                else:
                    reviews_bad.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')

        reviews_good = reviews_good[:min(len(reviews_good), 50)]
        reviews_bad = reviews_bad[:min(len(reviews_bad), 50)]

        reviews_good_text = '\n'.join(reviews_good)
        reviews_bad_text = '\n'.join(reviews_bad)

        return reviews_good_text, reviews_bad_text

def pairwise_eval(reviews, answer_a, answer_b):
    eval_prompt = f"""[System]
    Please act as an impartial judge and evaluate the quality of the Korean summaries provided by two
    AI assistants to the set of user reviews on accommodations displayed below. You should choose the assistant that
    follows the user’s instructions and answers the user’s question better. Your evaluation
    should consider factors such as the helpfulness, relevance, accuracy, depth, creativity,
    and level of detail of their responses. Begin your evaluation by comparing the two
    responses and provide a short explanation. Avoid any position biases and ensure that the
    order in which the responses were presented does not influence your decision. Do not allow
    the length of the responses to influence your evaluation. Do not favor certain names of
    the assistants. Be as objective as possible. After providing your explanation, output your
    final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]"
    if assistant B is better, and "[[C]]" for a tie.
    [User Reviews]
    {reviews}
    [The Start of Assistant A’s Answer]
    {answer_a}
    [The End of Assistant A’s Answer]
    [The Start of Assistant B’s Answer]
    {answer_b}
    [The End of Assistant B’s Answer]"""

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': eval_prompt}],
        temperature=0.0
    )

    return completion
def summarize(reviews, prompt, temperature=0.0, model='gpt-4o-mini'):
    prompt = prompt + '\n\n' + reviews

    completion = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature
    )

    return completion

if __name__ == '__main__':

    ##1. 데이터 확보
    # crawl_yanolja_reviews()

    ##2. 데이터 전처리
    review_good, review_bad = pre_process_review()
    print("good_review = {}", review_good)
    print("bad_review = {}", review_good)

    ##3. Baseline 모델 개발
    PROMPT_BASELINE = f"""아래 숙소 리뷰에 대해 5문장 내로 요약해줘:"""

    ##4. 리뷰 요약
    print(summarize(review_good, PROMPT_BASELINE).choices[0].message.content)


    # print(pairwise_eval(review_good, summarize(review_good, PROMPT_BASELINE).choices[0].message.content, summary_real_20240526).choices[0].message.content)


