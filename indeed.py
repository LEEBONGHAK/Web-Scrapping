from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&l=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%84%B1%EB%82%A8&limit={LIMIT}&radius=25"


# indeed url에서 max_page 추출 함수
def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')

    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page


# 제목, 회사이름, 위치, 지원링크 추출
def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")

    if company:
        if company_anchor != None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None
    # 빈칸이 포함된 string 다음에 사용하여 () 속 문자를 없애주거나 빈칸을 없애줄 수 있음
    location = html.find(
        "span", {"class": "location accessible-contrast-color-location"}).string
    job_id = html["data-jk"]

    return {"title": title, "company": company, "location": location, "link": f"https://kr.indeed.com/viewjob?jk={job_id}&tk=1erlkb7qcqejt800&from=serp&vjs=3"}  # dictionary로 반환


# indeed의 pages를 받아서 그만큼의 request 생성
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeed page {page}")
        # 페이지 요청
        result = requests.get(f"{URL}&start={page * LIMIT}")  
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = extract_pages()
    jobs = extract_jobs(last_page)

    return jobs
