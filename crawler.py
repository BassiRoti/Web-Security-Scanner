import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser


class Crawler:


    def __init__(self, target_url, delay=1):

        self.target_url = target_url
        self.delay = delay
        self.robot_parser = self.init_robot_parser()
        self.site_map = set()
        self.visited_links = set()  

    def init_robot_parser(self):
        robot_parser = RobotFileParser()
        robots_url = urljoin(self.target_url, 'robots.txt')
        robot_parser.set_url(robots_url)
        try:
            robot_parser.read()  
            print(f"Robots.txt loaded from: {robots_url}")
        except Exception as e:
            print(f"Failed to load robots.txt from {robots_url}: {e}")
        return robot_parser

    def fetch_urls_from_robots(self):
        """Fetch and parse URLs directly listed in robots.txt."""
        urls = []
        robots_url = urljoin(self.target_url, 'robots.txt')

        try:
            response = requests.get(robots_url)
            response.raise_for_status()
            for line in response.text.splitlines():
                if line.lower().startswith("disallow:") or line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:  
                        url = urljoin(self.target_url, path)
                        urls.append(url)
            print(f"Fetched URLs from robots.txt: {urls}")
        except Exception as e:
            print(f"Error fetching robots.txt: {e}")

        return urls

    def crawl(self):
        """Crawl the website using URLs fetched from robots.txt."""
        urls = self.fetch_urls_from_robots()
        all_urls = set()

        for url in urls:
            all_urls.add(url)
            internal_links = self.extract_links(url)
            all_urls.update(internal_links)
            time.sleep(self.delay)  

        self.site_map = all_urls
        return self.site_map

    def extract_links(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
            internal_links = [link for link in links if urlparse(link).netloc == urlparse(self.target_url).netloc]
            print(f"Extracted {len(internal_links)} internal links from {url}")
            return internal_links
        except Exception as e:
            print(f"Error fetching links from {url}: {e}")
            return []

    def get_collected_urls(self):
        return self.site_map

