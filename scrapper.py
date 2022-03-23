import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(URL) #스크래핑할 페이지 url 가져옴
    soup = BeautifulSoup(result.text, "html.parser") #쉽게 분석하기 위해
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a") #마지막 페이지를 얻기 위해
    last_page = pages[-2].get_text(strip=True) #strip=빈칸 삭제
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"scrapping SO: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page,url)
    return jobs
