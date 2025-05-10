import os
import requests
import time
import re
import concurrent.futures
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cneura_ai.logger import logger

class BodyTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_body = False
        self.ignored_tags = {"script", "style", "nav", "footer", "header", "aside", "form"}
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "body":
            self.in_body = True
        if tag in self.ignored_tags:
            self.skip_content = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "body":
            self.in_body = False
        if tag in self.ignored_tags:
            self.skip_content = False

    def handle_data(self, data):
        if self.in_body and not self.skip_content:
            self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)


class Research:
    def __init__(self, google_api_key, search_engine_id):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.driver = None
        self._init_selenium()

    def _init_selenium(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(180)

    def google_search(self, query, num_results=5):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.search_engine_id}&num={num_results}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return [(item["title"], item["link"]) for item in data.get("items", [])]
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Search API error: {e}")
            return []

    def duckduckgo_search(self, query, num_results=5):
        """DuckDuckGo search using duckduckgo_search library."""
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results)
                return [(r["title"], r["href"]) for r in results]
        except Exception as e:
            logger.error(f"Error during DuckDuckGo search: {e}")
            return []


    def scrape_page(self, url, retries=3):
        for attempt in range(retries):
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                time.sleep(3)
                return self.driver.page_source
            except Exception as e:
                logger.warning(f"[Attempt {attempt+1}] Failed to scrape {url}: {e}")
                time.sleep(2)
        logger.error(f"Final failure scraping {url}")
        return None

    def extract_body_text(self, html: str) -> str:
        parser = BodyTextExtractor()
        parser.feed(html)
        text = parser.get_text()
        return re.sub(r'\s+', ' ', text).strip()

    def process_results(self, query, engine="google", num_results=5):
        logger.info(f"Running query '{query}' using {engine} engine")

        if engine == "google":
            results = self.google_search(query, num_results)
        elif engine == "duckduckgo":
            results = self.duckduckgo_search(query, num_results)
        else:
            raise ValueError("Unknown engine specified.")

        if not results:
            logger.info("No search results found.")
            return {"query": query, "results": []}

        output = []

        def process_url(title_link):
            title, link = title_link
            html = self.scrape_page(link)
            if not html:
                return None
            body = self.extract_body_text(html)
            return {
                "title": title,
                "url": link,
                "content": body,
                "token_count": len(body.split())
            }

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_url, item) for item in results]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    output.append(result)

        return {"query": query, "results": output}

    def close(self):
        if self.driver:
            self.driver.quit()


researcher = Research(google_api_key=os.environ.get("GOOGLE_API_KEY"), search_engine_id=os.environ.get("SEARCH_ENGINE_ID"))
json_result = researcher.process_results("latest AI agents", engine="duckduckgo", num_results=3)
researcher.close()

import json
print(json.dumps(json_result, indent=2))
