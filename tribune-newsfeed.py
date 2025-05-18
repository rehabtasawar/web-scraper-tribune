import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


csv_filename = 'tribune_newsfeed.csv'
base_url = 'https://tribune.com.pk/'

cookies = {
    '_gid': 'GA1.3.1267643114.1747130675',
    'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQRWXMAQRWXMAEsACBENBqFoAP_gAEPgAAAgINJD7C7FbSFCyD5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAYFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAQNVSD2F2K2kKFkHCmwXYAYBCujYAAhQgAAAkCBMACgAUgQAgFJIAgCIFAAAAAAAAAQEiCQAAQABAAAIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAQAAIAAQAAAAIAABEhAAAQQAEAAAAAAAQAAA%22%2C%222~70.89.93.108.122.149.184.196.236.259.311.313.314.323.358.415.442.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%2217609457-BABF-46F2-94D0-772716CB53B9%22%5D%5D',
    '_pubcid': '552d24c1-7ac2-4e0e-9705-f8b5d0f8a952',
    '__gsas': 'ID=c992b73ba34904dc:T=1747130660:RT=1747130660:S=ALNI_MZXJCxLuLHpzqqbXyoGi9BseE6cSg',
    '_ga_9LKLY5PKLW': 'GS2.1.s1747130754$o1$g1$t1747130771$j0$l0$h0',
    '_ga_ZYJ0HT46LD': 'GS2.1.s1747130754$o1$g1$t1747130771$j0$l0$h0',
    '_pubcid_cst': 'zix7LPQsHA%3D%3D',
    '_ga_1VFHRSCV8M': 'GS2.1.s1747130785$o1$g1$t1747130805$j0$l0$h0',
    '_ga_T04MK197EX': 'GS2.1.s1747130786$o1$g1$t1747130805$j0$l0$h0',
    '_ga_SGDPP0HZTL': 'GS2.1.s1747130671$o1$g1$t1747131206$j60$l0$h0',
    '_ga': 'GA1.3.536356793.1747130672',
    '_gat_gtag_UA_15752538_1': '1',
    '__gads': 'ID=fe1d24fe1f26b14b:T=1747130589:RT=1747131113:S=ALNI_MZkQcCZL60b0hryCaoBJhBxKOSwcQ',
    '__gpi': 'UID=000010abefae9c2e:T=1747130589:RT=1747131113:S=ALNI_MbIun8CTpWjN7da_6GoWgblPmW36w',
    '__eoi': 'ID=57854fa9923d38a3:T=1747130589:RT=1747131113:S=AA-AfjbPaJKqC8L0MowdX8xhGR8b',
    'FCNEC': '%5B%5B%22AKsRol_wgOvp8-m2ENJZgK2eCH-Wrs6egkwOF8OghI_jsOfYG2VThjMZTPmFRe8jN8Yjh8wm7C3aZ1seya8VMoxewoO6bQWKiqTscgWoGUC8XiTG6SPeEDWVY6Oe4Bo3ZsIQCJ7cyCmGsXLTAjYVmJngHkNusoEEtw%3D%3D%22%5D%5D',
    'cto_bundle': 'jLCnv19qTUZISEpyOCUyRmUlMkJOaExiTWlUall1bjNwNllwSnNCQjAwSW1WRkNBTHFZNFlBZTFTUEhKQ29QVWh3UTFjU096Znl0YiUyQnNZMjdJUEZ1aUYlMkJnelRFMVpkMHlEU0RMM0tNS2FUMTFJVkRwbHNVMmZibVM4RyUyQnZkWFJPdWQwcE95TmtpTG5taTJPZmNRd0xsbmclMkZNUFNDeVElM0QlM0Q',
    'cto_bidid': '5V9-CV9YcHAlMkJ1UDFqZmpPTjBaelduZU5WYUJpRzJ2TjZXQ1NSWnN5MlgwUTBNWFRLM0FoQjUlMkJFWnFlY1U3cXRJRVc0Y0IyJTJGOEs3dnpDN0lPUTFRdVhONDYzNVpFJTJGMm10MFVGQzVMeXlZVmh5cGMwTEMlMkZCZzZVVEJ1RCUyQmcxdExoZTM0JTJC',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Tue, 13 May 2025 10:11:34 GMT',
    'priority': 'u=0, i',
    'referer': 'https://tribune.com.pk/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': '_gid=GA1.3.1267643114.1747130675; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQRWXMAQRWXMAEsACBENBqFoAP_gAEPgAAAgINJD7C7FbSFCyD5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAYFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAQNVSD2F2K2kKFkHCmwXYAYBCujYAAhQgAAAkCBMACgAUgQAgFJIAgCIFAAAAAAAAAQEiCQAAQABAAAIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAQAAIAAQAAAAIAABEhAAAQQAEAAAAAAAQAAA%22%2C%222~70.89.93.108.122.149.184.196.236.259.311.313.314.323.358.415.442.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%2217609457-BABF-46F2-94D0-772716CB53B9%22%5D%5D; _pubcid=552d24c1-7ac2-4e0e-9705-f8b5d0f8a952; __gsas=ID=c992b73ba34904dc:T=1747130660:RT=1747130660:S=ALNI_MZXJCxLuLHpzqqbXyoGi9BseE6cSg; _ga_9LKLY5PKLW=GS2.1.s1747130754$o1$g1$t1747130771$j0$l0$h0; _ga_ZYJ0HT46LD=GS2.1.s1747130754$o1$g1$t1747130771$j0$l0$h0; _pubcid_cst=zix7LPQsHA%3D%3D; _ga_1VFHRSCV8M=GS2.1.s1747130785$o1$g1$t1747130805$j0$l0$h0; _ga_T04MK197EX=GS2.1.s1747130786$o1$g1$t1747130805$j0$l0$h0; _ga_SGDPP0HZTL=GS2.1.s1747130671$o1$g1$t1747131206$j60$l0$h0; _ga=GA1.3.536356793.1747130672; _gat_gtag_UA_15752538_1=1; __gads=ID=fe1d24fe1f26b14b:T=1747130589:RT=1747131113:S=ALNI_MZkQcCZL60b0hryCaoBJhBxKOSwcQ; __gpi=UID=000010abefae9c2e:T=1747130589:RT=1747131113:S=ALNI_MbIun8CTpWjN7da_6GoWgblPmW36w; __eoi=ID=57854fa9923d38a3:T=1747130589:RT=1747131113:S=AA-AfjbPaJKqC8L0MowdX8xhGR8b; FCNEC=%5B%5B%22AKsRol_wgOvp8-m2ENJZgK2eCH-Wrs6egkwOF8OghI_jsOfYG2VThjMZTPmFRe8jN8Yjh8wm7C3aZ1seya8VMoxewoO6bQWKiqTscgWoGUC8XiTG6SPeEDWVY6Oe4Bo3ZsIQCJ7cyCmGsXLTAjYVmJngHkNusoEEtw%3D%3D%22%5D%5D; cto_bundle=jLCnv19qTUZISEpyOCUyRmUlMkJOaExiTWlUall1bjNwNllwSnNCQjAwSW1WRkNBTHFZNFlBZTFTUEhKQ29QVWh3UTFjU096Znl0YiUyQnNZMjdJUEZ1aUYlMkJnelRFMVpkMHlEU0RMM0tNS2FUMTFJVkRwbHNVMmZibVM4RyUyQnZkWFJPdWQwcE95TmtpTG5taTJPZmNRd0xsbmclMkZNUFNDeVElM0QlM0Q; cto_bidid=5V9-CV9YcHAlMkJ1UDFqZmpPTjBaelduZU5WYUJpRzJ2TjZXQ1NSWnN5MlgwUTBNWFRLM0FoQjUlMkJFWnFlY1U3cXRJRVc0Y0IyJTJGOEs3dnpDN0lPUTFRdVhONDYzNVpFJTJGMm10MFVGQzVMeXlZVmh5cGMwTEMlMkZCZzZVVEJ1RCUyQmcxdExoZTM0JTJC',
}

