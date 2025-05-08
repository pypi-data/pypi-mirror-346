import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abstract_security import *
from abstract_webtools import *
DOWNLOAD_DIR = os.path.abspath("./downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
class K2SDownloader:
    def __init__(self,env_path=None):
        self.env_path = env_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = self._init_driver()
        self.logged_in = False

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def login(self):
        userName = get_env_value('userName',path=self.env_path)
        passWord = get_env_value('passWord',path=self.env_path)

        self.driver.get("https://k2s.cc/auth/login")
        time.sleep(3)

        
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "input-password-auto-complete-on")
        email_input.send_keys(userName)
        password_input.send_keys(passWord)
        password_input.send_keys(Keys.RETURN)

        #WebDriverWait(self.driver, 20).until(
        #    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Logout')]"))
        #)
        self.logged_in = True
        print("Login successful")
        #except Exception as e:
        #    print(f"Login failed: {e}")
        #    with open('login_error.html', 'w', encoding='utf-8') as f:
        #        f.write(self.driver.page_source)

    def download_file(self, url):
        if not self.logged_in:
            self.login()

        print(f"Navigating to: {url}")
        self.driver.get(url)
        time.sleep(5)

        if 'captcha' in self.driver.page_source.lower():
            print("CAPTCHA detected. Manual intervention required.")
            return

        try:
            download_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/download"], button[class*="download"]'))
            )
            print("Download button found; attempting to click or fetch URL")
            download_url = download_button.get_attribute('href')

            if download_url:
                response = self.session.get(download_url, stream=True)
                file_name = self._extract_filename(response, download_url)
                file_path = os.path.join(DOWNLOAD_DIR, file_name)

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {file_path}")
                return file_path
            else:
                download_button.click()
                print("Button clicked. Waiting for download...")
                time.sleep(30)  # adjust as needed
        except Exception as e:
            print(f"Download failed for {url}: {e}")

    def _extract_filename(self, response, url):
        cd = response.headers.get('Content-Disposition', '')
        if 'filename=' in cd:
            return cd.split('filename=')[-1].strip('"')
        return url.split('/')[-1].split('?')[0]

class dlsManager:
    def __init__(self, downloader):
        self.downloader = downloader
        self.all_dls = []

    def is_prev_dl(self, data):
        k2s_link = data.get('k2s')
        for prev_data in self.all_dls:
            if prev_data.get('k2s') == k2s_link:
                return True
        self.all_dls.append(data)
        return False

    def dl_k2s_link(self, k2s_link):
        if k2s_link:
            print(f"Downloading: {k2s_link}")
            self.downloader.download_file(k2s_link)
            time.sleep(10)


def get_soup(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch soup for {url}: {e}")
        return None

def get_k2s_link(soup):
    match = re.search(r'https://k2s\.cc/file/[^"<]+', str(soup))
    return match.group(0) if match else None
