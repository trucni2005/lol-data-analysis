import csv
import time
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Import các hằng số từ config.py
from src.utils.config import (
    SERVERS, DURATIONS, MAX_PAGES, MAX_ITERATIONS, CSV_FILENAME, BASE_URL_TEMPLATE
)

class Crawler:
    def __init__(self, servers: List[str] = SERVERS, durations: List[str] = DURATIONS,
                 max_pages: int = MAX_PAGES, headless: bool = True):
        self.servers = servers
        self.durations = durations
        self.max_pages = max_pages
        self.headless = headless
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")  # Kích thước cửa sổ trình duyệt
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.implicitly_wait(20)
        return driver

    def construct_url(self, server: str, duration: str, page: int) -> str:
        """
        Xây dựng URL dựa trên server, duration và số trang.
        """
        base_url = BASE_URL_TEMPLATE.format(server=server, duration=duration)
        return f"{base_url}/page-{page}" if page > 1 else base_url

    def fetch_page(self, url: str) -> str:
        """
        Mở trang web và trả về HTML của trang.
        """
        try:
            print(f"Fetching URL: {url}")
            self.driver.get(url)
            time.sleep(3)  # Thay thế bằng WebDriverWait để kiểm soát tốt hơn
            return self.driver.page_source
        except WebDriverException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    def parse_links(self, html: str) -> List[str]:
        """
        Phân tích HTML và trích xuất các liên kết cần thiết.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        th_tags = soup.find_all('th', {'class': 'text-left-dark-only'})
        for th_tag in th_tags:
            a_tag = th_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                links.append(a_tag['href'])
        return links

    def crawl(self, limit: int = None) -> List[str]:
        """
        Thu thập tất cả các liên kết từ các server và duration đã định.
        """
        all_links = []
        count = 0
        try:
            for server in self.servers:
                for duration in self.durations:
                    for page in range(1, self.max_pages + 1):
                        url = self.construct_url(server, duration, page)
                        html = self.fetch_page(url)
                        if not html:
                            continue
                        links = self.parse_links(html)
                        all_links.extend(links)
                        count += 1
                        if limit and count >= limit:
                            print("Reached maximum iteration limit. Stopping crawl.")
                            return all_links
        finally:
            self.driver.quit()
            print("WebDriver closed.")
        return all_links