def read_existing_data(csv_filename):
    existing_links = set()
    existing_texts = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_links.add(row['link'])
                existing_texts.add(row['text'])
    return existing_links, existing_texts

def fetch_article_details(article_url):
    try:
        response = requests.get(article_url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Title extraction fix
        title_container = soup.find("div", class_="story-box-section")
        title_tag = title_container.h1 if title_container else None
        title = title_tag.text.strip() if title_tag else "No title found"  # Ensure title is assigned

        # Author and published date
        author_box = soup.find('div', class_='left-authorbox')
        if author_box:
            spans = author_box.find_all('span')
            if len(spans) >= 2:
                raw_date = spans[1].text.strip()
                published_date = raw_date
            else:
                published_date = "No date found"
        else:
            published_date = "No date found"

        # Description extraction
        description_tag = soup.find("p", class_="story-excerpt")
        description = description_tag.text.strip() if description_tag else "No description found"

        # Content extraction
        # Content extraction
        story_text_blocks = soup.find_all('span', class_='story-text')

        content = []
        for block in story_text_blocks:
            content.extend(p.text.strip() for p in block.find_all('p'))

        text = ' '.join(content).replace('\n', ' ').replace('\r', ' ').strip() if content else "No content found"



        data = {
            'country': 'Pakistan',
            'source': 'Tribune',
            'title': title,
            'link': article_url,
            'published_date': published_date,
            'published_by': 'Tribune News Desk',
            'description': description,
            'text': text
        }

        return data

    except Exception as e:
        print(f"Error fetching article {article_url}: {e}")
        return None


def extract_articles(soup, existing_links, existing_texts, section_class):
    section_divs = soup.find_all("div", class_=section_class)
    urls_to_fetch = []

    for section in section_divs:
        a_tag = section.find('a')
        if a_tag:
            link = a_tag.get('href')
            if not link.startswith("http"):
                link = "https://tribune.com.pk" + link
            if link and link not in existing_links:
                urls_to_fetch.append(link)

    new_articles = []

    def fetch_and_validate(url):
        time.sleep(1.5)  # ✅ Rate limiting
        article_data = fetch_article_details(url)
        if not article_data:
            return None
        if not article_data['title'].strip() or not article_data['text'].strip():
            return None
        if article_data['link'] in existing_links:
            return None
        if article_data['text'] in existing_texts:
            return None
        return article_data

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_url = {executor.submit(fetch_and_validate, url): url for url in urls_to_fetch}
        for future in as_completed(future_to_url):
            data = future.result()
            if data:
                new_articles.append(data)
                existing_links.add(data['link'])  # prevent dupes within same run

    return new_articles


def save_to_csv(data_list, csv_filename):
    if not data_list:
        print("No new articles to save.")
        return

    fieldnames = data_list[0].keys()
    cleaned_data = []

    seen_links = set()
    for row in data_list:
        if row['link'] in seen_links:
            continue
        if not row['title'].strip() or not row['text'].strip():
            continue
        seen_links.add(row['link'])
        cleaned_data.append(row)

    if not cleaned_data:
        print("No valid articles to write.")
        return

    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"\nSaved {len(cleaned_data)} clean articles to '{csv_filename}'")

def main():
    response = requests.get(base_url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    existing_links, existing_texts = read_existing_data(csv_filename)

    # Define all the different newstype classes you want to scrape
    newstype_classes = [
        "main-section1-top-heading",   
        "home-main-small-button-story-desc",  
        "related-content-text",  
        "shortnews-right-caption",
        "sidebarblogmain-img",
        "sidebarblog-caption",
        "horiz-news1-caption",
        "related-post-sdBar",
        "stories-slider-captions",
        "horiz-news2-caption",
        "main-section1-caption",
        "featured-row",
        "shortnews-img",
        "general-news",
        "horiz-news3-caption"
    ]

    total_new_articles = []

    for section_class in newstype_classes:
        print(f"\nProcessing section: {section_class}")
        new_articles = extract_articles(soup, existing_links, existing_texts, section_class)
        total_new_articles.extend(new_articles)

    save_to_csv(total_new_articles, csv_filename)

if __name__ == "__main__":
    main()