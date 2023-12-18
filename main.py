import requests
import re
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from tqdm import tqdm

def solve(list_item):
    if "jobs/result" in list_item:
        return True
    return False

def get_href_link(list_item, link_base):
    a_tag = list_item.find('a')
    href = a_tag.get('href')
    link = link_base+str(href)
    return link

def get_job_links_from_url(url, link_base):
    response = requests.get(url)

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    all_list_items = soup.find_all('li')

    job_listings = [x for x in all_list_items if solve(str(x))]
    job_listings_links = [get_href_link(job_listings_list_item, link_base) for job_listings_list_item in job_listings]
    return job_listings_links

def get_all_job_links(url, pages, link_base):
    all_links = []
    for i in range(1, 1+pages):
        page_url = url+'?page=' + str(i)
        all_links.extend(get_job_links_from_url(page_url, link_base))
    return all_links

def get_all_job_links_non_paginated(url, base_url='https://boards.greenhouse.io/'):
    all_links = []
    response = requests.get(base_url+url)

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    all_list_items = soup.find_all('a')

    all_links = [base_url+str(x.get('href')) for x in all_list_items if '/phonepe/jobs' in str(x)]
    return all_links


def get_job_titles_and_reqs(job_links, save=False):
    print(len(job_links))
    scraped_result = {}
    for job_link in job_links:
        response = requests.get(job_link)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        all_list_items = soup.find_all('li')
        all_list_items = [list_item for list_item in all_list_items if not list_item.find('div') and not list_item.find('a') and not list_item.find('span') and not list_item.find('svg') and not list_item.find('i')]
        print(len(all_list_items))
        cleaned_strings = [re.search(r'<li>(.*?)</li>', str(li), re.DOTALL).group(1).strip() if li is not None else "" for li in all_list_items]
        print(len(cleaned_strings))
        scraped_result[job_link] = cleaned_strings
    if(save):
        json_data = json.dumps(scraped_result, indent=2)
        with open('output.json', 'w') as json_file:
            json_file.write(json_data)
        return scraped_result

def get_job_titles_and_reqs_new(job_links, save=False):
    print(len(job_links))
    scraped_result = {}
    for job_link in tqdm(job_links, desc="Processing", unit="iteration"):
        response = requests.get(job_link)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        all_list_items = soup.find_all('li')
        cleaned_strings = [extract_text(str(list_item)) for list_item in all_list_items]
        scraped_result[job_link] = cleaned_strings
    if(save):
        json_data = json.dumps(scraped_result, indent=2)
        with open('output.json', 'w') as json_file:
            json_file.write(json_data)
        return scraped_result
    return cleaned_strings

def extract_text(html_content, tags_to_remove=['span', 'a', 'h', 'strong']):
    pattern = re.compile(r'<li[^>]*>\s*(.*?)\s*</li>')
    match = pattern.search(html_content)
    if match:
        extracted_text = match.group(1)
        for tag in tags_to_remove:
            extracted_text = re.sub(fr'<{tag}[^>]*>', '', extracted_text)
            extracted_text = re.sub(fr'</{tag}>', '', extracted_text)
        return extracted_text
    return None

def main():
    # url = "https://www.google.com/about/careers/applications/jobs/results/"
    # link_base = "https://www.google.com/about/careers/applications/"
    # job_links = get_all_job_links(url, 1, link_base)
    # get_job_titles_and_reqs(job_links)
    job_links = get_all_job_links_non_paginated('phonepe')
    get_job_titles_and_reqs_new(job_links, True)

if __name__ == '__main__':
    main()