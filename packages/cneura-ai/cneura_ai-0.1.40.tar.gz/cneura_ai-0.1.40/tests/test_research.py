import os
import re
import time
import atexit
import requests
import concurrent.futures
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from readability import Document
from lxml import html as lxml_html
from cneura_ai.logger import logger  # Ensure your logger is properly configured

class Research:
    def __init__(self, google_api_key, search_engine_id, max_workers=4):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.driver = None
        self.max_workers = max_workers
        self._init_selenium()
        atexit.register(self.close)

    def _init_selenium(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(60)

    def google_search(self, query, num_results=5):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.search_engine_id}&num={num_results}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return [(item["title"], item["link"]) for item in data.get("items", [])]
        except requests.RequestException as e:
            logger.error(f"Google Search API error: {e}")
            return []

    def duckduckgo_search(self, query, num_results=5):
        try:
            from duckduckgo_search import DDGS  # pip install duckduckgo-search
            with DDGS() as ddgs:
                results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results)
                return [(r["title"], r["href"]) for r in results]
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    def scrape_page(self, url, retries=2):
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"[Selenium] Attempt {attempt} scraping {url}")
                self.driver.get(url)
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(1)
                html = self.driver.execute_script("return document.documentElement.outerHTML;")
                if re.search(r"captcha|verify you are human|cloudflare", html, re.IGNORECASE):
                    logger.warning("CAPTCHA or challenge detected.")
                    continue
                return html
            except Exception as e:
                logger.warning(f"[Selenium] Failed attempt {attempt} on {url}: {e}")
                time.sleep(1)

        # Fallback with requests
        try:
            logger.info(f"[Fallback] Trying requests for {url}")
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                return resp.text
            else:
                logger.warning(f"[Fallback] Non-200 status: {resp.status_code}")
        except Exception as e:
            logger.warning(f"[Fallback] Request failed: {e}")

        logger.error(f"[Error] Final failure scraping {url}")
        return None

    def extract_main_content(self, html: str) -> str:
        try:
            doc = Document(html)
            summary_html = doc.summary()
            tree = lxml_html.fromstring(summary_html)
            text = tree.text_content()
            return re.sub(r'\s+', ' ', text).strip()
        except Exception as e:
            logger.error(f"Readability extraction failed: {e}")
            return ""

    def process_results(self, query, engine="google", num_results=5):
        logger.info(f"Searching: '{query}' with {engine}")
        if engine == "google":
            results = self.google_search(query, num_results)
        elif engine == "duckduckgo":
            results = self.duckduckgo_search(query, num_results)
        else:
            raise ValueError("Invalid engine. Use 'google' or 'duckduckgo'.")

        if not results:
            logger.warning("No results found.")
            return {"query": query, "results": []}

        output = []

        def process(title_link):
            title, link = title_link
            domain = urlparse(link).netloc
            logger.info(f"[Process] Scraping {domain}")
            html = self.scrape_page(link)
            if not html:
                return None
            text = self.extract_main_content(html)
            if len(re.findall(r'\w+', text)) < 30:
                logger.info(f"Skipping short content from {link}")
                return None
            return {
                "title": title,
                "url": link,
                "content": text,
                "token_count": len(re.findall(r'\w+', text))
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(process, item) for item in results]
            for f in concurrent.futures.as_completed(futures):
                res = f.result()
                if res:
                    output.append(res)

        return {"query": query, "results": output}

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


# Example usage
if __name__ == "__main__":
    researcher = Research(
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        search_engine_id=os.environ.get("SEARCH_ENGINE_ID")
    )
    json_result = researcher.process_results("latest AI agents", engine="duckduckgo", num_results=3)
    researcher.close()

    import json
    print(json.dumps(json_result, indent=2))
