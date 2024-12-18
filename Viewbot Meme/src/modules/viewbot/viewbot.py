# Tracker.gg added cf clearance - testing headless useragent for bypass currently - neox 05/12/2024
# Credits to Zaptons - Check ReadME
# OpenAI ontop

import os
import random
import concurrent.futures
import requests
from threading import Lock
from user_agent import generate_user_agent
from src.modules.utils.logger import Logger
from src.modules.helper.config import Config
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
import time

class ViewBot():
    def __init__(self):
        self.views_sent, self.views_ratelimited, self.views_failed = 0, 0, 0
        self.config = Config()
        self.logger = Logger()
        self.proxy_list = []

    def load_proxy_list(self):
        with open(self.config.proxies_file, "r", encoding="utf8", errors="ignore") as file:
            self.proxy_list = file.read().splitlines()
        return self.proxy_list

    def set_proxy(self):
        proxy = random.choice(self.proxy_list)
        return {'http': f"http://{proxy}", 'https': f'http://{proxy}'}

    def generate_custom_user_agent(self):
        devices = [
            {"platform": "Windows", "browser": "Chrome", "version": random.randint(70, 110)},
            {"platform": "Macintosh", "browser": "Safari", "version": random.randint(10, 16)},
            {"platform": "Linux", "browser": "Firefox", "version": random.randint(50, 110)},
            {"platform": "Android", "browser": "Chrome", "version": random.randint(70, 110)},
            {"platform": "iOS", "browser": "Safari", "version": random.randint(10, 16)}
        ]

        device = random.choice(devices)
        if device['platform'] in ["Windows", "Linux", "Macintosh"]:
            return f"Mozilla/5.0 ({device['platform']}; x64) AppleWebKit/537.36 (KHTML, like Gecko) {device['browser']}/{device['version']} Safari/537.36"
        elif device['platform'] == "Android":
            return f"Mozilla/5.0 ({device['platform']} {random.randint(7, 13)}; Mobile; rv:{device['version']}) Gecko/20100101 Firefox/{device['version']}"
        elif device['platform'] == "iOS":
            return f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(12, 16)}_{random.randint(1, 6)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{device['version']}.0 Mobile/15E148 Safari/604.1"

    def get_cf_clearance_cookie(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            proxy = self.set_proxy()
            page.context.set_proxy(proxy)
            page.goto(url)
            page.wait_for_timeout(5000)
            cookies = page.context.cookies()
            cf_clearance_cookie = next((cookie for cookie in cookies if cookie['name'] == 'cf_clearance'), None)
            browser.close()
            return cf_clearance_cookie

    def send_request(self):
        time.sleep(random.uniform(1, 3))  
        
        session = requests.Session()
        proxy = self.set_proxy()
        session.proxies.update(proxy)

        cf_clearance_cookie = self.get_cf_clearance_cookie(self.config.link_to_boost)
        if cf_clearance_cookie:
            session.cookies.set('cf_clearance', cf_clearance_cookie['value'])
        else:
            self.logger.log("ERROR", "Failed to obtain cf_clearance cookie.")
            self.views_failed += 1
            return False

        user_agent = self.generate_custom_user_agent()

        headers = {
            'Accept': random.choice(['application/json,text/plain,*/*', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8']),
            'Accept-Encoding': random.choice(['gzip, deflate, br', 'gzip, deflate']),
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'en;q=0.7']),
            'Host': 'api.tracker.gg',
            'Origin': 'https://tracker.gg',
            'Referer': 'https://tracker.gg/',
            'sec-ch-ua': random.choice([
                '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                '"Microsoft Edge";v="90", "Chromium";v="90", "Not.A/Brand";v="25"'
            ]),
            'sec-ch-ua-mobile': random.choice(['?0', '?1']),
            'sec-ch-ua-platform': random.choice(['"Windows"', '"Linux"', '"Mac OS X"']),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            "User-Agent": user_agent,
        }

        response = session.get(self.config.link_to_boost, headers=headers)

        if response.status_code == 429:
            self.logger.log("ERROR", "You are being rate limited, retrying.")
            self.views_ratelimited += 1
            return False

        if response.status_code != 200:
            self.logger.log("ERROR", f"Error sending request: {response.status_code}")
            self.views_failed += 1
            return False

        self.views_sent += 1
        self.logger.log("SUCCESS", f"Successfully sent request. Total views sent: {self.views_sent}")
        return True

    def start(self):
        self.logger.log("INFO", "Loading proxies...")
        self.load_proxy_list()

        self.logger.log("INFO", "Starting view bot threads...")
        with ThreadPoolExecutor(max_workers=self.config.threads) as executor:
            while True:
                futures = {executor.submit(self.send_request) for _ in range(self.config.threads)}
                concurrent.futures.wait(futures)
